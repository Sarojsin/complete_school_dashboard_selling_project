from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.chat_models import ChatMessage
from app.models.models import User
from datetime import datetime

class ChatService:
    @staticmethod
    async def save_message(db: AsyncSession, sender_id: int, receiver_id: int, content: str):
        chat_message = ChatMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        db.add(chat_message)
        await db.commit()
        await db.refresh(chat_message)
        return chat_message

    @staticmethod
    async def mark_messages_as_read(db: AsyncSession, message_ids: list, receiver_id: int):
        await db.execute(
            update(ChatMessage).filter(
                ChatMessage.id.in_(message_ids),
                ChatMessage.receiver_id == receiver_id
            ).values(is_read=True)
        )
        await db.commit()

    @staticmethod
    async def get_chat_history(db: AsyncSession, user1_id: int, user2_id: int, limit: int = 50):
        # Implementation for fetching history
        pass
