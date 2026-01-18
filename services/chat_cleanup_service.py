from datetime import datetime
from app.core.database import AsyncSessionLocal
from models.chat_models import ChatMessage
from sqlalchemy import delete
import logging

logger = logging.getLogger(__name__)

async def cleanup_expired_messages():
    """Delete chat messages that have expired"""
    async with AsyncSessionLocal() as db:
        try:
            now = datetime.utcnow()
            res = await db.execute(
                delete(ChatMessage).filter(
                    ChatMessage.expires_at < now
                )
            )
            await db.commit()
            logger.info(f"Cleaned up {res.rowcount} expired chat messages")
            
        except Exception as e:
            logger.error(f"Error cleaning up chat messages: {e}")
            await db.rollback()