from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import date

from backup.models.models import Notice, User
from backup.repositories.admin_notice_repository import AdminNoticeRepository
from backup.core.exceptions import NotFoundError


class NoticeCreateDto(BaseModel):
    title: str
    content: str
    target_role: Optional[str] = None
    is_emergency: bool = False
    publish_date: Optional[date] = None
    expiry_date: Optional[date] = None

class NoticeUpdateDto(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    target_role: Optional[str] = None
    is_emergency: Optional[bool] = None
    is_active: Optional[bool] = None
    publish_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AdminNoticeService:
    """Business logic for Admin Notice management."""

    @staticmethod
    async def get_all_notices(
        db: AsyncSession,
        target_role: Optional[str],
        is_emergency: Optional[bool],
        is_active: Optional[bool],
        skip: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        notices = await AdminNoticeRepository.get_notices(db, target_role, is_emergency, is_active, skip, limit)
        return [{
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "target_role": n.target_role,
            "is_emergency": n.is_emergency,
            "is_active": n.is_active,
            "created_by": n.created_by,
            "creator_name": n.teacher.full_name if getattr(n, 'teacher', None) else (n.authority.full_name if getattr(n, 'authority', None) else "Admin"),
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "publish_date": n.publish_date.isoformat() if n.publish_date else None,
            "expiry_date": n.expiry_date.isoformat() if n.expiry_date else None
        } for n in notices]

    @staticmethod
    async def create_notice(db: AsyncSession, notice_data: NoticeCreateDto, current_user_id: int) -> Dict[str, Any]:
        notice = Notice(
            title=notice_data.title,
            content=notice_data.content,
            target_role=notice_data.target_role or "all",
            is_emergency=notice_data.is_emergency,
            is_active=True,
            publish_date=notice_data.publish_date,
            expiry_date=notice_data.expiry_date,
            created_by=current_user_id
        )
        db.add(notice)
        await db.commit()
        await db.refresh(notice)
        
        return {
            "success": True,
            "notice": {
                "id": notice.id,
                "title": notice.title,
                "is_emergency": notice.is_emergency
            }
        }

    @staticmethod
    async def update_notice(db: AsyncSession, notice_id: int, notice_data: NoticeUpdateDto) -> Dict[str, Any]:
        notice = await AdminNoticeRepository.get_by_id(db, notice_id)
        if not notice:
            raise NotFoundError("Notice not found")
        
        for field, value in notice_data.model_dump(exclude_unset=True).items():
            setattr(notice, field, value)
        
        await db.commit()
        return {"success": True, "message": "Notice updated"}

    @staticmethod
    async def delete_notice(db: AsyncSession, notice_id: int) -> Dict[str, Any]:
        notice = await AdminNoticeRepository.get_by_id(db, notice_id)
        if not notice:
            raise NotFoundError("Notice not found")
        
        await db.delete(notice)
        await db.commit()
        return {"success": True, "message": "Notice deleted"}

    @staticmethod
    async def toggle_notice(db: AsyncSession, notice_id: int) -> Dict[str, Any]:
        notice = await AdminNoticeRepository.get_by_id(db, notice_id)
        if not notice:
            raise NotFoundError("Notice not found")
        
        notice.is_active = not notice.is_active
        await db.commit()
        return {"success": True, "is_active": notice.is_active}

    @staticmethod
    async def toggle_emergency(db: AsyncSession, notice_id: int) -> Dict[str, Any]:
        notice = await AdminNoticeRepository.get_by_id(db, notice_id)
        if not notice:
            raise NotFoundError("Notice not found")
        
        notice.is_emergency = not notice.is_emergency
        await db.commit()
        return {"success": True, "is_emergency": notice.is_emergency}

    @staticmethod
    async def get_notice_stats(db: AsyncSession) -> Dict[str, Any]:
        stats = await AdminNoticeRepository.get_stats(db)
        return stats

    @staticmethod
    async def get_scheduled_notices(db: AsyncSession) -> List[Dict[str, Any]]:
        notices = await AdminNoticeRepository.get_scheduled_notices(db)
        return [{
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "target_role": n.target_role,
            "is_emergency": n.is_emergency,
            "publish_date": n.publish_date.isoformat() if n.publish_date else None,
            "expiry_date": n.expiry_date.isoformat() if n.expiry_date else None
        } for n in notices]
