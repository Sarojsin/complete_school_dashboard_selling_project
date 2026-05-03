"""
CSRF Middleware - Backward Compatibility Layer

This file now imports from app.shared.middleware for backward compatibility.
New code should import directly from app.shared.middleware
"""

# Re-export from shared location for backward compatibility
from backup.shared.middleware.csrf import CSRFMiddleware, csrf_token_processor

__all__ = ["CSRFMiddleware", "csrf_token_processor"]
