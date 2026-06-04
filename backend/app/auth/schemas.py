"""
Pydantic schemas for authentication.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenPayload(BaseModel):
    """Decoded JWT token payload from Supabase Auth."""
    sub: str = Field(..., description="Supabase Auth user ID (UUID string)")
    email: str = Field(default="", description="User email from JWT claims")
    exp: int = Field(default=0, description="Token expiration timestamp")
    aud: str = Field(default="", description="Token audience")


class UserResponse(BaseModel):
    """Public user profile returned by the API."""
    id: uuid.UUID
    email: str
    full_name: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserSyncRequest(BaseModel):
    """
    Optional body for the user sync endpoint.

    The JWT already carries the user ID and email.  This request
    allows the frontend to send additional profile fields that
    aren't in the JWT (e.g. full_name from the signup form).
    """
    full_name: str = Field(default="", max_length=255)
    avatar_url: str = Field(default="", max_length=2048)
