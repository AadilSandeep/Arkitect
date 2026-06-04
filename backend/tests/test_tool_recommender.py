"""Tests for the ToolRecommender service."""

import pytest

from app.services.recommendations.recommender import ToolRecommender
from app.schemas.response import Complexity, Deliverable, Goal


@pytest.fixture
def recommender() -> ToolRecommender:
    return ToolRecommender()


def _make_goal(domain: str = "Web Development") -> Goal:
    return Goal(
        user_input="Test goal",
        domain=domain,
        goal_type="Test Project",
        complexity=Complexity.MEDIUM,
    )


def _make_deliverables() -> list[Deliverable]:
    return [
        Deliverable(id=1, title="UI/UX Design", description="Design the interface."),
        Deliverable(id=2, title="Authentication System", description="Add auth."),
        Deliverable(id=3, title="Database Design", description="Design the DB."),
    ]


class TestToolRecommendation:
    """Verify tool recommendation behavior."""

    def test_returns_tools_for_known_domain(self, recommender: ToolRecommender) -> None:
        tools = recommender.recommend(_make_goal(), _make_deliverables())
        assert len(tools) >= 4

    def test_max_tool_count(self, recommender: ToolRecommender) -> None:
        tools = recommender.recommend(_make_goal(), _make_deliverables())
        assert len(tools) <= 10

    def test_no_duplicate_tool_names(self, recommender: ToolRecommender) -> None:
        tools = recommender.recommend(_make_goal(), _make_deliverables())
        names = [t.name for t in tools]
        assert len(names) == len(set(names))

    def test_tools_have_valid_categories(self, recommender: ToolRecommender) -> None:
        tools = recommender.recommend(_make_goal(), _make_deliverables())
        valid_categories = {"AI", "Development", "Design", "Productivity", "Marketing", "Other"}
        for tool in tools:
            assert tool.category.value in valid_categories

    def test_deliverable_specific_tools_injected(self, recommender: ToolRecommender) -> None:
        """Deliverables with relevant keywords should inject extra tools."""
        # Use a domain with fewer base tools so injected ones aren't capped out
        goal = _make_goal("General")
        deliverables_with_auth = [
            Deliverable(id=1, title="Authentication System", description="Add auth."),
        ]
        tools = recommender.recommend(goal, deliverables_with_auth)
        tool_names = {t.name for t in tools}
        # Auth0 should be injected due to "Authentication" deliverable
        assert "Auth0" in tool_names

    def test_fallback_for_unknown_domain(self, recommender: ToolRecommender) -> None:
        tools = recommender.recommend(_make_goal("Unknown"), [])
        assert len(tools) >= 4

    def test_all_domains_produce_tools(self, recommender: ToolRecommender) -> None:
        domains = [
            "Web Development", "Mobile Development", "Data Science",
            "Content Creation", "Marketing", "Game Development",
            "E-Commerce", "DevOps", "General",
        ]
        for domain in domains:
            tools = recommender.recommend(_make_goal(domain), [])
            assert len(tools) >= 4, f"Domain {domain} produced too few tools"
