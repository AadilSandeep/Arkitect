"""
Arkitect API — FastAPI application entry point.

Configures the application, registers routers, and defines
middleware and error handlers.
"""

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import settings
from app.api.routes.workflow import router as workflow_router
from app.api.routes.workflows import router as workflows_router
from app.api.routes.auth import router as auth_router
from app.api.middleware import RequestIDMiddleware

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)

# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown hooks
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — initialize and clean up resources."""
    # Startup
    if settings.DATABASE_URL:
        from app.database.db import init_db
        try:
            await init_db()
            logger.info("Database initialized successfully")
        except Exception as exc:
            logger.warning("Database initialization skipped: %s", exc)
    else:
        logger.warning("DATABASE_URL not set — running without database")

    yield

    # Shutdown
    if settings.DATABASE_URL:
        from app.database.db import close_db
        await close_db()
        logger.info("Database connections closed")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Attach limiter to app state for slowapi
app.state.limiter = limiter

# ---------------------------------------------------------------------------
# Middleware (order matters — outermost first)
# ---------------------------------------------------------------------------

# 1. Request ID (outermost — every request gets an ID)
app.add_middleware(RequestIDMiddleware)

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------

# Rate limit exceeded → 429
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(workflow_router)
app.include_router(workflows_router)
app.include_router(auth_router)

# ---------------------------------------------------------------------------
# Root & Health Endpoints
# ---------------------------------------------------------------------------


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint — API status check."""
    # Trigger uvicorn reload again to apply new connection parameters
    return {
        "message": "Arkitect API Running",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/api/v1/health/db", tags=["health"])
async def health_db() -> dict[str, str]:
    """Check database connectivity."""
    if not settings.DATABASE_URL:
        return {"status": "skipped", "reason": "DATABASE_URL not configured"}
    try:
        from app.database.db import _get_engine
        from sqlalchemy import text

        engine = _get_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "service": "database"}
    except Exception as exc:
        logger.error("Database health check failed: %s", exc)
        return {"status": "unhealthy", "service": "database", "error": str(exc)}


# ---------------------------------------------------------------------------
# Global Error Handler
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all error handler for unhandled exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception(
        "Unhandled exception on %s %s [request_id=%s]",
        request.method,
        request.url,
        request_id,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again.",
            "request_id": request_id,
        },
    )