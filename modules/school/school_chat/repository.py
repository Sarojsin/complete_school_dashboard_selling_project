from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, and_, func, desc
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime, timedelta
from modules.school.school_chat.models import ChatMessage


class ChatRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, message_id: int) -> Optional[ChatMessage]:
        result = await db.execute(select(ChatMessage).filter(ChatMessage.id == message_id))
        return result.scalars().first()

    @staticmethod
    async def get_conversation(db: AsyncSession, user1_id: int, user2_id: int, limit: int = 50) -> List[ChatMessage]:
        """Get messages between two users"""
        result = await db.execute(
            select(ChatMessage).options(
                joinedload(ChatMessage.sender),
                joinedload(ChatMessage.receiver)
            ).filter(
                or_(
                    and_(ChatMessage.sender_id == user1_id, ChatMessage.receiver_id == user2_id),
                    and_(ChatMessage.sender_id == user2_id, ChatMessage.receiver_id == user1_id)
                )
            ).order_by(desc(ChatMessage.created_at)).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, message_data: dict) -> ChatMessage:
        message = ChatMessage(**message_data)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def mark_as_read(db: AsyncSession, user1_id: int, user2_id: int):
        """Mark messages from user2 to user1 as read"""
        await db.execute(
            update(ChatMessage).filter(
                ChatMessage.sender_id == user2_id,
                ChatMessage.receiver_id == user1_id,
                ChatMessage.is_read == False
            ).values(is_read=True)
        )
        await db.commit()

    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: int) -> int:
        """Get count of unread messages"""
        result = await db.execute(
            select(func.count(ChatMessage.id)).filter(
                ChatMessage.receiver_id == user_id,
                ChatMessage.is_read == False
            )
        )
        return result.scalar() or 0

    @staticmethod
    async def get_conversations(db: AsyncSession, user_id: int) -> List[dict]:
        """Get list of conversations with last message info"""
        # Get distinct users the user has chatted with
        other_user_id_col = (
            ChatMessage.receiver_id if ChatMessage.sender_id == user_id
            else ChatMessage.sender_id
        ).label('other_user_id')

        subquery = select(
            other_user_id_col,
            func.max(ChatMessage.created_at).label('last_message_time')
        ).filter(
            or_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == user_id)
        ).group_by('other_user_id').subquery()

        # Get conversations with last message and unread count
        conversations = []
        result = await db.execute(
            select(subquery).order_by(subquery.c.last_message_time.desc())
        )
        
        for row in result:
            other_user_id = row.other_user_id
            
            # Get last message
            last_msg_result = await db.execute(
                select(ChatMessage).filter(
                    or_(
                        and_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == other_user_id),
                        and_(ChatMessage.sender_id == other_user_id, ChatMessage.receiver_id == user_id)
                    )
                ).order_by(desc(ChatMessage.created_at)).limit(1)
            )
            last_msg = last_msg_result.scalars().first()
            
            # Get unread count
            unread_result = await db.execute(
                select(func.count(ChatMessage.id)).filter(
                    ChatMessage.sender_id == other_user_id,
                    ChatMessage.receiver_id == user_id,
                    ChatMessage.is_read == False
                )
            )
            unread_count = unread_result.scalar() or 0
            
            if last_msg:
                # Get other user info (placeholder - would need User model)
                conversations.append({
                    "user_id": other_user_id,
                    "last_message": last_msg.content[:50] + "..." if len(last_msg.content) > 50 else last_msg.content,
                    "last_message_time": last_msg.created_at,
                    "unread_count": unread_count
                })
        
        return conversations

    @staticmethod
    async def delete_expired_messages(db: AsyncSession):
        """Delete messages past expiration date"""
        now = datetime.utcnow()
        result = await db.execute(
            delete(ChatMessage).filter(ChatMessage.expires_at < now)
        )
        await db.commit()
        return result.rowcount

    @staticmethod
    async def search_messages(db: AsyncSession, user_id: int, query: str) -> List[ChatMessage]:
        """Search messages for a user"""
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(ChatMessage).filter(
                or_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == user_id),
                ChatMessage.content.ilike(search_pattern)
            ).order_by(desc(ChatMessage.created_at)).limit(50)
        )
        return result.scalars().all()