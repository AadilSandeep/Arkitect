"""
FastAPI dependencies for authentication.

Verifies Supabase JWTs using the project's JWT secret and resolves
the caller to a database User record.
"""

import logging
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.db import get_db
from app.database.models import User

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Security scheme — extracts the Bearer token from the Authorization header.
# auto_error=False so we can return a friendlier 401 message.
# ---------------------------------------------------------------------------
_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Verify the Supabase JWT and return the corresponding database user.

    This dependency:
      1. Extracts the Bearer token from the Authorization header.
      2. Decodes and verifies the JWT using the Supabase JWT secret.
      3. Looks up the user in the database by the ``sub`` claim (Supabase UID).
      4. Returns the User ORM instance.

    Raises:
        HTTPException 401: If the token is missing, invalid, or expired.
        HTTPException 401: If the user is not found in the database.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # --- Verify JWT ---
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError as exc:
        logger.warning("JWT verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # --- Extract user ID from the `sub` claim ---
    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing 'sub' claim.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # --- Look up user in the database ---
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        # User exists in Supabase Auth but hasn't been synced yet.
        # The frontend should call /auth/sync-user after signup.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please complete registration by calling /api/v1/auth/sync-user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
