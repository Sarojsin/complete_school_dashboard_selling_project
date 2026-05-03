"""
Student Repository

Data access layer for student.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.models.college import CollegeStudent


class StudentRepository:
    """Repository for student data access"""
    
    async def get_by_id(self, db: AsyncSession, student_id: int):
        """Get student by ID"""
        result = await db.execute(
            select(CollegeStudent).where(CollegeStudent.id == student_id)
        )
        return result.scalars().first()
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        """Get student by user ID"""
        result = await db.execute(
            select(CollegeStudent).where(CollegeStudent.user_id == user_id)
        )
        return result.scalars().first()
    
    async def get_by_student_id(self, db: AsyncSession, student_id: str):
        """Get student by student ID"""
        result = await db.execute(
            select(CollegeStudent).where(CollegeStudent.student_id == student_id)
        )
        return result.scalars().first()
    
    async def get_by_program(self, db: AsyncSession, program_id: int, skip: int = 0, limit: int = 100):
        """Get students by program"""
        result = await db.execute(
            select(CollegeStudent)
            .where(CollegeStudent.program_id == program_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_semester(self, db: AsyncSession, semester_id: int, skip: int = 0, limit: int = 100):
        """Get students by semester"""
        result = await db.execute(
            select(CollegeStudent)
            .where(CollegeStudent.semester_id == semester_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all students"""
        result = await db.execute(
            select(CollegeStudent).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_count(self, db: AsyncSession):
        """Get total count of students"""
        result = await db.execute(select(CollegeStudent))
        return len(result.scalars().all())
    
    async def create(self, db: AsyncSession, student_data: dict):
        """Create new student"""
        student = CollegeStudent(**student_data)
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student
    
    async def update(self, db: AsyncSession, student_id: int, student_data: dict):
        """Update student"""
        student = await self.get_by_id(db, student_id)
        if student:
            for key, value in student_data.items():
                if value is not None:
                    setattr(student, key, value)
            await db.commit()
            await db.refresh(student)
        return student
    
    async def delete(self, db: AsyncSession, student_id: int):
        """Delete student"""
        student = await self.get_by_id(db, student_id)
        if student:
            await db.delete(student)
            await db.commit()
        return student
