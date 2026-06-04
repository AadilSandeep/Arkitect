"""
Low-level Gemini API transport client.

Handles HTTP communication with the Gemini API, including:
  - JSON-only response enforcement via response_mime_type
  - Schema-constrained output via response_schema
  - Exponential backoff with jitter for transient errors (429, timeouts)
  - Typed exception mapping for the service layer
"""

import json
import logging
from typing import Any

from google import genai
from google.genai import types
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings
from app.integrations.exceptions import (
    GeminiAPIError,
    GeminiRateLimitError,
    GeminiTimeoutError,
)

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Low-level Gemini API transport layer.

    Wraps the google-genai SDK to provide:
      - Structured JSON responses (no markdown, no prose)
      - Automatic retry on transient failures
      - Clean exception mapping
    """

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set — Gemini calls will fail")

        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self._model = settings.GEMINI_MODEL

    @retry(
        stop=stop_after_attempt(settings.GEMINI_MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((GeminiRateLimitError, GeminiTimeoutError)),
        reraise=True,
    )
    def generate(
        self,
        *,
        user_prompt: str,
        system_instruction: str,
        response_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Send a prompt to Gemini and return the parsed JSON response.

        Args:
            user_prompt: The dynamic user-facing prompt.
            system_instruction: Fixed system-level instructions.
            response_schema: JSON Schema dict constraining the output shape.

        Returns:
            Parsed JSON dict from Gemini's response.

        Raises:
            GeminiAPIError: Non-retryable API error (400, 401, 403).
            GeminiRateLimitError: Rate limit hit (429) — retried automatically.
            GeminiTimeoutError: Request timed out — retried automatically.
        """
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
            system_instruction=system_instruction,
        )

        # Attach response schema if provided
        if response_schema is not None:
            config.response_schema = response_schema

        try:
            logger.debug(
                "Sending request to Gemini model=%s, prompt_len=%d",
                self._model,
                len(user_prompt),
            )

            response = self._client.models.generate_content(
                model=self._model,
                contents=user_prompt,
                config=config,
            )

            # Extract text from response
            raw_text = response.text
            if not raw_text:
                raise GeminiAPIError(
                    "Gemini returned an empty response",
                    status_code=None,
                )

            logger.debug("Gemini raw response length: %d chars", len(raw_text))

            # Parse JSON
            try:
                parsed = json.loads(raw_text)
            except json.JSONDecodeError as exc:
                logger.error(
                    "Gemini returned invalid JSON: %s\nRaw: %s",
                    exc,
                    raw_text[:500],
                )
                raise GeminiAPIError(
                    f"Gemini returned invalid JSON: {exc}"
                ) from exc

            return parsed

        except GeminiAPIError:
            raise
        except GeminiRateLimitError:
            raise
        except GeminiTimeoutError:
            raise
        except Exception as exc:
            error_msg = str(exc).lower()

            # Map known error patterns to typed exceptions
            if "429" in error_msg or "resource exhausted" in error_msg:
                logger.warning("Gemini rate limit hit, will retry: %s", exc)
                raise GeminiRateLimitError(
                    f"Rate limit exceeded: {exc}", status_code=429
                ) from exc

            if "timeout" in error_msg or "deadline" in error_msg:
                logger.warning("Gemini timeout, will retry: %s", exc)
                raise GeminiTimeoutError(
                    f"Request timed out: {exc}"
                ) from exc

            if "401" in error_msg or "403" in error_msg or "permission" in error_msg:
                logger.error("Gemini auth failure: %s", exc)
                raise GeminiAPIError(
                    f"Authentication failed: {exc}", status_code=401
                ) from exc

            # Unknown error — wrap as non-retryable
            logger.error("Unexpected Gemini error: %s", exc)
            raise GeminiAPIError(f"Unexpected error: {exc}") from exc
