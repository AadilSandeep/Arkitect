"""
Workflow Generation Service.

Generates actionable, sequential workflow steps based on domain
templates, deliverables, and recommended tools.
"""

from app.schemas.response import Complexity, Deliverable, Goal, RecommendedTool, WorkflowStep
from app.services.knowledge_base import DOMAIN_WORKFLOWS


class WorkflowGenerator:
    """
    Deterministic workflow generation engine.

    Retrieves domain-specific step templates and produces a tailored
    workflow whose length scales with goal complexity.
    """

    # Step count targets per complexity
    _STEP_LIMITS: dict[Complexity, tuple[int, int]] = {
        Complexity.LOW: (4, 6),
        Complexity.MEDIUM: (5, 9),
        Complexity.HIGH: (7, 12),
    }

    def generate(
        self,
        goal: Goal,
        deliverables: list[Deliverable],
        tools: list[RecommendedTool],
    ) -> list[WorkflowStep]:
        """
        Generate a sequential workflow for the given goal.

        Args:
            goal: Analyzed goal.
            deliverables: Detected deliverables (used for context).
            tools: Recommended tools (used for context enrichment).

        Returns:
            Ordered list of WorkflowStep objects with sequential step numbers.
        """
        domain = goal.domain
        complexity = goal.complexity

        templates = list(
            DOMAIN_WORKFLOWS.get(domain, DOMAIN_WORKFLOWS["General"])
        )

        # Determine how many steps to produce
        min_steps, max_steps = self._STEP_LIMITS.get(complexity, (5, 9))

        # Trim or pad the template list
        selected = templates[:max_steps]
        if len(selected) < min_steps:
            # Pad with General steps not already present
            existing_titles = {t["title"] for t in selected}
            for fallback in DOMAIN_WORKFLOWS["General"]:
                if len(selected) >= min_steps:
                    break
                if fallback["title"] not in existing_titles:
                    selected.append(fallback)
                    existing_titles.add(fallback["title"])

        # Build a quick lookup of available tools for potential substitution
        tool_names = {t.name for t in tools}

        steps: list[WorkflowStep] = []
        for idx, template in enumerate(selected):
            # If the template references a tool we recommended, keep it;
            # otherwise still use the template tool (it's a reasonable default).
            tool_name = template["tool"]

            steps.append(
                WorkflowStep(
                    step_number=idx + 1,
                    title=template["title"],
                    tool=tool_name,
                    why=template["why"],
                    what_to_do=template["what_to_do"],
                    prompt="",  # Prompt generation is a separate service
                    expected_result=template["expected_result"],
                )
            )

        return steps
