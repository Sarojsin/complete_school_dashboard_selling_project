"""
Rate Limiting Configuration

Provides rate limiting for API endpoints to prevent abuse and ensure fair usage.
Uses slowapi with Redis backend when available, falls back to in-memory storage.
"""

import os
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Configure rate limiter
def create_limiter() -> Limiter:
    """
    Create and configure the rate limiter instance.

    Uses Redis if available, otherwise falls back to in-memory storage.
    """
    # Check if Redis is configured
    redis_url = os.getenv("REDIS_URL")
    storage_uri = redis_url if redis_url else "memory://"

    limiter = Limiter(
        key_func=get_remote_address,  # Rate limit by IP address
        storage_uri=storage_uri,
        default_limits=["200/day", "50/hour"],  # Default limits for all routes
        strategy="fixed-window",  # Fixed window strategy
        application_limits=["1000/day", "200/hour"],  # Global application limits
    )

    return limiter

# Global limiter instance
limiter = create_limiter()

# Specific limit decorators for different endpoint types
def auth_limit():
    """Rate limit for authentication endpoints (stricter)"""
    return limiter.limit("5/minute", key_func=get_remote_address)

def write_limit():
    """Rate limit for write operations (create, update, delete)"""
    return limiter.limit("30/minute", key_func=get_remote_address)

def read_limit():
    """Rate limit for read operations (list, get)"""
    return limiter.limit("100/minute", key_func=get_remote_address)

def admin_limit():
    """Rate limit for admin operations (most restrictive)"""
    return limiter.limit("10/minute", key_func=get_remote_address)

# Custom error handler for rate limit exceeded
def rate_limit_exceeded_handler(request, exc):
    """
    Custom handler for rate limit exceeded errors.
    Returns a structured error response.
    """
    from fastapi.responses import JSONResponse
    from fastapi import status

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": getattr(exc, 'retry_after', 60),  # seconds
            "limit": getattr(exc, 'limit', 'unknown'),
            "remaining": getattr(exc, 'remaining', 0),
        },
        headers={
            "Retry-After": str(getattr(exc, 'retry_after', 60)),
            "X-RateLimit-Limit": str(getattr(exc, 'limit', 'unknown')),
            "X-RateLimit-Remaining": str(getattr(exc, 'remaining', 0)),
        }
    )

# Middleware instance for FastAPI integration
rate_limit_middleware = SlowAPIMiddleware

__all__ = [
    "limiter",
    "auth_limit",
    "write_limit",
    "read_limit",
    "admin_limit",
    "rate_limit_exceeded_handler",
    "rate_limit_middleware",
]