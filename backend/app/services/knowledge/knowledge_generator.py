"""
Knowledge Areas Generation Service.

Identifies knowledge domains relevant to a goal, grouped by
importance level (high, medium, low).
"""

from app.schemas.response import Goal, KnowledgeAreas
from app.services.knowledge_base import DOMAIN_KNOWLEDGE


class KnowledgeGenerator:
    """
    Deterministic knowledge area engine.

    Looks up domain-specific knowledge areas categorized by
    priority level.
    """

    def generate(self, goal: Goal) -> KnowledgeAreas:
        """
        Generate knowledge area recommendations for the given goal.

        Args:
            goal: Analyzed goal with domain info.

        Returns:
            KnowledgeAreas with high, medium, and low priority lists.
        """
        domain = goal.domain
        knowledge = DOMAIN_KNOWLEDGE.get(
            domain, DOMAIN_KNOWLEDGE["General"]
        )

        return KnowledgeAreas(
            high=list(knowledge.get("high", [])),
            medium=list(knowledge.get("medium", [])),
            low=list(knowledge.get("low", [])),
        )
