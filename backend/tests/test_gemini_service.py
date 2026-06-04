"""
Tests for the GeminiService high-level integration.

Mocks the GeminiClient to test prompt construction, validation flow,
repair logic, and error handling without real API calls.
"""

import copy
from unittest.mock import MagicMock, patch

import pytest

from app.integrations.exceptions import (
    GeminiAPIError,
    GeminiValidationError,
)
from app.services.gemini_service import GeminiService


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def valid_gemini_response():
    """A fully valid response dict as Gemini would return."""
    return {
        "goal": {
            "user_input": "Build a portfolio website",
            "domain": "Web Development",
            "goal_type": "Portfolio Website",
            "complexity": "Medium",
        },
        "deliverables": [
            {"id": 1, "title": "Design", "description": "Create visual design."},
            {"id": 2, "title": "Development", "description": "Build the site."},
            {"id": 3, "title": "Testing", "description": "Test the site."},
            {"id": 4, "title": "Deployment", "description": "Deploy the site."},
        ],
        "recommended_tools": [
            {"name": "Figma", "category": "Design", "reason": "UI design tool."},
            {"name": "React", "category": "Development", "reason": "UI framework."},
            {"name": "Vercel", "category": "Development", "reason": "Hosting."},
            {"name": "ChatGPT", "category": "AI", "reason": "Code help."},
        ],
        "workflow": [
            {
                "step_number": 1,
                "title": "Plan",
                "tool": "ChatGPT",
                "why": "Planning assistance",
                "what_to_do": "Outline project structure",
                "prompt": "Help me plan a portfolio website",
                "expected_result": "Project outline",
            },
            {
                "step_number": 2,
                "title": "Design",
                "tool": "Figma",
                "why": "Design tool",
                "what_to_do": "Create mockups",
                "prompt": "",
                "expected_result": "Design mockups",
            },
            {
                "step_number": 3,
                "title": "Develop",
                "tool": "React",
                "why": "UI framework",
                "what_to_do": "Build components",
                "prompt": "",
                "expected_result": "Working components",
            },
            {
                "step_number": 4,
                "title": "Deploy",
                "tool": "Vercel",
                "why": "Easy deployment",
                "what_to_do": "Deploy to production",
                "prompt": "",
                "expected_result": "Live website",
            },
        ],
        "alternative_workflows": {
            "fastest": {"summary": "Use a website builder", "tools": ["Wix"]},
            "cheapest": {"summary": "HTML/CSS only", "tools": ["VS Code"]},
            "highest_quality": {
                "summary": "Full custom stack",
                "tools": ["React", "Tailwind"],
            },
            "beginner_friendly": {
                "summary": "No-code platform",
                "tools": ["Squarespace"],
            },
        },
        "knowledge_areas": {
            "high": ["HTML", "CSS", "Git"],
            "medium": ["JavaScript", "React"],
            "low": ["SEO", "DevOps"],
        },
        "estimated_time": "8-12 hours",
    }


# --------------------------------------------------------------------------
# Tests: Successful generation
# --------------------------------------------------------------------------

class TestGeminiServiceSuccess:
    """Tests for successful workflow generation via GeminiService."""

    @patch("app.services.gemini_service.GeminiClient")
    def test_generate_workflow_returns_valid_response(
        self, MockClient, valid_gemini_response
    ):
        """Successful Gemini call should return a valid WorkflowResponse."""
        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        response = service.generate_workflow("Build a portfolio website")

        assert response.goal.user_input == "Build a portfolio website"
        assert response.goal.domain == "Web Development"
        assert len(response.deliverables) == 4
        assert len(response.workflow) == 4
        assert len(response.recommended_tools) == 4
        assert response.estimated_time == "8-12 hours"

    @patch("app.services.gemini_service.GeminiClient")
    def test_user_input_is_injected_into_goal(
        self, MockClient, valid_gemini_response
    ):
        """The service should ensure user_input matches the original request."""
        # Gemini might return a different user_input
        valid_gemini_response["goal"]["user_input"] = "Something else"
        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        response = service.generate_workflow("My actual goal")

        assert response.goal.user_input == "My actual goal"


