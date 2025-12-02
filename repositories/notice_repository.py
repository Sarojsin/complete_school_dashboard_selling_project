from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from models.models import Notice

class NoticeRepository:
    @staticmethod
    def get_by_id(db: Session, notice_id: int) -> Optional[Notice]:
        return db.query(Notice).options(
            joinedload(Notice.authority)
        ).filter(Notice.id == notice_id).first()
    
    @staticmethod
    def create(db: Session, notice_data: dict) -> Notice:
        notice = Notice(**notice_data)
        db.add(notice)
        db.commit()
        db.refresh(notice)
        return notice
    
    @staticmethod
    def update(db: Session, notice: Notice, **kwargs) -> Notice:
        for key, value in kwargs.items():
            if value is not None and hasattr(notice, key):
                setattr(notice, key, value)
        db.commit()
        db.refresh(notice)
        return notice
    
    @staticmethod
    def delete(db: Session, notice: Notice):
        db.delete(notice)
        db.commit()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                target_role: str = None, priority: str = None) -> List[Notice]:
        query = db.query(Notice).options(joinedload(Notice.authority))
        
        # Filter out expired notices
        query = query.filter(
            (Notice.expires_at.is_(None)) | (Notice.expires_at >= datetime.utcnow())
        )
        
        if target_role:
            query = query.filter(
                (Notice.target_role == target_role) | (Notice.target_role == 'all')
            )
        
        if priority:
            query = query.filter(Notice.priority == priority)
        
        return query.order_by(
            Notice.priority.desc(),
            Notice.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_active_notices(db: Session, target_role: str = None) -> List[Notice]:
        """Get all active (non-expired) notices"""
        return NoticeRepository.get_all(db, target_role=target_role)
    
    @staticmethod
    def get_by_priority(db: Session, priority: str, 
                       target_role: str = None) -> List[Notice]:
        """Get notices by priority level"""
        return NoticeRepository.get_all(db, priority=priority, target_role=target_role)
    
    @staticmethod
    def get_urgent_notices(db: Session, target_role: str = None) -> List[Notice]:
        """Get urgent notices"""
        return NoticeRepository.get_by_priority(db, 'urgent', target_role)
    
    @staticmethod
    def get_recent_notices(db: Session, days: int = 7, 
                          target_role: str = None) -> List[Notice]:
        """Get notices from last N days"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(Notice).filter(Notice.created_at >= cutoff_date)
        
        if target_role:
            query = query.filter(
                (Notice.target_role == target_role) | (Notice.target_role == 'all')
            )
        
        return query.order_by(Notice.created_at.desc()).all()
    
    @staticmethod
    def delete_expired_notices(db: Session):
        """Delete expired notices (run as scheduled task)"""
        deleted = db.query(Notice).filter(
            Notice.expires_at < datetime.utcnow()
        ).delete()
        
        db.commit()
        return deleted
    
    @staticmethod
    def search_notices(db: Session, query: str, target_role: str = None) -> List[Notice]:
        """Search notices by title or content"""
        search_pattern = f"%{query}%"
        
        search_query = db.query(Notice).filter(
            (Notice.title.ilike(search_pattern)) |
            (Notice.content.ilike(search_pattern))
        )
        
        if target_role:
            search_query = search_query.filter(
                (Notice.target_role == target_role) | (Notice.target_role == 'all')
            )
        
        return search_query.order_by(Notice.created_at.desc()).limit(50).all()