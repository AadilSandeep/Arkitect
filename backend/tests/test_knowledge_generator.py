"""Tests for the KnowledgeGenerator service."""

import pytest

from app.services.knowledge.knowledge_generator import KnowledgeGenerator
from app.schemas.response import Complexity, Goal


@pytest.fixture
def generator() -> KnowledgeGenerator:
    return KnowledgeGenerator()


def _make_goal(domain: str = "Web Development") -> Goal:
    return Goal(
        user_input="Test goal",
        domain=domain,
        goal_type="Test Project",
        complexity=Complexity.MEDIUM,
    )


class TestKnowledgeGeneration:
    """Verify knowledge area generation."""

    def test_returns_three_priority_levels(self, generator: KnowledgeGenerator) -> None:
        result = generator.generate(_make_goal())
        assert isinstance(result.high, list)
        assert isinstance(result.medium, list)
        assert isinstance(result.low, list)

    def test_web_dev_includes_expected_areas(self, generator: KnowledgeGenerator) -> None:
        result = generator.generate(_make_goal("Web Development"))
        assert "HTML" in result.high
        assert "CSS" in result.high
        assert "JavaScript" in result.high

    def test_all_levels_have_items(self, generator: KnowledgeGenerator) -> None:
        result = generator.generate(_make_goal())
        assert len(result.high) > 0
        assert len(result.medium) > 0
        assert len(result.low) > 0

    def test_fallback_for_unknown_domain(self, generator: KnowledgeGenerator) -> None:
        result = generator.generate(_make_goal("Alien Technology"))
        assert len(result.high) > 0

    def test_all_domains_produce_knowledge(self, generator: KnowledgeGenerator) -> None:
        domains = [
            "Web Development", "Mobile Development", "Data Science",
            "Content Creation", "Marketing", "Game Development",
            "E-Commerce", "DevOps", "General",
        ]
        for domain in domains:
            result = generator.generate(_make_goal(domain))
            assert len(result.high) > 0, f"Domain {domain} missing high-priority knowledge"
