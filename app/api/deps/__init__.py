"""
app.api.deps

Shared FastAPI dependency functions for API routes.
"""

from .admin import get_current_admin, require_super_admin, ADMIN_ROLES, SECTION_ADMIN_ROLES

__all__ = [
    "get_current_admin",
    "require_super_admin",
    "ADMIN_ROLES",
    "SECTION_ADMIN_ROLES",
]
