"""
Auth Module - Authentication & Authorization

This module provides authentication dependencies for the new modular structure.
Imports from the existing app/ structure.
"""

from modules.auth.dependencies import get_current_user, require_role, require_super_admin
from modules.auth.utils import verify_password, hash_password, create_access_token, decode_token
from modules.shared.models import UserRole

__all__ = [
    "get_current_user",
    "require_role",
    "require_super_admin",
    "verify_password",
    "hash_password",
    "create_access_token",
    "decode_token",
    "UserRole",
]
