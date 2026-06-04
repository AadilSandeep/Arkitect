"""
Alternative Workflow Generation Service.

Generates four alternative approaches (fastest, cheapest, highest quality,
beginner friendly) for achieving a goal, using domain-specific templates.
"""

from app.schemas.response import AlternativeWorkflow, AlternativeWorkflows, Goal
from app.services.knowledge_base import DOMAIN_ALTERNATIVES


class AlternativeGenerator:
    """
    Deterministic alternative workflow engine.

    Looks up domain-specific alternative strategies and returns
    structured AlternativeWorkflows with four strategies.
    """

    def generate(self, goal: Goal) -> AlternativeWorkflows:
        """
        Generate alternative workflow strategies for the given goal.

        Args:
            goal: Analyzed goal with domain info.

        Returns:
            AlternativeWorkflows containing four strategies.
        """
        domain = goal.domain
        alternatives = DOMAIN_ALTERNATIVES.get(
            domain, DOMAIN_ALTERNATIVES["General"]
        )

        return AlternativeWorkflows(
            fastest=AlternativeWorkflow(
                summary=alternatives["fastest"]["summary"],
                tools=list(alternatives["fastest"]["tools"]),
            ),
            cheapest=AlternativeWorkflow(
                summary=alternatives["cheapest"]["summary"],
                tools=list(alternatives["cheapest"]["tools"]),
            ),
            highest_quality=AlternativeWorkflow(
                summary=alternatives["highest_quality"]["summary"],
                tools=list(alternatives["highest_quality"]["tools"]),
            ),
            beginner_friendly=AlternativeWorkflow(
                summary=alternatives["beginner_friendly"]["summary"],
                tools=list(alternatives["beginner_friendly"]["tools"]),
            ),
        )
