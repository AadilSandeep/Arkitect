"""
Tests for the Gemini transport client.

Mocks the google-genai SDK to test retry logic, exception mapping,
JSON parsing, and error handling without making real API calls.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from app.integrations.exceptions import (
    GeminiAPIError,
    GeminiRateLimitError,
    GeminiTimeoutError,
)
from app.integrations.gemini_client import GeminiClient


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def mock_settings():
    """Patch settings with test values."""
    with patch("app.integrations.gemini_client.settings") as mock:
        mock.GEMINI_API_KEY = "test-key"
        mock.GEMINI_MODEL = "gemini-2.0-flash"
        mock.GEMINI_MAX_RETRIES = 2
        mock.GEMINI_TIMEOUT = 5
        mock.GEMINI_TEMPERATURE = 0.7
        mock.GEMINI_MAX_OUTPUT_TOKENS = 4096
        yield mock


@pytest.fixture
def sample_response_data():
    """Minimal valid response data."""
    return {
        "goal": {
            "user_input": "Build a website",
            "domain": "Web Development",
            "goal_type": "Website",
            "complexity": "Medium",
        },
        "deliverables": [
            {"id": 1, "title": "Design", "description": "Create design"},
            {"id": 2, "title": "Development", "description": "Build site"},
            {"id": 3, "title": "Deployment", "description": "Deploy site"},
        ],
        "recommended_tools": [
            {"name": "Figma", "category": "Design", "reason": "Design tool"},
            {"name": "React", "category": "Development", "reason": "UI framework"},
            {"name": "Vercel", "category": "Development", "reason": "Deployment"},
            {"name": "ChatGPT", "category": "AI", "reason": "Code assistance"},
        ],
        "workflow": [
            {
                "step_number": 1,
                "title": "Design",
                "tool": "Figma",
                "why": "Design tool",
                "what_to_do": "Create wireframes",
                "prompt": "",
                "expected_result": "Wireframes",
            },
            {
                "step_number": 2,
                "title": "Develop",
                "tool": "React",
                "why": "UI framework",
                "what_to_do": "Build components",
                "prompt": "",
                "expected_result": "Components",
            },
            {
                "step_number": 3,
                "title": "Test",
                "tool": "Jest",
                "why": "Testing",
                "what_to_do": "Write tests",
                "prompt": "",
                "expected_result": "Test suite",
            },
            {
                "step_number": 4,
                "title": "Deploy",
                "tool": "Vercel",
                "why": "Hosting",
                "what_to_do": "Deploy app",
                "prompt": "",
                "expected_result": "Live site",
            },
        ],
        "alternative_workflows": {
            "fastest": {"summary": "Use a builder", "tools": ["Wix"]},
            "cheapest": {"summary": "Free tools only", "tools": ["HTML"]},
            "highest_quality": {"summary": "Full stack", "tools": ["React", "Node"]},
            "beginner_friendly": {"summary": "No-code", "tools": ["Squarespace"]},
        },
        "knowledge_areas": {
            "high": ["HTML", "CSS"],
            "medium": ["JavaScript"],
            "low": ["SEO"],
        },
        "estimated_time": "8-12 hours",
    }


def _make_mock_response(data: dict) -> MagicMock:
    """Create a mock Gemini response object."""
    response = MagicMock()
    response.text = json.dumps(data)
    return response


# --------------------------------------------------------------------------
# Tests: Successful generation
# --------------------------------------------------------------------------

class TestGeminiClientSuccess:
    """Tests for successful Gemini API calls."""

    @patch("app.integrations.gemini_client.genai")
    def test_generate_returns_parsed_json(
        self, mock_genai, mock_settings, sample_response_data
    ):
        """Gemini should return parsed JSON dict on success."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.return_value = _make_mock_response(
            sample_response_data
        )

        client = GeminiClient()
        result = client.generate(
            user_prompt="Build a website",
            system_instruction="You are Arkitect",
        )

        assert isinstance(result, dict)
        assert result["goal"]["user_input"] == "Build a website"
        assert len(result["deliverables"]) == 3
        assert len(result["workflow"]) == 4

    @patch("app.integrations.gemini_client.genai")
    def test_generate_passes_response_schema(
        self, mock_genai, mock_settings, sample_response_data
    ):
        """response_schema should be set on the config when provided."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.return_value = _make_mock_response(
            sample_response_data
        )

        client = GeminiClient()
        schema = {"type": "object", "properties": {}}
        client.generate(
            user_prompt="Build a website",
            system_instruction="You are Arkitect",
            response_schema=schema,
        )

        # Verify generate_content was called
        mock_client.models.generate_content.assert_called_once()


# --------------------------------------------------------------------------
# Tests: Error handling
# --------------------------------------------------------------------------

class TestGeminiClientErrors:
    """Tests for error handling and exception mapping."""

    @patch("app.integrations.gemini_client.genai")
    def test_empty_response_raises_api_error(self, mock_genai, mock_settings):
        """Empty response text should raise GeminiAPIError."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        empty_response = MagicMock()
        empty_response.text = ""
        mock_client.models.generate_content.return_value = empty_response

        client = GeminiClient()
        with pytest.raises(GeminiAPIError, match="empty response"):
            client.generate(
                user_prompt="test",
                system_instruction="test",
            )

    @patch("app.integrations.gemini_client.genai")
    def test_invalid_json_raises_api_error(self, mock_genai, mock_settings):
        """Non-JSON response text should raise GeminiAPIError."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        bad_response = MagicMock()
        bad_response.text = "This is not JSON {{"
        mock_client.models.generate_content.return_value = bad_response

        client = GeminiClient()
        with pytest.raises(GeminiAPIError, match="invalid JSON"):
            client.generate(
                user_prompt="test",
                system_instruction="test",
            )

    @patch("app.integrations.gemini_client.genai")
    def test_auth_error_raises_api_error(self, mock_genai, mock_settings):
        """401/403 errors should raise GeminiAPIError (non-retryable)."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.side_effect = Exception(
            "403 Permission denied"
        )

        client = GeminiClient()
        with pytest.raises(GeminiAPIError, match="Authentication failed"):
            client.generate(
                user_prompt="test",
                system_instruction="test",
            )

    @patch("app.integrations.gemini_client.genai")
    def test_unknown_error_raises_api_error(self, mock_genai, mock_settings):
        """Unknown errors should be wrapped as GeminiAPIError."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.side_effect = RuntimeError(
            "Something completely unexpected"
        )

        client = GeminiClient()
        with pytest.raises(GeminiAPIError, match="Unexpected error"):
            client.generate(
                user_prompt="test",
                system_instruction="test",
            )


# --------------------------------------------------------------------------
# Tests: Retry behavior
# --------------------------------------------------------------------------

class TestGeminiClientRetry:
    """Tests for retry logic on transient errors."""

    @patch("app.integrations.gemini_client.genai")
    def test_rate_limit_is_retried(self, mock_genai, mock_settings, sample_response_data):
        """429 errors should be retried and succeed on subsequent attempt."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        # First call fails with 429, second succeeds
        mock_client.models.generate_content.side_effect = [
            Exception("429 Resource exhausted"),
            _make_mock_response(sample_response_data),
        ]

        client = GeminiClient()
        result = client.generate(
            user_prompt="test",
            system_instruction="test",
        )

        assert result["goal"]["user_input"] == "Build a website"
        assert mock_client.models.generate_content.call_count == 2

    @patch("app.integrations.gemini_client.genai")
    def test_timeout_is_retried(self, mock_genai, mock_settings, sample_response_data):
        """Timeout errors should be retried and succeed on subsequent attempt."""
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        mock_client.models.generate_content.side_effect = [
            Exception("Request timeout exceeded"),
            _make_mock_response(sample_response_data),
        ]

        client = GeminiClient()
        result = client.generate(
            user_prompt="test",
            system_instruction="test",
        )

        assert isinstance(result, dict)
        assert mock_client.models.generate_content.call_count == 2
