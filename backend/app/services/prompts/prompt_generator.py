"""
Prompt Generation Service.

Enriches workflow steps with context-aware AI prompts for steps
that use AI tools (ChatGPT, Gemini, Claude, etc.).
"""

from app.schemas.response import Goal, WorkflowStep


class PromptGenerator:
    """
    Deterministic prompt generation engine.

    Iterates through workflow steps, identifies those using AI tools,
    and generates a ready-to-use prompt string based on the goal context
    and step instructions.
    """

    # Tools that accept natural-language prompts
    _AI_TOOLS: set[str] = {
        "ChatGPT", "Gemini", "Claude", "Copilot", "Perplexity",
        "Jasper", "Notion AI", "Bard",
    }

    def generate(
        self,
        workflow_steps: list[WorkflowStep],
        goal: Goal,
    ) -> list[WorkflowStep]:
        """
        Enrich workflow steps with AI prompts where applicable.

        For steps using an AI tool, generates a context-aware prompt.
        For steps using non-AI tools, the prompt remains an empty string.

        Args:
            workflow_steps: Existing workflow steps (prompt field is empty).
            goal: Analyzed goal for context.

        Returns:
            New list of WorkflowStep objects with prompts filled in.
        """
        enriched: list[WorkflowStep] = []

        for step in workflow_steps:
            if step.tool in self._AI_TOOLS:
                prompt = self._build_prompt(step, goal)
            else:
                prompt = ""

            # Create a new step with the prompt filled in
            enriched.append(
                WorkflowStep(
                    step_number=step.step_number,
                    title=step.title,
                    tool=step.tool,
                    why=step.why,
                    what_to_do=step.what_to_do,
                    prompt=prompt,
                    expected_result=step.expected_result,
                )
            )

        return enriched

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, step: WorkflowStep, goal: Goal) -> str:
        """
        Build a context-aware prompt string for an AI-tool step.

        Template structure:
        1. Role / context
        2. User goal
        3. Specific task
        4. Expected output format
        """
        lines = [
            f"You are an expert assistant helping with a {goal.goal_type} project "
            f"in the {goal.domain} domain.",
            "",
            f"The user's goal is: \"{goal.user_input}\"",
            "",
            f"Your task: {step.what_to_do}",
            "",
            f"Please provide: {step.expected_result}",
            "",
            "Be specific, actionable, and well-structured in your response. "
            "Use bullet points or numbered lists where appropriate.",
        ]
        return "\n".join(lines)
