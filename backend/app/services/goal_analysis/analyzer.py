"""
Goal Analysis Service.

Analyzes user input to extract domain, goal type, and complexity.
Uses keyword matching against the domain knowledge base.
"""

from app.schemas.response import Complexity, Goal
from app.services.knowledge_base import (
    DOMAIN_KEYWORDS,
    GOAL_TYPE_PATTERNS,
    HIGH_COMPLEXITY_KEYWORDS,
    LOW_COMPLEXITY_KEYWORDS,
)


class GoalAnalyzer:
    """
    Deterministic goal analysis engine.

    Tokenizes user input, matches keywords against domain catalogs,
    detects goal type via pattern matching, and estimates complexity
    using heuristic rules.
    """

    def analyze(self, user_input: str) -> Goal:
        """
        Analyze a natural-language goal and return a structured Goal object.

        Args:
            user_input: Raw goal string from the user.

        Returns:
            Goal with populated domain, goal_type, and complexity fields.
        """
        normalized = user_input.lower().strip()
        domain = self._detect_domain(normalized)
        goal_type = self._detect_goal_type(normalized, domain)
        complexity = self._estimate_complexity(normalized)

        return Goal(
            user_input=user_input.strip(),
            domain=domain,
            goal_type=goal_type,
            complexity=complexity,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _detect_domain(self, text: str) -> str:
        """
        Score each domain by counting keyword hits in the input text.
        Returns the domain with the highest score, or 'General' on tie/miss.
        """
        scores: dict[str, int] = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[domain] = score

        if not scores:
            return "General"

        return max(scores, key=scores.get)  # type: ignore[arg-type]

    def _detect_goal_type(self, text: str, domain: str) -> str:
        """
        Match input text against goal-type patterns.
        Returns the first matching goal type, or a domain-based default.
        """
        for goal_type, patterns in GOAL_TYPE_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                return goal_type

        # Domain-based fallback
        domain_defaults: dict[str, str] = {
            "Web Development": "Web Application",
            "Mobile Development": "Mobile Application",
            "Data Science": "Data Analysis Project",
            "Content Creation": "Content Project",
            "Marketing": "Marketing Campaign",
            "Game Development": "Game Project",
            "E-Commerce": "E-Commerce Store",
            "DevOps": "Infrastructure Project",
        }
        return domain_defaults.get(domain, "Custom Project")

    def _estimate_complexity(self, text: str) -> Complexity:
        """
        Estimate complexity based on keyword signals in the input.

        Checks for high-complexity and low-complexity keyword hits.
        If neither dominates, defaults to Medium.
        """
        high_hits = sum(1 for kw in HIGH_COMPLEXITY_KEYWORDS if kw in text)
        low_hits = sum(1 for kw in LOW_COMPLEXITY_KEYWORDS if kw in text)

        if high_hits > low_hits:
            return Complexity.HIGH
        if low_hits > high_hits:
            return Complexity.LOW
        # Longer inputs tend to describe more complex goals
        word_count = len(text.split())
        if word_count >= 20:
            return Complexity.HIGH
        if word_count <= 5:
            return Complexity.LOW
        return Complexity.MEDIUM
