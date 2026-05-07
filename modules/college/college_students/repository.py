"""
College Student Repository

Database CRUD operations for college students.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from modules.college.college_students.models import CollegeStudent


class CollegeStudentRepository:
    """Repository for student operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, roll_number: str, first_name: str, last_name: str,
                    email: str, program_id: Optional[int] = None,
                    semester_id: Optional[int] = None, phone: str = None,
                    date_of_birth: str = None, gender: str = None,
                    address: str = None, enrollment_year: int = None) -> CollegeStudent:
        """Create a new student"""
        student = CollegeStudent(
            user_id=user_id,
            roll_number=roll_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            program_id=program_id,
            semester_id=semester_id,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            enrollment_year=enrollment_year
        )
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def get(self, student_id: int) -> Optional[CollegeStudent]:
        """Get student by ID (excludes soft-deleted)"""
        result = await self.db.execute(
            select(CollegeStudent).where(
                CollegeStudent.id == student_id,
                CollegeStudent.is_deleted == False
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[CollegeStudent]:
        """Get student by user ID"""
        result = await self.db.execute(
            select(CollegeStudent).where(CollegeStudent.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_roll_number(self, roll_number: str) -> Optional[CollegeStudent]:
        """Get student by roll number"""
        result = await self.db.execute(
            select(CollegeStudent).where(CollegeStudent.roll_number == roll_number)
        )
        return result.scalar_one_or_none()

    async def list(self, program_id: Optional[int] = None, semester_id: Optional[int] = None,
                   skip: int = 0, limit: int = 100) -> List[CollegeStudent]:
        """List students with filters (excludes soft-deleted)"""
        query = select(CollegeStudent).where(CollegeStudent.is_deleted == False)

        if program_id:
            query = query.where(CollegeStudent.program_id == program_id)
        if semester_id:
            query = query.where(CollegeStudent.semester_id == semester_id)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, program_id: Optional[int] = None, semester_id: Optional[int] = None) -> int:
        """Count students (excludes soft-deleted)"""
        query = select(func.count(CollegeStudent.id)).where(CollegeStudent.is_deleted == False)

        if program_id:
            query = query.where(CollegeStudent.program_id == program_id)
        if semester_id:
            query = query.where(CollegeStudent.semester_id == semester_id)

        result = await self.db.execute(query)
        return result.scalar() or 0

    async def update(self, student_id: int, **kwargs) -> Optional[CollegeStudent]:
        """Update student"""
        student = await self.get(student_id)
        if student:
            for key, value in kwargs.items():
                if value is not None and hasattr(student, key):
                    setattr(student, key, value)
            await self.db.commit()
            await self.db.refresh(student)
        return student

    async def soft_delete(self, student_id: int) -> bool:
        """Soft delete student"""
        student = await self.get(student_id)
        if student:
            await student.soft_delete(self.db)
            return True
        return False

    async def delete(self, student_id: int) -> bool:
        """Hard delete student (not recommended)"""
        student = await self.get(student_id)
        if student:
            await self.db.delete(student)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeStudentRepository"]