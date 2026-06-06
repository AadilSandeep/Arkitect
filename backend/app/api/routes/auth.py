"""
Authentication API routes.

Handles user sync from Supabase Auth and profile retrieval.
"""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import UserResponse, UserSyncRequest
from app.auth.dependencies import get_current_user
from app.config import settings
from app.database.db import get_db
from app.database.models import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

_bearer_scheme = HTTPBearer(auto_error=False)


@router.post(
    "/sync-user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Sync Supabase Auth user to the database",
    description=(
        "Called by the frontend after signup/login. Extracts user info "
        "from the JWT and upserts a record in the users table."
    ),
)
async def sync_user(
    body: UserSyncRequest | None = None,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Upsert a user record from the Supabase JWT claims.

    The frontend calls this after signup or first login so the backend
    database has a matching user row for foreign key references.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decode the JWT to get user info
    try:
        if not settings.SUPABASE_JWT_SECRET and settings.ENVIRONMENT == "development":
            logger.warning("SUPABASE_JWT_SECRET not set — decoding JWT without signature verification (dev bypass)")
            payload = jwt.get_unverified_claims(credentials.credentials)
        else:
            payload = jwt.decode(
                credentials.credentials,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
    except JWTError as exc:
        logger.warning("JWT verification failed during sync: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user_id_str = payload.get("sub")
    email = payload.get("email", "")

    if not user_id_str or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token missing required claims (sub, email).",
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID in token.",
        ) from exc

    # Upsert: find existing user or create new
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        # Create new user
        user = User(
            id=user_id,
            email=email,
            full_name=body.full_name if body else "",
            avatar_url=body.avatar_url if body else "",
        )
        db.add(user)
        logger.info("Created new user: %s (%s)", user_id, email)
    else:
        # Update existing user (email may change, profile fields may be new)
        user.email = email
        if body and body.full_name:
            user.full_name = body.full_name
        if body and body.avatar_url:
            user.avatar_url = body.avatar_url
        logger.info("Updated existing user: %s (%s)", user_id, email)

    await db.flush()
    await db.refresh(user)
    return user


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile information.",
)
async def get_me(
    user: User = Depends(get_current_user),
) -> User:
    """Return the current authenticated user's profile."""
    return user
