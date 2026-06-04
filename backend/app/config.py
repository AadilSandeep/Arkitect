"""
Centralized application configuration using Pydantic BaseSettings.

Reads from environment variables and .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # ── Environment ──────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False

    # ── Application metadata ─────────────────────────────────────────────
    APP_NAME: str = "Arkitect API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered workflow architect — turn any goal into an execution plan."

    # ── API configuration ────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"

    # ── CORS configuration ───────────────────────────────────────────────
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = ""  # postgresql+asyncpg://user:pass@host/db

    # ── Supabase Auth ────────────────────────────────────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # ── Gemini API configuration ─────────────────────────────────────────
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_MAX_RETRIES: int = 3
    GEMINI_TIMEOUT: int = 30
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_OUTPUT_TOKENS: int = 4096
    GEMINI_ENABLED: bool = True

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_GENERATE: str = "10/minute"
    RATE_LIMIT_READ: str = "100/minute"


# Singleton instance
settings = Settings()
