"""
Shared module for common components used across the application.
Contains authentication, middleware, and utility functions.
"""

from backup.shared.auth import get_current_user
from backup.shared.middleware import SecurityHeadersMiddleware, require_feature, Features

__all__ = [
    "get_current_user",
    "SecurityHeadersMiddleware",
    "require_feature",
    "Features",
]
