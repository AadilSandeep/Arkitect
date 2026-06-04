"""Tests for the TimeEstimator service."""

import pytest

from app.services.time_estimator import TimeEstimator
from app.schemas.response import Complexity, Deliverable, Goal


@pytest.fixture
def estimator() -> TimeEstimator:
    return TimeEstimator()


def _make_goal(complexity: str = "Medium") -> Goal:
    return Goal(
        user_input="Test goal",
        domain="Web Development",
        goal_type="Test Project",
        complexity=Complexity(complexity),
    )


def _make_deliverables(count: int) -> list[Deliverable]:
    return [
        Deliverable(id=i + 1, title=f"Deliverable {i + 1}", description="Test.")
        for i in range(count)
    ]


class TestTimeEstimation:
    """Verify time estimation behavior."""

    def test_returns_nonempty_string(self, estimator: TimeEstimator) -> None:
        result = estimator.estimate(_make_goal(), _make_deliverables(3))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_low_few_is_shortest(self, estimator: TimeEstimator) -> None:
        result = estimator.estimate(_make_goal("Low"), _make_deliverables(2))
        assert result == "2-4 hours"

    def test_high_many_is_longest(self, estimator: TimeEstimator) -> None:
        result = estimator.estimate(_make_goal("High"), _make_deliverables(8))
        assert result == "1-3 weeks"

    def test_medium_moderate(self, estimator: TimeEstimator) -> None:
        result = estimator.estimate(_make_goal("Medium"), _make_deliverables(5))
        assert result == "1-3 days"

    def test_bucket_boundaries(self, estimator: TimeEstimator) -> None:
        # 3 deliverables → "few"
        assert TimeEstimator._get_bucket(3) == "few"
        # 4 deliverables → "moderate"
        assert TimeEstimator._get_bucket(4) == "moderate"
        # 6 deliverables → "moderate"
        assert TimeEstimator._get_bucket(6) == "moderate"
        # 7 deliverables → "many"
        assert TimeEstimator._get_bucket(7) == "many"

    def test_higher_complexity_longer_time(self, estimator: TimeEstimator) -> None:
        deliverables = _make_deliverables(5)
        low = estimator.estimate(_make_goal("Low"), deliverables)
        high = estimator.estimate(_make_goal("High"), deliverables)
        # Low should be "4-8 hours", High should be "3-7 days"
        assert low != high
