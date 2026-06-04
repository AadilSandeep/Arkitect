"""
Tool Recommendation Service.

Recommends the best combination of tools for achieving a goal,
based on domain-specific catalogs in the knowledge base.
"""

from app.schemas.response import Deliverable, Goal, RecommendedTool, ToolCategory
from app.services.knowledge_base import DOMAIN_TOOLS


class ToolRecommender:
    """
    Deterministic tool recommendation engine.

    Retrieves domain-specific tools, cross-references with deliverables
    for contextual relevance, deduplicates, and returns a curated list.
    """

    # Deliverable-title keywords → extra tools to inject
    _DELIVERABLE_TOOL_MAP: dict[str, list[dict[str, str]]] = {
        "authentication": [
            {"name": "Auth0", "category": "Development", "reason": "Managed authentication and authorization service."},
        ],
        "payment": [
            {"name": "Stripe", "category": "Development", "reason": "Industry-leading payment processing API."},
        ],
        "database": [
            {"name": "PostgreSQL", "category": "Development", "reason": "Robust open-source relational database."},
        ],
        "testing": [
            {"name": "Jest", "category": "Development", "reason": "JavaScript testing framework for unit and integration tests."},
        ],
        "deployment": [
            {"name": "Vercel", "category": "Development", "reason": "Zero-config deployment for frontend applications."},
        ],
        "design": [
            {"name": "Figma", "category": "Design", "reason": "Collaborative interface design and prototyping tool."},
        ],
        "analytics": [
            {"name": "Google Analytics", "category": "Marketing", "reason": "Track user behavior and measure performance."},
        ],
        "seo": [
            {"name": "SEMrush", "category": "Marketing", "reason": "SEO research, keyword tracking, and competitor analysis."},
        ],
    }

    def recommend(
        self,
        goal: Goal,
        deliverables: list[Deliverable],
    ) -> list[RecommendedTool]:
        """
        Recommend tools for a goal and its deliverables.

        Args:
            goal: Analyzed goal with domain info.
            deliverables: Detected deliverables for cross-referencing.

        Returns:
            Deduplicated list of 4–10 RecommendedTool objects.
        """
        domain = goal.domain

        # Start with domain-level tools
        raw_tools = list(DOMAIN_TOOLS.get(domain, DOMAIN_TOOLS["General"]))

        # Inject deliverable-specific tools
        for deliverable in deliverables:
            title_lower = deliverable.title.lower()
            for keyword, extras in self._DELIVERABLE_TOOL_MAP.items():
                if keyword in title_lower:
                    raw_tools.extend(extras)

        # Deduplicate by tool name (keep first occurrence)
        seen: set[str] = set()
        unique: list[dict[str, str]] = []
        for tool in raw_tools:
            name = tool["name"]
            if name not in seen:
                seen.add(name)
                unique.append(tool)

        # Clamp to 4–10
        selected = unique[:10]
        if len(selected) < 4:
            # Pad from General if needed
            for fallback in DOMAIN_TOOLS["General"]:
                if len(selected) >= 4:
                    break
                if fallback["name"] not in seen:
                    seen.add(fallback["name"])
                    selected.append(fallback)

        return [
            RecommendedTool(
                name=tool["name"],
                category=ToolCategory(tool["category"]),
                reason=tool["reason"],
            )
            for tool in selected
        ]
