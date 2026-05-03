"""
Admin Communication Monitoring API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API endpoints for monitoring chat, moderating messages, and analytics.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminMessageService`.
- No direct database manipulations in the routing layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.core.database import get_async_db
from backup.models.models import User
from backup.api.deps.admin import get_current_admin
from backup.services.admin_message_service import AdminMessageService


# Create router
router = APIRouter(prefix="/admin/messages", tags=["Admin Messages"])


@router.get("/all")
async def get_all_messages(
    sender_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all messages with filtering"""
    return await AdminMessageService.get_all_messages(db, sender_id, recipient_id, search, skip, limit)


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a message (moderation)"""
    return await AdminMessageService.delete_message(db, message_id)


@router.get("/analytics")
async def get_message_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get message analytics"""
    return await AdminMessageService.get_message_analytics(db, days)
