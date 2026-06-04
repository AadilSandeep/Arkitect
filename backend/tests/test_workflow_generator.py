"""Tests for the WorkflowGenerator service."""

import pytest

from app.services.workflow.generator import WorkflowGenerator
from app.schemas.response import Complexity, Deliverable, Goal, RecommendedTool, ToolCategory


@pytest.fixture
def generator() -> WorkflowGenerator:
    return WorkflowGenerator()


def _make_goal(domain: str = "Web Development", complexity: str = "Medium") -> Goal:
    return Goal(
        user_input="Test goal",
        domain=domain,
        goal_type="Test Project",
        complexity=Complexity(complexity),
    )


def _make_deliverables() -> list[Deliverable]:
    return [
        Deliverable(id=1, title="Frontend", description="Build UI."),
        Deliverable(id=2, title="Backend", description="Build API."),
    ]


def _make_tools() -> list[RecommendedTool]:
    return [
        RecommendedTool(name="React", category=ToolCategory.DEVELOPMENT, reason="UI framework."),
        RecommendedTool(name="Node.js", category=ToolCategory.DEVELOPMENT, reason="Backend runtime."),
    ]


class TestWorkflowGeneration:
    """Verify workflow generation behavior."""

    def test_generates_steps(self, generator: WorkflowGenerator) -> None:
        steps = generator.generate(_make_goal(), _make_deliverables(), _make_tools())
        assert len(steps) >= 4

    def test_sequential_step_numbers(self, generator: WorkflowGenerator) -> None:
        steps = generator.generate(_make_goal(), _make_deliverables(), _make_tools())
        numbers = [s.step_number for s in steps]
        assert numbers == list(range(1, len(numbers) + 1))

    def test_low_complexity_fewer_steps(self, generator: WorkflowGenerator) -> None:
        low = generator.generate(_make_goal(complexity="Low"), _make_deliverables(), _make_tools())
        high = generator.generate(_make_goal(complexity="High"), _make_deliverables(), _make_tools())
        assert len(low) <= len(high)

    def test_steps_have_all_fields(self, generator: WorkflowGenerator) -> None:
        steps = generator.generate(_make_goal(), _make_deliverables(), _make_tools())
        for step in steps:
            assert step.title
            assert step.tool
            assert step.why
            assert step.what_to_do
            assert step.expected_result

    def test_prompts_are_empty_before_enrichment(self, generator: WorkflowGenerator) -> None:
        steps = generator.generate(_make_goal(), _make_deliverables(), _make_tools())
        for step in steps:
            assert step.prompt == ""

    def test_all_domains_produce_steps(self, generator: WorkflowGenerator) -> None:
        domains = [
            "Web Development", "Mobile Development", "Data Science",
            "Content Creation", "Marketing", "Game Development",
            "E-Commerce", "DevOps", "General",
        ]
        for domain in domains:
            steps = generator.generate(_make_goal(domain), _make_deliverables(), _make_tools())
            assert len(steps) >= 4, f"Domain {domain} produced too few steps"
