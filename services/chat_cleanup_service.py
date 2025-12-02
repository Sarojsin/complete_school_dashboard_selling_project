from datetime import datetime
from database.database import SessionLocal
from models.chat_models import ChatMessage
import logging

logger = logging.getLogger(__name__)

def cleanup_expired_messages():
    """Delete chat messages that have expired"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        deleted_count = db.query(ChatMessage).filter(
            ChatMessage.expires_at < now
        ).delete()
        
        db.commit()
        logger.info(f"Cleaned up {deleted_count} expired chat messages")
        
    except Exception as e:
        logger.error(f"Error cleaning up chat messages: {e}")
        db.rollback()
    finally:
        db.close()