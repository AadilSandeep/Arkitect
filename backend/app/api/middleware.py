"""
API middleware — request IDs and rate limiting.
"""

import logging
import uuid
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)

# Context var for request ID — accessible from anywhere in the call stack
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Attach a unique request ID to every request for log correlation.

    The ID is:
      - Generated from the incoming X-Request-ID header (if present), or
      - Auto-generated as a UUID4.
      - Set in a context var for use in logging.
      - Returned in the X-Request-ID response header.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        request_id_ctx.set(rid)
        request.state.request_id = rid

        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
