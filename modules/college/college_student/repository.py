"""
College Student Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from backup.models.college.student import CollegeStudent


class CollegeStudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, roll_number: str, program_id: int,
                   semester_id: int = None) -> CollegeStudent:
        student = CollegeStudent(
            user_id=user_id,
            roll_number=roll_number,
            program_id=program_id,
            semester_id=semester_id
        )
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student
    
    async def get(self, student_id: int) -> Optional[CollegeStudent]:
        result = await self.db.execute(
            select(CollegeStudent).where(CollegeStudent.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[CollegeStudent]:
        """Get college student by user_id (for /me endpoint)"""
        result = await self.db.execute(
            select(CollegeStudent).where(CollegeStudent.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def list(self, program_id: Optional[int] = None, semester_id: Optional[int] = None,
                  skip: int = 0, limit: int = 100) -> List[CollegeStudent]:
        query = select(CollegeStudent)
        if program_id:
            query = query.where(CollegeStudent.program_id == program_id)
        if semester_id:
            query = query.where(CollegeStudent.semester_id == semester_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count(self, program_id: Optional[int] = None) -> int:
        query = select(func.count(CollegeStudent.id))
        if program_id:
            query = query.where(CollegeStudent.program_id == program_id)
        result = await self.db.execute(query)
        return result.scalar() or 0


__all__ = ["CollegeStudentRepository"]