# --------------------------------------------------------------------------
# Tests: Validation and repair
# --------------------------------------------------------------------------

class TestGeminiServiceValidation:
    """Tests for validation and repair during generation."""

    @patch("app.services.gemini_service.GeminiClient")
    def test_misnumbered_steps_are_repaired(
        self, MockClient, valid_gemini_response
    ):
        """Steps with wrong numbers should be auto-repaired."""
        valid_gemini_response["workflow"][0]["step_number"] = 10
        valid_gemini_response["workflow"][1]["step_number"] = 20
        valid_gemini_response["workflow"][2]["step_number"] = 30
        valid_gemini_response["workflow"][3]["step_number"] = 40

        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        response = service.generate_workflow("Build a website")

        # Steps should be renumbered 1-4
        assert response.workflow[0].step_number == 1
        assert response.workflow[1].step_number == 2
        assert response.workflow[2].step_number == 3
        assert response.workflow[3].step_number == 4

    @patch("app.services.gemini_service.GeminiClient")
    def test_invalid_complexity_is_repaired(
        self, MockClient, valid_gemini_response
    ):
        """Invalid complexity should be defaulted to Medium."""
        valid_gemini_response["goal"]["complexity"] = "Extreme"

        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        response = service.generate_workflow("Build a website")

        assert response.goal.complexity.value == "Medium"


# --------------------------------------------------------------------------
# Tests: Error handling
# --------------------------------------------------------------------------

class TestGeminiServiceErrors:
    """Tests for error handling in GeminiService."""

    @patch("app.services.gemini_service.GeminiClient")
    def test_gemini_api_error_propagates(self, MockClient):
        """GeminiAPIError from the client should propagate up."""
        mock_client = MagicMock()
        mock_client.generate.side_effect = GeminiAPIError("API key invalid")
        MockClient.return_value = mock_client

        service = GeminiService()
        with pytest.raises(GeminiAPIError):
            service.generate_workflow("Build something")

    @patch("app.services.gemini_service.GeminiClient")
    def test_missing_required_keys_raises_validation_error(self, MockClient):
        """Missing required keys should raise GeminiValidationError."""
        mock_client = MagicMock()
        mock_client.generate.return_value = {
            "goal": {"user_input": "test", "domain": "General",
                     "goal_type": "Test", "complexity": "Low"},
            # Missing all other keys
        }
        MockClient.return_value = mock_client

        service = GeminiService()
        with pytest.raises(GeminiValidationError):
            service.generate_workflow("test")


# --------------------------------------------------------------------------
# Tests: Prompt construction
# --------------------------------------------------------------------------

class TestPromptConstruction:
    """Tests for prompt template usage."""

    @patch("app.services.gemini_service.GeminiClient")
    def test_prompt_contains_user_goal(self, MockClient, valid_gemini_response):
        """The prompt sent to Gemini should contain the user's goal."""
        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        service.generate_workflow("Launch a SaaS startup")

        # Check that generate was called with the goal in the prompt
        call_args = mock_client.generate.call_args
        assert "Launch a SaaS startup" in call_args.kwargs["user_prompt"]

    @patch("app.services.gemini_service.GeminiClient")
    def test_system_instruction_is_set(self, MockClient, valid_gemini_response):
        """System instruction should be passed to the client."""
        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        service.generate_workflow("Build a website")

        call_args = mock_client.generate.call_args
        assert "Arkitect" in call_args.kwargs["system_instruction"]

    @patch("app.services.gemini_service.GeminiClient")
    def test_response_schema_is_passed(self, MockClient, valid_gemini_response):
        """Response schema should be passed to constrain output structure."""
        mock_client = MagicMock()
        mock_client.generate.return_value = copy.deepcopy(valid_gemini_response)
        MockClient.return_value = mock_client

        service = GeminiService()
        service.generate_workflow("Build a website")

        call_args = mock_client.generate.call_args
        assert call_args.kwargs["response_schema"] is not None
        assert isinstance(call_args.kwargs["response_schema"], dict)
