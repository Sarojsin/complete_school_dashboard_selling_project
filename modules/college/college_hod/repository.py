"""
College HOD Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from .models import Department, Faculty, CollegeCourse


class HodRepository:
    """Repository for HOD operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_departments_by_hod(self, hod_user_id: int) -> List[Department]:
        """Get departments where user is HOD"""
        result = await self.db.execute(
            select(Department).where(Department.hod_teacher_id == hod_user_id)
        )
        return list(result.scalars().all())

    async def get_department_by_id(self, dept_id: int) -> Optional[Department]:
        """Get department by ID"""
        result = await self.db.execute(select(Department).where(Department.id == dept_id))
        return result.scalar_one_or_none()

    async def get_faculty_by_department(self, department_id: int) -> List[Faculty]:
        """Get all faculty members in a department"""
        result = await self.db.execute(
            select(Faculty).where(Faculty.department_id == department_id)
        )
        return list(result.scalars().all())

    async def get_courses_by_department(self, department_id: int) -> List[CollegeCourse]:
        """Get all courses in a department"""
        result = await self.db.execute(
            select(CollegeCourse).where(CollegeCourse.department_id == department_id)
        )
        return list(result.scalars().all())

    async def count_faculty(self, department_id: int) -> int:
        """Count faculty in department"""
        result = await self.db.execute(
            select(func.count(Faculty.id)).where(Faculty.department_id == department_id)
        )
        return result.scalar() or 0


__all__ = ["HodRepository"]
