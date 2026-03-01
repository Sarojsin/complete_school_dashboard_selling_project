"""
Admin User Management API
~~~~~~~~~~~~~~~~~~~~~~~~~

Endpoints for managing users (students, teachers, parents, etc.).

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminUserService`.
- No direct database manipulations in the routing layer.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin, require_super_admin
from app.api.schemas.admin.users import ChangeRoleRequest, PasswordResetRequest, UserResponse
from app.services.admin_user_service import AdminUserService

router = APIRouter(prefix="/admin/users", tags=["Admin User Management"])


# ---------------------------------------------------------------------------
# User list / detail
# ---------------------------------------------------------------------------

@router.get("", response_model=List[UserResponse])
async def get_all_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all users with optional role, status, and text filters."""
    return await AdminUserService.get_all_users(db, role, is_active, search, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return a single user by primary key."""
    return await AdminUserService.get_user_or_404(db, user_id)


# ---------------------------------------------------------------------------
# Activate / deactivate
# ---------------------------------------------------------------------------

@router.patch("/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Toggle a user's active status. Admins cannot deactivate themselves."""
    return await AdminUserService.toggle_user_active(db, user_id, current_user.id)


# ---------------------------------------------------------------------------
# Password reset
# ---------------------------------------------------------------------------

@router.post("/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    body: PasswordResetRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Reset a user's password."""
    return await AdminUserService.reset_user_password(db, user_id, body)


# ---------------------------------------------------------------------------
# Role change (super-admin only)
# ---------------------------------------------------------------------------

@router.post("/{user_id}/change-role")
async def change_user_role(
    user_id: int,
    body: ChangeRoleRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Change a user's role (Super Admin only)."""
    return await AdminUserService.change_user_role(db, user_id, body)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

@router.get("/stats/by-role")
async def get_user_stats_by_role(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return per-role user statistics."""
    return await AdminUserService.get_user_stats_by_role(db)


# ---------------------------------------------------------------------------
# Scoped list endpoints
# ---------------------------------------------------------------------------

@router.get("/students/list")
async def get_students_list(
    grade: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return students with optional grade and name filters."""
    return await AdminUserService.get_students_list(db, grade, search, skip, limit)


@router.get("/teachers/list")
async def get_teachers_list(
    department: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return teachers with optional department and name filters."""
    return await AdminUserService.get_teachers_list(db, department, search, skip, limit)


@router.get("/parents/list")
async def get_parents_list(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return parents with optional name filter."""
    return await AdminUserService.get_parents_list(db, search, skip, limit)
