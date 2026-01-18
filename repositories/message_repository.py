from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from models.models import Message, User
from datetime import datetime, timedelta

class MessageRepository:
    @staticmethod
    async def create(db: AsyncSession, sender_id: int, recipient_id: int, subject: str, body: str) -> Message:
        """Create a new message"""
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            subject=subject,
            body=body
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message
    
    @staticmethod
    async def get_inbox(db: AsyncSession, user_id: int, limit: int = 50, unread_only: bool = False) -> List[Message]:
        """Get messages for a user's inbox (only messages from last 24 hours)"""
        # Filter messages older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        query = select(Message).options(
            joinedload(Message.sender)
        ).filter(
            Message.recipient_id == user_id,
            Message.created_at >= cutoff_time  # Auto-delete: only show messages < 24hrs old
        )
        
        if unread_only:
            query = query.filter(Message.is_read == False)
        
        result = await db.execute(query.order_by(Message.created_at.desc()).limit(limit))
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_by_id(db: AsyncSession, message_id: int) -> Optional[Message]:
        """Get a single message by ID"""
        result = await db.execute(
            select(Message).options(
                joinedload(Message.sender),
                joinedload(Message.recipient)
            ).filter(Message.id == message_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def mark_as_read(db: AsyncSession, message_id: int) -> Optional[Message]:
        """Mark a message as read"""
        result = await db.execute(select(Message).filter(Message.id == message_id))
        message = result.scalars().first()
        if message:
            message.is_read = True
            await db.commit()
            await db.refresh(message)
        return message
    
    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: int) -> int:
        """Get count of unread messages for a user (only from last 24 hours)"""
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        result = await db.execute(
            select(func.count(Message.id)).filter(
                Message.recipient_id == user_id,
                Message.is_read == False,
                Message.created_at >= cutoff_time  # Auto-delete: only count messages < 24hrs old
            )
        )
        return result.scalar() or 0
