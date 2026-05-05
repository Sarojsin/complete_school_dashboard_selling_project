"""
School HOD Repository

Async CRUD operations for HOD queries.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from typing import Optional, List
from .models import Teacher
from modules.school.school_courses.models import SchoolCourse
from modules.school.school_student.models import Student


class HODRepository:
    """Repository for HOD-related queries"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_teacher_by_user_id(self, user_id: int) -> Optional[Teacher]:
        """Get teacher profile for a user"""
        result = await self.db.execute(
            select(Teacher).where(Teacher.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_department_name(self, teacher: Teacher) -> str:
        """Get department name from teacher"""
        return teacher.department or "Unknown"

    async def count_teachers_in_department(self, department: str) -> int:
        """Count teachers in a department"""
        result = await self.db.execute(
            select(func.count(Teacher.id)).where(Teacher.department == department)
        )
        return result.scalar() or 0

    async def count_students_in_department(self) -> int:
        """Count all students in school (HOD view: all students)"""
        result = await self.db.execute(select(func.count(Student.id)))
        return result.scalar() or 0

    async def count_courses_in_department(self, department: str) -> int:
        """Count courses in department (by grade_level mapping)"""
        result = await self.db.execute(
            select(func.count(SchoolCourse.id)).where(SchoolCourse.grade_level == department)
        )
        return result.scalar() or 0

    async def get_all_departments(self) -> List[str]:
        """Get distinct list of department names from teachers"""
        result = await self.db.execute(
            select(distinct(Teacher.department)).where(Teacher.department != None)
        )
        return list(result.scalars().all())

    async def get_teachers_in_department(self, department: str) -> List[Teacher]:
        """Get all teachers in a department"""
        result = await self.db.execute(
            select(Teacher).where(Teacher.department == department)
        )
        return list(result.scalars().all())

    async def get_courses_in_department(self, department: str) -> List[SchoolCourse]:
        """Get all courses assigned to a department"""
        result = await self.db.execute(
            select(SchoolCourse).where(SchoolCourse.grade_level == department)
        )
        return list(result.scalars().all())


__all__ = ["HODRepository"]
