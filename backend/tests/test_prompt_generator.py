"""Tests for the PromptGenerator service."""

import pytest

from app.services.prompts.prompt_generator import PromptGenerator
from app.schemas.response import Complexity, Goal, WorkflowStep


@pytest.fixture
def generator() -> PromptGenerator:
    return PromptGenerator()


def _make_goal() -> Goal:
    return Goal(
        user_input="Build a portfolio website",
        domain="Web Development",
        goal_type="Portfolio Website",
        complexity=Complexity.MEDIUM,
    )


def _make_steps() -> list[WorkflowStep]:
    return [
        WorkflowStep(
            step_number=1,
            title="Research Competitors",
            tool="ChatGPT",
            why="Fast research.",
            what_to_do="Research competing portfolio sites.",
            prompt="",
            expected_result="A list of competitor insights.",
        ),
        WorkflowStep(
            step_number=2,
            title="Design UI",
            tool="Figma",
            why="Industry-standard design tool.",
            what_to_do="Create wireframes and mockups.",
            prompt="",
            expected_result="Complete UI mockups.",
        ),
        WorkflowStep(
            step_number=3,
            title="Generate Content",
            tool="Gemini",
            why="AI content generation.",
            what_to_do="Write project descriptions for the portfolio.",
            prompt="",
            expected_result="Written descriptions for each project.",
        ),
    ]


class TestPromptGeneration:
    """Verify prompt generation behavior."""

    def test_ai_tools_get_prompts(self, generator: PromptGenerator) -> None:
        steps = generator.generate(_make_steps(), _make_goal())
        # ChatGPT step should have a prompt
        assert steps[0].prompt != ""
        # Gemini step should have a prompt
        assert steps[2].prompt != ""

    def test_non_ai_tools_get_empty_prompt(self, generator: PromptGenerator) -> None:
        steps = generator.generate(_make_steps(), _make_goal())
        # Figma step should NOT have a prompt
        assert steps[1].prompt == ""

    def test_prompt_contains_goal_context(self, generator: PromptGenerator) -> None:
        steps = generator.generate(_make_steps(), _make_goal())
        prompt = steps[0].prompt
        assert "Portfolio Website" in prompt
        assert "Web Development" in prompt

    def test_prompt_contains_task_instruction(self, generator: PromptGenerator) -> None:
        steps = generator.generate(_make_steps(), _make_goal())
        prompt = steps[0].prompt
        assert "Research competing portfolio sites" in prompt

    def test_preserves_step_numbers(self, generator: PromptGenerator) -> None:
        steps = generator.generate(_make_steps(), _make_goal())
        numbers = [s.step_number for s in steps]
        assert numbers == [1, 2, 3]

    def test_preserves_other_fields(self, generator: PromptGenerator) -> None:
        original = _make_steps()
        enriched = generator.generate(original, _make_goal())
        for orig, enr in zip(original, enriched):
            assert orig.title == enr.title
            assert orig.tool == enr.tool
            assert orig.why == enr.why
            assert orig.what_to_do == enr.what_to_do
            assert orig.expected_result == enr.expected_result
