from typing import List, Dict, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models.models import Notice

class AdminNoticeRepository:
    """Handles database queries for the Admin Notice endpoints."""

    @staticmethod
    async def get_notices(
        db: AsyncSession,
        target_role: Optional[str] = None,
        is_emergency: Optional[bool] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Notice]:
        query = select(Notice).options(
            selectinload(Notice.teacher),
            selectinload(Notice.authority)
        )
        
        if target_role:
            query = query.where(Notice.target_role == target_role)
        if is_emergency is not None:
            query = query.where(Notice.is_emergency == is_emergency)
        if is_active is not None:
            query = query.where(Notice.is_active == is_active)
        
        query = query.offset(skip).limit(limit).order_by(Notice.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, notice_id: int) -> Optional[Notice]:
        result = await db.execute(select(Notice).where(Notice.id == notice_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_stats(db: AsyncSession) -> Dict[str, int]:
        total_r = await db.execute(select(func.count(Notice.id)))
        active_r = await db.execute(select(func.count(Notice.id)).where(Notice.is_active == True))
        emergency_r = await db.execute(select(func.count(Notice.id)).where(Notice.is_emergency == True))
        
        by_role = {}
        for role in ["all", "student", "teacher", "parent", "authority"]:
            count_r = await db.execute(select(func.count(Notice.id)).where(Notice.target_role == role))
            by_role[role] = count_r.scalar() or 0
        
        today = date.today()
        scheduled_r = await db.execute(
            select(func.count(Notice.id)).where(
                Notice.publish_date > today,
                Notice.is_active == True
            )
        )
        
        return {
            "total_notices": total_r.scalar() or 0,
            "active_notices": active_r.scalar() or 0,
            "emergency_notices": emergency_r.scalar() or 0,
            "by_target_role": by_role,
            "scheduled_notices": scheduled_r.scalar() or 0
        }

    @staticmethod
    async def get_scheduled_notices(db: AsyncSession) -> List[Notice]:
        today = date.today()
        result = await db.execute(
            select(Notice).where(
                Notice.publish_date > today,
                Notice.is_active == True
            ).order_by(Notice.publish_date)
        )
        return list(result.scalars().all())
