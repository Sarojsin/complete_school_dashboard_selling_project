from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
from models.models import Notice

class NoticeRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, notice_id: int) -> Optional[Notice]:
        result = await db.execute(
            select(Notice).options(
                joinedload(Notice.authority)
            ).filter(Notice.id == notice_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, notice_data: dict) -> Notice:
        notice = Notice(**notice_data)
        db.add(notice)
        await db.commit()
        await db.refresh(notice)
        return notice
    
    @staticmethod
    async def update(db: AsyncSession, notice: Notice, **kwargs) -> Notice:
        for key, value in kwargs.items():
            if value is not None and hasattr(notice, key):
                setattr(notice, key, value)
        await db.commit()
        await db.refresh(notice)
        return notice
    
    @staticmethod
    async def delete(db: AsyncSession, notice: Notice):
        await db.delete(notice)
        await db.commit()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100,
                target_role: str = None, priority: str = None) -> List[Notice]:
        query = select(Notice).options(joinedload(Notice.authority))
        
        # Filter out expired notices
        query = query.filter(
            or_(Notice.expires_at.is_(None), Notice.expires_at >= datetime.utcnow())
        )
        
        if target_role:
            query = query.filter(
                or_(Notice.target_role == target_role, Notice.target_role == 'all')
            )
        
        if priority:
            query = query.filter(Notice.priority == priority)
        
        result = await db.execute(
            query.order_by(
                Notice.priority.desc(),
                Notice.created_at.desc()
            ).offset(skip).limit(limit)
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_active_notices(db: AsyncSession, target_role: str = None) -> List[Notice]:
        """Get all active (non-expired) notices"""
        return await NoticeRepository.get_all(db, target_role=target_role)
    
    @staticmethod
    async def get_by_priority(db: AsyncSession, priority: str, 
                       target_role: str = None) -> List[Notice]:
        """Get notices by priority level"""
        return await NoticeRepository.get_all(db, priority=priority, target_role=target_role)
    
    @staticmethod
    async def get_urgent_notices(db: AsyncSession, target_role: str = None) -> List[Notice]:
        """Get urgent notices"""
        return await NoticeRepository.get_by_priority(db, 'urgent', target_role)
    
    @staticmethod
    async def get_recent_notices(db: AsyncSession, days: int = 7, 
                          target_role: str = None) -> List[Notice]:
        """Get notices from last N days"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = select(Notice).options(joinedload(Notice.authority)).filter(Notice.created_at >= cutoff_date)
        
        if target_role:
            query = query.filter(
                or_(Notice.target_role == target_role, Notice.target_role == 'all')
            )
        
        result = await db.execute(query.order_by(Notice.created_at.desc()))
        return result.scalars().unique().all()
    
    @staticmethod
    async def delete_expired_notices(db: AsyncSession):
        """Delete expired notices (run as scheduled task)"""
        result = await db.execute(
            delete(Notice).filter(Notice.expires_at < datetime.utcnow())
        )
        await db.commit()
        return result.rowcount
    
    @staticmethod
    async def search_notices(db: AsyncSession, query: str, target_role: str = None) -> List[Notice]:
        """Search notices by title or content"""
        search_pattern = f"%{query}%"
        
        search_query = select(Notice).options(joinedload(Notice.authority)).filter(
            or_(
                Notice.title.ilike(search_pattern),
                Notice.content.ilike(search_pattern)
            )
        )
        
        if target_role:
            search_query = search_query.filter(
                or_(Notice.target_role == target_role, Notice.target_role == 'all')
            )
        
        result = await db.execute(search_query.order_by(Notice.created_at.desc()).limit(50))
        return result.scalars().unique().all()