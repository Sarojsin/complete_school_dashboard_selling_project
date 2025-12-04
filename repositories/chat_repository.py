from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from models.chat_models import ChatMessage

class ChatRepository:
    @staticmethod
    def get_by_id(db: Session, message_id: int) -> Optional[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    @staticmethod
    def get_conversation(db: Session, user1_id: int, user2_id: int, 
                        limit: int = 50) -> List[ChatMessage]:
        """Get messages between two users"""
        return db.query(ChatMessage).options(
            joinedload(ChatMessage.sender),
            joinedload(ChatMessage.receiver)
        ).filter(
            or_(
                and_(ChatMessage.sender_id == user1_id, ChatMessage.receiver_id == user2_id),
                and_(ChatMessage.sender_id == user2_id, ChatMessage.receiver_id == user1_id)
            )
        ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def create(db: Session, message_data: dict) -> ChatMessage:
        message = ChatMessage(**message_data)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def mark_as_read(db: Session, user1_id: int, user2_id: int):
        """Mark all messages from user2 to user1 as read"""
        db.query(ChatMessage).filter(
            ChatMessage.sender_id == user2_id,
            ChatMessage.receiver_id == user1_id,
            ChatMessage.is_read == False
        ).update({"is_read": True})
        db.commit()
    
    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """Get count of unread messages for a user"""
        return db.query(ChatMessage).filter(
            ChatMessage.receiver_id == user_id,
            ChatMessage.is_read == False
        ).count()
    
    @staticmethod
    def get_conversations_list(db: Session, user_id: int) -> List[dict]:
        """Get list of users the current user has conversations with"""
        from sqlalchemy import func, case
        from models.models import User
        
        # Subquery to get last message timestamp for each conversation
        last_message = db.query(
            case(
                (ChatMessage.sender_id == user_id, ChatMessage.receiver_id),
                else_=ChatMessage.sender_id
            ).label('other_user_id'),
            func.max(ChatMessage.created_at).label('last_message_time')
        ).filter(
            or_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == user_id)
        ).group_by('other_user_id').subquery()
        
        # Get users and their last message time
        conversations = db.query(
            User,
            last_message.c.last_message_time
        ).join(
            last_message,
            User.id == last_message.c.other_user_id
        ).order_by(
            last_message.c.last_message_time.desc()
        ).all()
        
        result = []
        for user, last_time in conversations:
            unread = db.query(ChatMessage).filter(
                ChatMessage.sender_id == user.id,
                ChatMessage.receiver_id == user_id,
                ChatMessage.is_read == False
            ).count()
            
            result.append({
                'user': user,
                'last_message_time': last_time,
                'unread_count': unread
            })
        
        return result
    
    @staticmethod
    def delete_expired(db: Session):
        """Delete expired messages"""
        now = datetime.utcnow()
        deleted = db.query(ChatMessage).filter(
            ChatMessage.expires_at < now
        ).delete()
        db.commit()
        return deleted
    
    @staticmethod
    def search_messages(db: Session, user_id: int, query: str) -> List[ChatMessage]:
        """Search messages for a user"""
        search_pattern = f"%{query}%"
        return db.query(ChatMessage).filter(
            or_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == user_id),
            ChatMessage.content.ilike(search_pattern)
        ).order_by(ChatMessage.created_at.desc()).limit(50).all()

    @staticmethod
    def get_parent_teachers(db: Session, parent_id: int) -> List[dict]:
        """Get all teachers associated with a parent's children"""
        from models.models import Parent, Student, CourseEnrollment, Course, Teacher, User
        
        # Get parent to access user_id
        parent = db.query(Parent).filter(Parent.id == parent_id).first()
        if not parent:
            return []
            
        # Get parent's children
        children = db.query(Student).filter(Student.parent_id == parent_id).all()
        child_ids = [child.id for child in children]
        
        if not child_ids:
            return []
            
        # Get courses children are enrolled in
        enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id.in_(child_ids)
        ).all()
        
        course_ids = [e.course_id for e in enrollments]
        
        if not course_ids:
            return []
            
        # Get teachers of these courses
        teachers = db.query(Teacher).join(Course).filter(
            Course.id.in_(course_ids)
        ).distinct().all()
        
        # Format result
        result = []
        for teacher in teachers:
            # Get unread count
            unread = db.query(ChatMessage).filter(
                ChatMessage.sender_id == teacher.user_id,
                ChatMessage.receiver_id == parent.user_id,
                ChatMessage.is_read == False
            ).count()
            
            result.append({
                'user': teacher.user,
                'teacher': teacher,
                'unread_count': unread
            })
            
        return result

    @staticmethod
    def get_teacher_parents(db: Session, teacher_id: int) -> List[dict]:
        """Get all parents of students taught by a teacher"""
        from models.models import Teacher, Course, CourseEnrollment, Student, Parent, User
        
        # Get teacher to access user_id
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            return []
            
        # Get courses taught by teacher
        courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()
        course_ids = [c.id for c in courses]
        
        if not course_ids:
            return []
            
        # Get students enrolled in these courses
        enrollments = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id.in_(course_ids)
        ).all()
        
        student_ids = [e.student_id for e in enrollments]
        
        if not student_ids:
            return []
            
        # Get parents of these students
        parents = db.query(Parent).join(Student).filter(
            Student.id.in_(student_ids),
            Student.parent_id.isnot(None)
        ).distinct().all()
        
        # Format result
        result = []
        for parent in parents:
            # Get unread count
            unread = db.query(ChatMessage).filter(
                ChatMessage.sender_id == parent.user_id,
                ChatMessage.receiver_id == teacher.user_id,
                ChatMessage.is_read == False
            ).count()
            
            result.append({
                'user': parent.user,
                'parent': parent,
                'unread_count': unread
            })
            
        return result

    @staticmethod
    def get_all_teachers(db: Session, parent_id: int) -> List[dict]:
        """Get all teachers in the system for a parent to contact"""
        from models.models import Parent, Teacher, User
        
        # Get parent to access user_id
        parent = db.query(Parent).filter(Parent.id == parent_id).first()
        if not parent:
            return []
            
        # Get all teachers
        teachers = db.query(Teacher).all()
        
        # Format result
        result = []
        for teacher in teachers:
            # Get unread count
            unread = db.query(ChatMessage).filter(
                ChatMessage.sender_id == teacher.user_id,
                ChatMessage.receiver_id == parent.user_id,
                ChatMessage.is_read == False
            ).count()
            
            result.append({
                'user': teacher.user,
                'teacher': teacher,
                'unread_count': unread
            })
            
        return result