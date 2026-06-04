"""
Deliverables Detection Service.

Identifies major deliverables required to achieve a goal based on
domain-specific templates in the knowledge base.
"""

from app.schemas.response import Complexity, Deliverable, Goal
from app.services.knowledge_base import DOMAIN_DELIVERABLES


class DeliverableDetector:
    """
    Deterministic deliverable detection engine.

    Looks up domain-specific deliverables and filters based on
    goal complexity to return an appropriate number of deliverables.
    """

    # Bounds per complexity level
    _LIMITS: dict[Complexity, tuple[int, int]] = {
        Complexity.LOW: (3, 5),
        Complexity.MEDIUM: (4, 6),
        Complexity.HIGH: (5, 8),
    }

    def detect(self, goal: Goal) -> list[Deliverable]:
        """
        Detect deliverables for a given goal.

        Args:
            goal: Analyzed goal with domain and complexity.

        Returns:
            Ordered list of Deliverable objects with sequential IDs.
        """
        domain = goal.domain
        complexity = goal.complexity

        # Fetch domain-specific deliverable templates
        templates = DOMAIN_DELIVERABLES.get(domain, DOMAIN_DELIVERABLES["General"])

        # Determine how many to return based on complexity
        min_count, max_count = self._LIMITS.get(complexity, (3, 6))

        # For lower complexity, take fewer deliverables (from the front — they
        # are ordered by priority in the knowledge base).
        selected = templates[:max_count]

        # Ensure minimum count (should always pass with our data, but be safe)
        if len(selected) < min_count:
            # Pad from General fallback if domain-specific data is sparse
            fallback = DOMAIN_DELIVERABLES["General"]
            for item in fallback:
                if len(selected) >= min_count:
                    break
                if item not in selected:
                    selected.append(item)

        # Build Pydantic models with sequential IDs
        return [
            Deliverable(
                id=idx + 1,
                title=template["title"],
                description=template["description"],
            )
            for idx, template in enumerate(selected)
        ]
