from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.admin_message_repository import AdminMessageRepository
from app.core.exceptions import NotFoundError


class AdminMessageService:
    """Business logic for Admin Messages management."""

    @staticmethod
    async def get_all_messages(
        db: AsyncSession, sender_id: Optional[int], recipient_id: Optional[int], 
        search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        messages = await AdminMessageRepository.get_messages(db, sender_id, recipient_id, search, skip, limit)
        return [{
            "id": m.id,
            "sender_id": m.sender_id,
            "sender_name": getattr(m.sender, 'full_name', "N/A") if getattr(m, 'sender', None) else "N/A",
            "recipient_id": m.recipient_id,
            "recipient_name": getattr(m.recipient, 'full_name', "N/A") if getattr(m, 'recipient', None) else "N/A",
            "subject": m.subject,
            "body": m.body,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat() if m.created_at else None
        } for m in messages]

    @staticmethod
    async def delete_message(db: AsyncSession, message_id: int) -> Dict[str, Any]:
        message = await AdminMessageRepository.get_by_id(db, message_id)
        if not message:
            raise NotFoundError("Message not found")
        
        await db.delete(message)
        await db.commit()
        return {"success": True, "message": "Message deleted by admin"}

    @staticmethod
    async def get_message_analytics(db: AsyncSession, days: int) -> Dict[str, Any]:
        stats_raw = await AdminMessageRepository.get_analytics(db, days)
        
        most_active = []
        for user_id, count in stats_raw["most_active_raw"]:
            user = await AdminMessageRepository.get_user_by_id(db, user_id)
            if user:
                most_active.append({
                    "user_id": user_id,
                    "user_name": user.full_name,
                    "message_count": count
                })
                
        return {
            "total_messages": stats_raw["total_messages"],
            f"messages_last_{days}": stats_raw["recent_messages"],
            "most_active_senders": most_active,
            "daily_stats": stats_raw["daily_stats"]
        }
