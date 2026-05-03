from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, and_, func, case, desc
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from datetime import datetime
from backup.models.chat_models import ChatMessage
from backup.models.models import User, Parent, Student, CourseEnrollment, Course, Teacher

class ChatRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, message_id: int) -> Optional[ChatMessage]:
        result = await db.execute(select(ChatMessage).filter(ChatMessage.id == message_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_conversation(db: AsyncSession, user1_id: int, user2_id: int, 
                        limit: int = 50) -> List[ChatMessage]:
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
        return result.scalars().unique().all()
    
    @staticmethod
    async def create(db: AsyncSession, message_data: dict) -> ChatMessage:
        message = ChatMessage(**message_data)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message
    
    @staticmethod
    async def mark_as_read(db: AsyncSession, user1_id: int, user2_id: int):
        """Mark all messages from user2 to user1 as read"""
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
        """Get count of unread messages for a user"""
        result = await db.execute(
            select(func.count(ChatMessage.id)).filter(
                ChatMessage.receiver_id == user_id,
                ChatMessage.is_read == False
            )
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_conversations_list(db: AsyncSession, user_id: int) -> List[dict]:
        """Get list of users the current user has conversations with"""
        # Subquery to get last message timestamp for each conversation
        other_user_id_col = case(
            (ChatMessage.sender_id == user_id, ChatMessage.receiver_id),
            else_=ChatMessage.sender_id
        ).label('other_user_id')
        
        last_message_sub = select(
            other_user_id_col,
            func.max(ChatMessage.created_at).label('last_message_time')
        ).filter(
            or_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == user_id)
        ).group_by('other_user_id').subquery()
        
        # Get users and their last message time
        result = await db.execute(
            select(
                User,
                last_message_sub.c.last_message_time
            ).join(
                last_message_sub,
                User.id == last_message_sub.c.other_user_id
            ).order_by(
                desc(last_message_sub.c.last_message_time)
            )
        )
        conversations = result.all()
        
        final_result = []
        for user_obj, last_time in conversations:
            count_res = await db.execute(
                select(func.count(ChatMessage.id)).filter(
                    ChatMessage.sender_id == user_obj.id,
                    ChatMessage.receiver_id == user_id,
                    ChatMessage.is_read == False
                )
            )
            unread = count_res.scalar() or 0
            
            final_result.append({
                'user': user_obj,
                'last_message_time': last_time,
                'unread_count': unread
            })
        
        return final_result
    
    @staticmethod
    async def delete_expired(db: AsyncSession):
        """Delete expired messages"""
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

    @staticmethod
    async def get_parent_teachers(db: AsyncSession, parent_id: int) -> List[dict]:
        """Get all teachers associated with a parent's children"""
        # Get parent
        p_res = await db.execute(select(Parent).filter(Parent.id == parent_id))
        parent = p_res.scalars().first()
        if not parent:
            return []
            
        # Get parent's children
        c_res = await db.execute(select(Student).filter(Student.parent_id == parent_id))
        children = c_res.scalars().all()
        child_ids = [child.id for child in children]
        
        if not child_ids:
            return []
            
        # Get courses children are enrolled in
        e_res = await db.execute(
            select(CourseEnrollment).filter(CourseEnrollment.student_id.in_(child_ids))
        )
        enrollments = e_res.scalars().all()
        course_ids = [e.course_id for e in enrollments]
        
        if not course_ids:
            return []
            
        # Get teachers of these courses
        t_res = await db.execute(
            select(Teacher).options(joinedload(Teacher.user)).join(Course).filter(Course.id.in_(course_ids)).distinct()
        )
        teachers = t_res.scalars().all()
        
        # Format result
        final_result = []
        for teacher in teachers:
            # Get unread count
            unread_res = await db.execute(
                select(func.count(ChatMessage.id)).filter(
                    ChatMessage.sender_id == teacher.user_id,
                    ChatMessage.receiver_id == parent.user_id,
                    ChatMessage.is_read == False
                )
            )
            unread = unread_res.scalar() or 0
            
            final_result.append({
                'user': teacher.user,
                'teacher': teacher,
                'unread_count': unread
            })
            
        return final_result

    @staticmethod
    async def get_teacher_parents(db: AsyncSession, teacher_id: int) -> List[dict]:
        """Get all parents of students taught by a teacher"""
        # Get teacher
        t_res = await db.execute(select(Teacher).filter(Teacher.id == teacher_id))
        teacher = t_res.scalars().first()
        if not teacher:
            return []
            
        # Get courses taught by teacher
        co_res = await db.execute(select(Course).filter(Course.teacher_id == teacher_id))
        courses = co_res.scalars().all()
        course_ids = [c.id for c in courses]
        
        if not course_ids:
            return []
            
        # Get students enrolled in these courses
        e_res = await db.execute(
            select(CourseEnrollment).filter(CourseEnrollment.course_id.in_(course_ids))
        )
        enrollments = e_res.scalars().all()
        student_ids = [e.student_id for e in enrollments]
        
        if not student_ids:
            return []
            
        # Get parents of these students
        p_res = await db.execute(
            select(Parent).options(
                joinedload(Parent.user),
                selectinload(Parent.children).joinedload(Student.user)
            ).join(Student).filter(
                Student.id.in_(student_ids),
                Student.parent_id.isnot(None)
            ).distinct()
        )
        parents = p_res.scalars().all()
        
        # Format result
        final_result = []
        for parent in parents:
            # Get unread count
            unread_res = await db.execute(
                select(func.count(ChatMessage.id)).filter(
                    ChatMessage.sender_id == parent.user_id,
                    ChatMessage.receiver_id == teacher.user_id,
                    ChatMessage.is_read == False
                )
            )
            unread = unread_res.scalar() or 0
            
            final_result.append({
                'user': parent.user,
                'parent': parent,
                'unread_count': unread
            })
            
        return final_result

    @staticmethod
    async def get_all_teachers(db: AsyncSession, parent_id: int) -> List[dict]:
        """Get all teachers in the system for a parent to contact"""
        # Get parent
        p_res = await db.execute(select(Parent).filter(Parent.id == parent_id))
        parent = p_res.scalars().first()
        if not parent:
            return []
            
        # Get all teachers
        t_res = await db.execute(select(Teacher).options(joinedload(Teacher.user)))
        teachers = t_res.scalars().all()
        
        # Format result
        final_result = []
        for teacher in teachers:
            # Get unread count
            unread_res = await db.execute(
                select(func.count(ChatMessage.id)).filter(
                    ChatMessage.sender_id == teacher.user_id,
                    ChatMessage.receiver_id == parent.user_id,
                    ChatMessage.is_read == False
                )
            )
            unread = unread_res.scalar() or 0
            
            final_result.append({
                'user': teacher.user,
                'teacher': teacher,
                'unread_count': unread
            })
            
        return final_result