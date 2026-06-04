"""Authentication module — Supabase JWT verification and user management."""

from app.auth.dependencies import get_current_user  # noqa: F401

__all__ = ["get_current_user"]
