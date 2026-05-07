"""
Correlation ID Middleware

Generates unique correlation IDs for each request and binds them to the logging context.
This enables request tracing across all log entries for a single request.
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates and attaches correlation IDs to requests.

    Each incoming request gets a unique correlation ID that is:
    - Stored in request.state.correlation_id
    - Bound to the structlog context for all log entries
    - Included in response headers for client tracing
    """

    def __init__(self, app: Callable, header_name: str = "X-Correlation-ID"):
        """
        Initialize the correlation ID middleware.

        Args:
            app: FastAPI application instance
            header_name: HTTP header name for correlation ID
        """
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process each request and attach correlation ID.

        Args:
            request: Incoming FastAPI request
            call_next: Next middleware/handler in chain

        Returns:
            Response with correlation ID header
        """
        # Check if correlation ID is provided in request headers
        correlation_id = request.headers.get(self.header_name)

        # Generate new correlation ID if not provided
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Store in request state for access by endpoints
        request.state.correlation_id = correlation_id

        # Bind to structlog context for all log entries in this request
        try:
            import structlog
            # Bind correlation ID to the current context
            with structlog.contextvars.bound_contextvars(correlation_id=correlation_id):
                response = await call_next(request)
        except ImportError:
            # Fallback if structlog not available
            response = await call_next(request)

        # Add correlation ID to response headers
        response.headers[self.header_name] = correlation_id

        return response


def get_correlation_id(request: Request) -> str:
    """
    Get the correlation ID from a request.

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID string
    """
    return getattr(request.state, 'correlation_id', 'unknown')