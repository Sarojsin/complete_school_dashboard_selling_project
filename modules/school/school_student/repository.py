from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, Column
from sqlalchemy.sql import ClauseElement
from typing import List, Optional, Union
from .models import Student

class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id(self, student_id: int) -> Optional[Student]:
        result = await self.db.execute(select(Student).filter(Student.id == student_id))
        return result.scalars().first()
        
    async def get_by_user_id(self, user_id: Union[int, Column[int]]) -> Optional[Student]:
        result = await self.db.execute(select(Student).filter(Student.user_id == user_id))
        return result.scalars().first()
    
    async def get_by_student_id(self, student_id: str) -> Optional[Student]:
        result = await self.db.execute(select(Student).filter(Student.student_id == student_id))
        return result.scalars().first()
        
    async def list(self, skip: int = 0, limit: int = 100) -> List[Student]:
        result = await self.db.execute(select(Student).offset(skip).limit(limit))
        return list(result.scalars().all())
        
    async def create(self, student: Student) -> Student:
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student
        
    async def update(self, student: Student) -> Student:
        await self.db.commit()
        await self.db.refresh(student)
        return student
    
    async def delete(self, student_id: int) -> bool:
        student = await self.get_by_id(student_id)
        if student:
            await self.db.delete(student)
            await self.db.commit()
            return True
        return False
    
    async def get_by_teacher_id(self, teacher_id: int) -> List[Student]:
        """Get students taught by a specific teacher (via course enrollments)"""
        # Import here to avoid circular imports
        from modules.shared.models import User
        
        result = await self.db.execute(
            select(Student)
            .join(CourseEnrollment, CourseEnrollment.student_id == Student.id)
            .join(Course, Course.id == CourseEnrollment.course_id)
            .filter(Course.teacher_id == teacher_id)
            .distinct()
        )
        return list(result.scalars().all())
