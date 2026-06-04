"""Tests for the WorkflowOrchestrator end-to-end pipeline."""

from unittest.mock import MagicMock, patch

import pytest

from app.integrations.exceptions import GeminiAPIError
from app.services.orchestrator import WorkflowOrchestrator
from app.schemas.response import WorkflowRequest, WorkflowResponse


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def deterministic_orchestrator() -> WorkflowOrchestrator:
    """Orchestrator with Gemini disabled (deterministic only)."""
    with patch("app.services.orchestrator.settings") as mock_settings:
        mock_settings.GEMINI_ENABLED = False
        mock_settings.GEMINI_API_KEY = ""
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"
        yield WorkflowOrchestrator()


# --------------------------------------------------------------------------
# Tests: Deterministic pipeline (existing behavior preserved)
# --------------------------------------------------------------------------

class TestDeterministicPipeline:
    """Verify the deterministic orchestration pipeline (Gemini disabled)."""

    def test_produces_valid_response(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert isinstance(response, WorkflowResponse)

    def test_goal_fields_populated(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert response.goal.user_input == "Build a portfolio website"
        assert response.goal.domain != ""
        assert response.goal.goal_type != ""

    def test_deliverables_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert len(response.deliverables) >= 3

    def test_tools_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert len(response.recommended_tools) >= 4

    def test_workflow_steps_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert len(response.workflow) >= 4

    def test_workflow_steps_have_prompts(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        # At least one step should have an AI prompt
        has_prompt = any(step.prompt != "" for step in response.workflow)
        assert has_prompt, "No workflow steps have AI prompts"

    def test_alternatives_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert response.alternative_workflows.fastest.summary
        assert response.alternative_workflows.cheapest.summary
        assert response.alternative_workflows.highest_quality.summary
        assert response.alternative_workflows.beginner_friendly.summary

    def test_knowledge_areas_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert len(response.knowledge_areas.high) > 0

    def test_estimated_time_present(self, deterministic_orchestrator) -> None:
        request = WorkflowRequest(goal="Build a portfolio website")
        response = deterministic_orchestrator.process(request)
        assert response.estimated_time != ""

    def test_no_null_fields(self, deterministic_orchestrator) -> None:
        """Verify system contract rule: no null values."""
        request = WorkflowRequest(goal="Launch a SaaS startup")
        response = deterministic_orchestrator.process(request)
        data = response.model_dump()
        self._check_no_nulls(data, "root")

    def _check_no_nulls(self, obj: object, path: str) -> None:
        if obj is None:
            raise AssertionError(f"Null value found at {path}")
        if isinstance(obj, dict):
            for key, value in obj.items():
                self._check_no_nulls(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                self._check_no_nulls(item, f"{path}[{idx}]")

    def test_different_domains(self, deterministic_orchestrator) -> None:
        """Test that different goal strings produce domain-appropriate results."""
        goals = [
            ("Build a mobile app with Flutter", "Mobile Development"),
            ("Train a machine learning model", "Data Science"),
            ("Start a YouTube channel", "Content Creation"),
            ("Set up CI/CD with Docker", "DevOps"),
        ]
        for goal_text, expected_domain in goals:
            request = WorkflowRequest(goal=goal_text)
            response = deterministic_orchestrator.process(request)
            assert response.goal.domain == expected_domain, (
                f"Goal '{goal_text}' expected domain '{expected_domain}', "
                f"got '{response.goal.domain}'"
            )


# --------------------------------------------------------------------------
# Tests: Gemini integration in orchestrator
# --------------------------------------------------------------------------

class TestGeminiIntegration:
    """Test Gemini-first routing and fallback behavior."""

    @patch("app.services.orchestrator.settings")
    def test_gemini_disabled_uses_deterministic(self, mock_settings) -> None:
        """When GEMINI_ENABLED=False, Gemini should not be attempted."""
        mock_settings.GEMINI_ENABLED = False
        mock_settings.GEMINI_API_KEY = ""
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"

        orchestrator = WorkflowOrchestrator()
        assert orchestrator._gemini_service is None

        request = WorkflowRequest(goal="Build a website")
        response = orchestrator.process(request)
        assert isinstance(response, WorkflowResponse)

    @patch("app.services.orchestrator.settings")
    def test_empty_api_key_disables_gemini(self, mock_settings) -> None:
        """Empty GEMINI_API_KEY should disable Gemini even if enabled."""
        mock_settings.GEMINI_ENABLED = True
        mock_settings.GEMINI_API_KEY = ""
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"

        orchestrator = WorkflowOrchestrator()
        assert orchestrator._gemini_service is None

    @patch("app.services.orchestrator.settings")
    def test_gemini_failure_falls_back_to_deterministic(self, mock_settings) -> None:
        """When Gemini fails, orchestrator should fall back to deterministic."""
        mock_settings.GEMINI_ENABLED = True
        mock_settings.GEMINI_API_KEY = "test-key"
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"

        orchestrator = WorkflowOrchestrator()

        # Mock the Gemini service to fail
        mock_gemini = MagicMock()
        mock_gemini.generate_workflow.side_effect = GeminiAPIError("Test failure")
        orchestrator._gemini_service = mock_gemini

        request = WorkflowRequest(goal="Build a portfolio website")
        response = orchestrator.process(request)

        # Should still return a valid response from deterministic fallback
        assert isinstance(response, WorkflowResponse)
        assert response.goal.user_input == "Build a portfolio website"
        assert len(response.deliverables) >= 3

    @patch("app.services.orchestrator.settings")
    def test_gemini_success_returns_ai_response(self, mock_settings) -> None:
        """When Gemini succeeds, its response should be returned."""
        mock_settings.GEMINI_ENABLED = True
        mock_settings.GEMINI_API_KEY = "test-key"
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"

        orchestrator = WorkflowOrchestrator()

        # Create a mock WorkflowResponse
        mock_response = MagicMock(spec=WorkflowResponse)
        mock_gemini = MagicMock()
        mock_gemini.generate_workflow.return_value = mock_response
        orchestrator._gemini_service = mock_gemini

        request = WorkflowRequest(goal="Build a website")
        response = orchestrator.process(request)

        # Should return the Gemini response, not the deterministic one
        assert response is mock_response
        mock_gemini.generate_workflow.assert_called_once_with("Build a website")

    @patch("app.services.orchestrator.settings")
    def test_unexpected_exception_falls_back(self, mock_settings) -> None:
        """Even unexpected exceptions should trigger fallback, not crash."""
        mock_settings.GEMINI_ENABLED = True
        mock_settings.GEMINI_API_KEY = "test-key"
        mock_settings.GEMINI_MODEL = "gemini-2.0-flash"

        orchestrator = WorkflowOrchestrator()

        mock_gemini = MagicMock()
        mock_gemini.generate_workflow.side_effect = RuntimeError("Completely unexpected")
        orchestrator._gemini_service = mock_gemini

        request = WorkflowRequest(goal="Build a website")
        response = orchestrator.process(request)

        # Should fallback gracefully
        assert isinstance(response, WorkflowResponse)

