from typing import List, Dict, Optional, Tuple, Any
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models.models import User, Message

class AdminMessageRepository:
    """Handles database queries for the Admin Messages endpoints."""

    @staticmethod
    async def get_messages(
        db: AsyncSession,
        sender_id: Optional[int] = None,
        recipient_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Message]:
        query = select(Message).options(
            selectinload(Message.sender),
            selectinload(Message.recipient)
        )
        
        if sender_id:
            query = query.where(Message.sender_id == sender_id)
        if recipient_id:
            query = query.where(Message.recipient_id == recipient_id)
        if search:
            query = query.where(
                (Message.subject.ilike(f"%{search}%")) |
                (Message.body.ilike(f"%{search}%"))
            )
        
        query = query.offset(skip).limit(limit).order_by(Message.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, message_id: int) -> Optional[Message]:
        result = await db.execute(select(Message).where(Message.id == message_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_analytics(db: AsyncSession, days: int) -> Dict[str, Any]:
        # Total messages
        total_r = await db.execute(select(func.count(Message.id)))
        
        # Recent messages
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_r = await db.execute(select(func.count(Message.id)).where(Message.created_at >= cutoff))
        
        # Most active senders
        active_users_result = await db.execute(
            select(Message.sender_id, func.count(Message.id).label('count'))
            .group_by(Message.sender_id)
            .order_by(func.count(Message.id).desc())
            .limit(10)
        )
        most_active_raw = active_users_result.all()
        
        # Daily stats
        daily_stats = []
        for i in range(days):
            day = datetime.utcnow() - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            count_r = await db.execute(
                select(func.count(Message.id)).where(
                    Message.created_at >= day_start,
                    Message.created_at <= day_end
                )
            )
            daily_stats.append({
                "date": day.strftime("%Y-%m-%d"),
                "count": count_r.scalar() or 0
            })
            
        return {
            "total_messages": total_r.scalar() or 0,
            "recent_messages": recent_r.scalar() or 0,
            "most_active_raw": most_active_raw,
            "daily_stats": daily_stats
        }
