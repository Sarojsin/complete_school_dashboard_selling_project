"""
Request Logging Middleware

Logs every incoming HTTP request automatically.
"""

import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from modules.shared.logger import get_logger

logger = get_logger("http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs every HTTP request."""
    
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.perf_counter() - start) * 1000
        
        # Get client IP
        client_ip = None
        if request.client:
            client_ip = request.client.host
        
        # Log the request
        log_data = {
            "type": "request",
            "method": request.method,
            "path": str(request.url.path),
            "query": str(request.url.query) if request.url.query else "",
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": client_ip or "unknown",
        }
        
        # Add response headers size
        response_headers = dict(response.headers)
        content_length = response_headers.get("content-length", "0")
        log_data["response_size"] = content_length
        
        # Log based on status code
        if response.status_code >= 500:
            logger.error(f"{request.method} {request.url.path} -> {response.status_code}", extra=log_data)
        elif response.status_code >= 400:
            logger.warning(f"{request.method} {request.url.path} -> {response.status_code}", extra=log_data)
        elif duration_ms > 1000:
            logger.warning(f"Slow request: {request.method} {request.url.path} took {duration_ms}ms", extra=log_data)
        else:
            logger.info(f"{request.method} {request.url.path} -> {response.status_code}", extra=log_data)
        
        # Add response time header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        return response


# Alternative: Simple function-based middleware for Starlette
async def simple_request_logging_middleware(request: Request, call_next):
    """Simple request logging without BaseHTTPMiddleware."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    
    # Add response time header
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
    
    return response
