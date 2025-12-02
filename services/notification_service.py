from sqlalchemy.orm import Session
from typing import List, Dict
from repositories.notice_repository import NoticeRepository

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.notice_repo = NoticeRepository(db)

    def send_bulk_notification(self, title: str, content: str, target_audience: str, author_id: int) -> Dict:
        """Send notification to multiple users"""
        from tables.tables import NoticeCreate
        
        notice_data = NoticeCreate(
            title=title,
            content=content,
            target_audience=target_audience
        )
        
        notice = self.notice_repo.create(notice_data, author_id)
        
        # In a real application, you might also:
        # - Send email notifications
        # - Send push notifications
        # - Update user notification feeds
        
        return {
            'message': f'Notification sent to {target_audience}',
            'notice_id': notice.id,
            'recipients_count': self._estimate_recipient_count(target_audience)
        }

    def _estimate_recipient_count(self, target_audience: str) -> int:
        """Estimate how many users will receive the notification"""
        from models.models import User, Student
        
        if target_audience == 'all':
            return self.db.query(User).count()
        elif target_audience == 'students':
            return self.db.query(Student).count()
        elif target_audience == 'teachers':
            return self.db.query(User).filter(User.role == 'teacher').count()
        elif target_audience == 'authority':
            return self.db.query(User).filter(User.role == 'authority').count()
        else:
            # Assume it's a specific grade
            return self.db.query(Student).filter(Student.grade == target_audience).count()

    def get_unread_notifications(self, user_id: int, user_role: str, user_grade: str = None) -> List[Dict]:
        """Get unread notifications for a user"""
        notices = self.notice_repo.get_for_user(user_role, user_grade)
        
        # Mark as read logic would go here
        # For now, return all relevant notices
        
        return [{
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'author': notice.author.full_name,
            'created_at': notice.created_at,
            'is_urgent': 'urgent' in notice.title.lower()
        } for notice in notices[:10]]  # Return last 10 notices