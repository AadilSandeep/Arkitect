"""
Database engine and session factory.

Provides an async SQLAlchemy engine connected to PostgreSQL (Neon),
a session factory, and a FastAPI dependency for request-scoped sessions.
"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


# ---------------------------------------------------------------------------
# Engine & Session Factory
# ---------------------------------------------------------------------------
# The engine is created lazily on first access.  When DATABASE_URL is empty
# (e.g. during local testing without a database), we skip creation and let
# `get_db` raise a clear error.
# ---------------------------------------------------------------------------

_engine = None
_async_session_factory = None


def _get_engine():
    """Return the async engine, creating it on first call."""
    global _engine, _async_session_factory
    if _engine is None:
        if not settings.DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL is not configured. "
                "Set it in .env or as an environment variable."
            )
        is_sqlite = settings.DATABASE_URL.startswith("sqlite")
        engine_kwargs = {
            "echo": settings.DEBUG,
        }
        if not is_sqlite:
            engine_kwargs.update({
                "pool_pre_ping": True,
                "pool_size": 5,
                "max_overflow": 10,
            })
        _engine = create_async_engine(
            settings.DATABASE_URL,
            **engine_kwargs
        )
        _async_session_factory = sessionmaker(
            _engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.info("Database engine created (is_sqlite=%s)", is_sqlite)
    return _engine


def _get_session_factory():
    """Return the session factory, ensuring the engine is initialized."""
    if _async_session_factory is None:
        _get_engine()
    return _async_session_factory


# ---------------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a request-scoped async database session.

    Usage::

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    factory = _get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ---------------------------------------------------------------------------
# Lifecycle Helpers
# ---------------------------------------------------------------------------

async def init_db() -> None:
    """Create all tables (development convenience — use Alembic in production)."""
    engine = _get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created / verified")


async def close_db() -> None:
    """Dispose the engine connection pool."""
    global _engine, _async_session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        logger.info("Database engine disposed")
