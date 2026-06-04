"""
Custom exception hierarchy for Gemini API integration.

Provides typed exceptions so callers can distinguish transient
(retryable) failures from permanent ones and route accordingly.
"""


class GeminiError(Exception):
    """Base exception for all Gemini-related errors."""

    def __init__(self, message: str = "", *, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class GeminiAPIError(GeminiError):
    """
    Non-retryable API error (e.g., 400 bad request, 401 auth failure).

    The caller should fall back to deterministic pipeline immediately.
    """


class GeminiRateLimitError(GeminiError):
    """
    Rate limit hit (HTTP 429).

    Retryable — the retry decorator will wait with exponential backoff.
    """


class GeminiTimeoutError(GeminiError):
    """
    Request timed out before Gemini responded.

    Retryable — transient network or server-side slowness.
    """


class GeminiValidationError(GeminiError):
    """
    Gemini returned JSON that failed schema or business-rule validation.

    May be partially repairable by the validation layer.
    """

    def __init__(
        self,
        message: str = "",
        *,
        raw_data: dict | None = None,
        issues: list[str] | None = None,
    ) -> None:
        self.raw_data = raw_data
        self.issues = issues or []
        super().__init__(message)
