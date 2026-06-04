"""Tests for the DeliverableDetector service."""

import pytest

from app.services.deliverables.detector import DeliverableDetector
from app.schemas.response import Complexity, Goal


@pytest.fixture
def detector() -> DeliverableDetector:
    return DeliverableDetector()


def _make_goal(domain: str = "Web Development", complexity: str = "Medium") -> Goal:
    return Goal(
        user_input="Test goal",
        domain=domain,
        goal_type="Test Project",
        complexity=Complexity(complexity),
    )


class TestDeliverableDetection:
    """Verify deliverable detection behavior."""

    def test_returns_deliverables_for_known_domain(self, detector: DeliverableDetector) -> None:
        deliverables = detector.detect(_make_goal("Web Development"))
        assert len(deliverables) >= 3

    def test_low_complexity_returns_fewer(self, detector: DeliverableDetector) -> None:
        low = detector.detect(_make_goal(complexity="Low"))
        high = detector.detect(_make_goal(complexity="High"))
        assert len(low) <= len(high)

    def test_sequential_ids(self, detector: DeliverableDetector) -> None:
        deliverables = detector.detect(_make_goal())
        ids = [d.id for d in deliverables]
        assert ids == list(range(1, len(ids) + 1))

    def test_deliverables_have_titles_and_descriptions(self, detector: DeliverableDetector) -> None:
        deliverables = detector.detect(_make_goal())
        for d in deliverables:
            assert d.title
            assert d.description

    def test_fallback_for_unknown_domain(self, detector: DeliverableDetector) -> None:
        deliverables = detector.detect(_make_goal("Underwater Basket Weaving"))
        assert len(deliverables) >= 3

    def test_all_domains_produce_deliverables(self, detector: DeliverableDetector) -> None:
        domains = [
            "Web Development", "Mobile Development", "Data Science",
            "Content Creation", "Marketing", "Game Development",
            "E-Commerce", "DevOps", "General",
        ]
        for domain in domains:
            deliverables = detector.detect(_make_goal(domain))
            assert len(deliverables) >= 3, f"Domain {domain} produced too few deliverables"

    def test_high_complexity_cap(self, detector: DeliverableDetector) -> None:
        deliverables = detector.detect(_make_goal(complexity="High"))
        assert len(deliverables) <= 8
