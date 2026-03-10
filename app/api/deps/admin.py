"""
app.api.deps.admin
~~~~~~~~~~~~~~~~~~

Single source of truth for admin authentication dependencies and role constants.

All admin endpoint routers must import `get_current_admin` from here —
never re-define it locally and never import it from another endpoint module.

Usage:
    from app.api.deps.admin import get_current_admin

    @router.get("/some-route")
    async def my_handler(current_user: User = Depends(get_current_admin)):
        ...
"""

import bcrypt as _bcrypt

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.models import User, UserRole


# ---------------------------------------------------------------------------
# Password hashing — uses raw bcrypt, consistent with UserRepository
# ---------------------------------------------------------------------------

def hash_password(plain: str) -> str:
    """
    Hash a plain-text password using bcrypt (rounds=12).

    Mirrors ``UserRepository.get_password_hash`` — the single authoritative
    hashing approach used throughout this project.
    """
    password_bytes = plain.encode("utf-8")[:72]  # bcrypt max input length
    salt = _bcrypt.gensalt(rounds=12)
    return _bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    try:
        return _bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Role constants — defined once, imported everywhere
# ---------------------------------------------------------------------------

#: Roles with full admin/department-head access.
ADMIN_ROLES: list[UserRole] = [UserRole.ADMIN, UserRole.HOD]

#: Section-level admin roles with limited elevated access.
SECTION_ADMIN_ROLES: list[UserRole] = [
    UserRole.EXAM_SECTION,
    UserRole.LIBRARY_MANAGER,
    UserRole.ACCOUNT_SECTION,
    UserRole.AUTHORITY,
]

#: Combined set of all roles allowed into admin-protected endpoints.
ALL_ADMIN_ROLES: list[UserRole] = ADMIN_ROLES + SECTION_ADMIN_ROLES


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    FastAPI dependency that enforces admin or authority role.

    Resolves the current user from the session/token and raises:
    - 401 if not authenticated
    - 403 if the authenticated user lacks an admin role

    Returns the authenticated ``User`` ORM instance.
    """
    if current_user.role not in ALL_ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user


async def require_super_admin(
    current_user: User = Depends(get_current_admin),
) -> User:
    """
    Stricter dependency that only allows ADMIN role (not HOD or section admins).

    Use this for destructive or highly privileged operations such as:
    - changing user roles
    - deleting system features
    - modifying JWT/security settings
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super-admin (ADMIN role) privileges required",
        )
    return current_user
