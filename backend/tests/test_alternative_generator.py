"""Tests for the AlternativeGenerator service."""

import pytest

from app.services.alternatives.alternative_generator import AlternativeGenerator
from app.schemas.response import Complexity, Goal


@pytest.fixture
def generator() -> AlternativeGenerator:
    return AlternativeGenerator()


def _make_goal(domain: str = "Web Development") -> Goal:
    return Goal(
        user_input="Test goal",
        domain=domain,
        goal_type="Test Project",
        complexity=Complexity.MEDIUM,
    )


class TestAlternativeGeneration:
    """Verify alternative workflow generation."""

    def test_returns_four_strategies(self, generator: AlternativeGenerator) -> None:
        result = generator.generate(_make_goal())
        assert result.fastest is not None
        assert result.cheapest is not None
        assert result.highest_quality is not None
        assert result.beginner_friendly is not None

    def test_each_strategy_has_summary(self, generator: AlternativeGenerator) -> None:
        result = generator.generate(_make_goal())
        assert result.fastest.summary
        assert result.cheapest.summary
        assert result.highest_quality.summary
        assert result.beginner_friendly.summary

    def test_each_strategy_has_tools(self, generator: AlternativeGenerator) -> None:
        result = generator.generate(_make_goal())
        assert len(result.fastest.tools) > 0
        assert len(result.cheapest.tools) > 0
        assert len(result.highest_quality.tools) > 0
        assert len(result.beginner_friendly.tools) > 0

    def test_fallback_for_unknown_domain(self, generator: AlternativeGenerator) -> None:
        result = generator.generate(_make_goal("Unknown Domain"))
        assert result.fastest.summary
        assert len(result.fastest.tools) > 0

    def test_all_domains_produce_alternatives(self, generator: AlternativeGenerator) -> None:
        domains = [
            "Web Development", "Mobile Development", "Data Science",
            "Content Creation", "Marketing", "Game Development",
            "E-Commerce", "DevOps", "General",
        ]
        for domain in domains:
            result = generator.generate(_make_goal(domain))
            assert result.fastest.summary, f"Domain {domain} missing fastest summary"
