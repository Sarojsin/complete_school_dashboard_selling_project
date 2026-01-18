from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict
from repositories.notice_repository import NoticeRepository

class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notice_repo = NoticeRepository(db)

    async def send_bulk_notification(self, title: str, content: str, target_audience: str, author_id: int) -> Dict:
        """Send notification to multiple users"""
        from tables.tables import NoticeCreate
        
        notice_data = NoticeCreate(
            title=title,
            content=content,
            target_audience=target_audience
        )
        
        notice = await self.notice_repo.create(notice_data, author_id)
        
        return {
            'message': f'Notification sent to {target_audience}',
            'notice_id': notice.id,
            'recipients_count': await self._estimate_recipient_count(target_audience)
        }

    async def _estimate_recipient_count(self, target_audience: str) -> int:
        """Estimate how many users will receive the notification"""
        from models.models import User, Student
        
        if target_audience == 'all':
            res = await self.db.execute(select(func.count(User.id)))
            return res.scalar() or 0
        elif target_audience == 'students':
            res = await self.db.execute(select(func.count(Student.id)))
            return res.scalar() or 0
        elif target_audience == 'teachers':
            res = await self.db.execute(select(func.count(User.id)).filter(User.role == 'teacher'))
            return res.scalar() or 0
        elif target_audience == 'authority':
            res = await self.db.execute(select(func.count(User.id)).filter(User.role == 'authority'))
            return res.scalar() or 0
        else:
            # Assume it's a specific grade
            res = await self.db.execute(select(func.count(Student.id)).filter(Student.grade_level == target_audience))
            return res.scalar() or 0

    async def get_unread_notifications(self, user_id: int, user_role: str, user_grade: str = None) -> List[Dict]:
        """Get unread notifications for a user"""
        notices = await self.notice_repo.get_for_user(user_role, user_grade)
        
        return [{
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'author': notice.author.full_name if notice.author else "System",
            'created_at': notice.created_at,
            'is_urgent': 'urgent' in notice.title.lower() if notice.title else False
        } for notice in notices[:10]]  # Return last 10 notices