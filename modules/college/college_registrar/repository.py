"""
College Registrar Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from .models import CollegeStudent, Enrollment, Program


class RegistrarRepository:
    """Repository for registrar operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_students(self) -> int:
        result = await self.db.execute(select(func.count(CollegeStudent.id)))
        return result.scalar() or 0

    async def count_programs(self) -> int:
        result = await self.db.execute(select(func.count(Program.id)))
        return result.scalar() or 0

    async def count_enrollments(self) -> int:
        result = await self.db.execute(select(func.count(Enrollment.id)))
        return result.scalar() or 0

    async def get_all_students(
        self,
        program_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegeStudent]:
        query = select(CollegeStudent)
        if program_id is not None:
            query = query.where(CollegeStudent.program_id == program_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_student(self, student_id: int) -> Optional[CollegeStudent]:
        result = await self.db.execute(
            select(CollegeStudent).where(CollegeStudent.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_student_enrollments(
        self,
        student_id: int,
        include_completed: bool = True
    ) -> List[Enrollment]:
        query = select(Enrollment).where(Enrollment.student_id == student_id)
        if not include_completed:
            query = query.where(Enrollment.status != "completed")
        query = query.order_by(Enrollment.enrollment_date.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_enrollments(
        self,
        student_id: Optional[int] = None,
        program_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Enrollment]:
        query = select(Enrollment)
        if student_id is not None:
            query = query.where(Enrollment.student_id == student_id)
        # Could join with CollegeStudent to filter by program
        if program_id is not None:
            # Need to join CollegeStudent
            from sqlalchemy import and_
            query = query.join(CollegeStudent).where(CollegeStudent.program_id == program_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


__all__ = ["RegistrarRepository"]
