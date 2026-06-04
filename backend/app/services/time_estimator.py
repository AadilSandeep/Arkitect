"""
Time Estimation Service.

Estimates the total completion time for a goal based on its
complexity and the number of deliverables.
"""

from app.schemas.response import Deliverable, Goal
from app.services.knowledge_base import TIME_ESTIMATES


class TimeEstimator:
    """
    Deterministic time estimation engine.

    Maps (complexity, deliverable_count_bucket) to a human-readable
    time estimate string using the knowledge base lookup table.
    """

    def estimate(self, goal: Goal, deliverables: list[Deliverable]) -> str:
        """
        Estimate completion time for a goal.

        Args:
            goal: Analyzed goal with complexity info.
            deliverables: Detected deliverables (count determines bucket).

        Returns:
            Human-readable time estimate string (e.g., "8-12 hours").
        """
        complexity_key = goal.complexity.value  # "Low", "Medium", or "High"
        bucket = self._get_bucket(len(deliverables))

        time_map = TIME_ESTIMATES.get(complexity_key, TIME_ESTIMATES["Medium"])
        return time_map.get(bucket, "1-3 days")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_bucket(count: int) -> str:
        """
        Map a deliverable count to a bucket key.

        - 1–3  → "few"
        - 4–6  → "moderate"
        - 7+   → "many"
        """
        if count <= 3:
            return "few"
        if count <= 6:
            return "moderate"
        return "many"
