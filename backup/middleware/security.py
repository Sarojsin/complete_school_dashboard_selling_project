"""
Security Headers Middleware - Backward Compatibility Layer

This file now imports from app.shared.middleware for backward compatibility.
New code should import directly from app.shared.middleware
"""

# Re-export from shared location for backward compatibility
from backup.shared.middleware.security import SecurityHeadersMiddleware

__all__ = ["SecurityHeadersMiddleware"]
