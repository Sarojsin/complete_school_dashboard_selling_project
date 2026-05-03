"""
Admin Notice & Announcement Management API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API endpoints for managing global notices, role-based announcements, scheduled notices.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminNoticeService`.
- No direct database manipulations in the routing layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.core.database import get_async_db
from backup.models.models import User
from backup.api.deps.admin import get_current_admin
from backup.services.admin_notice_service import (
    AdminNoticeService, NoticeCreateDto, NoticeUpdateDto
)


# Create router
router = APIRouter(prefix="/admin/notices", tags=["Admin Notices"])


# ============ NOTICE MANAGEMENT ============

@router.get("")
async def get_all_notices(
    target_role: Optional[str] = None,
    is_emergency: Optional[bool] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all notices with filtering"""
    return await AdminNoticeService.get_all_notices(
        db, target_role, is_emergency, is_active, skip, limit
    )


@router.post("")
async def create_notice(
    notice_data: NoticeCreateDto,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new notice/announcement"""
    return await AdminNoticeService.create_notice(db, notice_data, current_user.id)


@router.patch("/{notice_id}")
async def update_notice(
    notice_id: int,
    notice_data: NoticeUpdateDto,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Update a notice"""
    return await AdminNoticeService.update_notice(db, notice_id, notice_data)


@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a notice"""
    return await AdminNoticeService.delete_notice(db, notice_id)


@router.post("/{notice_id}/toggle")
async def toggle_notice(
    notice_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Toggle notice active status"""
    return await AdminNoticeService.toggle_notice(db, notice_id)


@router.post("/{notice_id}/mark-emergency")
async def toggle_emergency(
    notice_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Mark/unmark notice as emergency"""
    return await AdminNoticeService.toggle_emergency(db, notice_id)


# ============ STATISTICS ============

@router.get("/stats")
async def get_notice_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get notice statistics"""
    return await AdminNoticeService.get_notice_stats(db)


# ============ SCHEDULED NOTICES ============

@router.get("/scheduled")
async def get_scheduled_notices(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get scheduled (future) notices"""
    return await AdminNoticeService.get_scheduled_notices(db)
