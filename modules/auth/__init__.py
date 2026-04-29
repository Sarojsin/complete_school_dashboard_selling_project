"""
Auth Module - Authentication & Authorization

This module provides authentication dependencies, JWT handling,
password utilities, role-based access control, and all auth endpoints.
"""

from modules.auth.dependencies import get_current_user, require_role, require_super_admin
from modules.auth.utils import verify_password, hash_password, create_access_token, decode_token
from modules.auth.schemas import UserRole, LoginRequest, TokenResponse, RefreshRequest
from modules.auth.router import router as auth_router

__all__ = [
    "get_current_user",
    "require_role",
    "require_super_admin",
    "verify_password",
    "hash_password",
    "create_access_token",
    "decode_token",
    "UserRole",
    "LoginRequest",
    "TokenResponse",
    "RefreshRequest",
    "auth_router",
]