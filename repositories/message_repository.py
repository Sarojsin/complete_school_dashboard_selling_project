from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Message, User

class MessageRepository:
    @staticmethod
    def create(db: Session, sender_id: int, recipient_id: int, subject: str, body: str) -> Message:
        """Create a new message"""
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            subject=subject,
            body=body
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def get_inbox(db: Session, user_id: int, limit: int = 50, unread_only: bool = False) -> List[Message]:
        """Get messages for a user's inbox (only messages from last 24 hours)"""
        from datetime import datetime, timedelta
        
        # Filter messages older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        query = db.query(Message).options(
            joinedload(Message.sender)
        ).filter(
            Message.recipient_id == user_id,
            Message.created_at >= cutoff_time  # Auto-delete: only show messages < 24hrs old
        )
        
        if unread_only:
            query = query.filter(Message.is_read == False)
        
        return query.order_by(Message.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, message_id: int) -> Optional[Message]:
        """Get a single message by ID"""
        return db.query(Message).options(
            joinedload(Message.sender),
            joinedload(Message.recipient)
        ).filter(Message.id == message_id).first()
    
    @staticmethod
    def mark_as_read(db: Session, message_id: int) -> Optional[Message]:
        """Mark a message as read"""
        message = db.query(Message).filter(Message.id == message_id).first()
        if message:
            message.is_read = True
            db.commit()
            db.refresh(message)
        return message
    
    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """Get count of unread messages for a user (only from last 24 hours)"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        return db.query(Message).filter(
            Message.recipient_id == user_id,
            Message.is_read == False,
            Message.created_at >= cutoff_time  # Auto-delete: only count messages < 24hrs old
        ).count()
