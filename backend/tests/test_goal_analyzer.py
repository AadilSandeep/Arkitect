"""Tests for the GoalAnalyzer service."""

import pytest

from app.services.goal_analysis.analyzer import GoalAnalyzer
from app.schemas.response import Complexity


@pytest.fixture
def analyzer() -> GoalAnalyzer:
    return GoalAnalyzer()


class TestDomainDetection:
    """Verify domain detection from user input."""

    def test_web_development_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build a portfolio website using React")
        assert goal.domain == "Web Development"

    def test_mobile_development_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Create a mobile app with Flutter")
        assert goal.domain == "Mobile Development"

    def test_data_science_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build a machine learning model for prediction")
        assert goal.domain == "Data Science"

    def test_content_creation_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Start a YouTube channel for gaming content")
        assert goal.domain == "Content Creation"

    def test_marketing_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Run a digital marketing campaign with SEO")
        assert goal.domain == "Marketing"

    def test_game_development_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Create an indie game using Unity")
        assert goal.domain == "Game Development"

    def test_ecommerce_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Launch an online store with Shopify")
        assert goal.domain == "E-Commerce"

    def test_devops_domain(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Set up a CI/CD pipeline with Docker and Kubernetes")
        assert goal.domain == "DevOps"

    def test_unknown_domain_defaults_to_general(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Organize my kitchen pantry")
        assert goal.domain == "General"


class TestGoalTypeDetection:
    """Verify goal type classification."""

    def test_portfolio_goal_type(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build a portfolio website")
        assert goal.goal_type == "Portfolio Website"

    def test_saas_goal_type(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build a SaaS application")
        assert goal.goal_type == "SaaS Application"

    def test_mvp_goal_type(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Launch an MVP for my startup")
        assert goal.goal_type == "MVP Launch"

    def test_fallback_goal_type(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build something with React")
        assert goal.goal_type in ("Web Application", "Custom Project")


class TestComplexityEstimation:
    """Verify complexity heuristics."""

    def test_simple_goal_is_low(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build a simple portfolio")
        assert goal.complexity == Complexity.LOW

    def test_enterprise_goal_is_high(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Build an enterprise scalable microservices platform")
        assert goal.complexity == Complexity.HIGH

    def test_medium_complexity_default(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("Create a website for my business")
        assert goal.complexity == Complexity.MEDIUM


class TestInputHandling:
    """Verify edge cases in input handling."""

    def test_preserves_original_input(self, analyzer: GoalAnalyzer) -> None:
        raw = "  Build a portfolio website  "
        goal = analyzer.analyze(raw)
        assert goal.user_input == "Build a portfolio website"

    def test_case_insensitive_matching(self, analyzer: GoalAnalyzer) -> None:
        goal = analyzer.analyze("BUILD A REACT WEBSITE")
        assert goal.domain == "Web Development"
