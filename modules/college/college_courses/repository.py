"""
College Course Repository

Database CRUD operations for college courses.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from modules.college.college_courses.models import CollegeCourse


class CollegeCourseRepository:
    """Repository for course operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, course_code: str, course_name: str,
                    department_id: Optional[int] = None, instructor_id: Optional[int] = None,
                    semester_id: Optional[int] = None, credits: int = None,
                    course_type: str = None, description: str = None) -> CollegeCourse:
        """Create a new course"""
        course = CollegeCourse(
            course_code=course_code,
            course_name=course_name,
            department_id=department_id,
            instructor_id=instructor_id,
            semester_id=semester_id,
            credits=credits,
            course_type=course_type,
            description=description
        )
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def get(self, course_id: int) -> Optional[CollegeCourse]:
        """Get course by ID"""
        result = await self.db.execute(
            select(CollegeCourse).where(CollegeCourse.id == course_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, course_code: str) -> Optional[CollegeCourse]:
        """Get course by code"""
        result = await self.db.execute(
            select(CollegeCourse).where(CollegeCourse.course_code == course_code)
        )
        return result.scalar_one_or_none()

    async def list(self, department_id: Optional[int] = None, semester_id: Optional[int] = None,
                   skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        """List courses with filters"""
        query = select(CollegeCourse)

        if department_id:
            query = query.where(CollegeCourse.department_id == department_id)
        if semester_id:
            query = query.where(CollegeCourse.semester_id == semester_id)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, department_id: Optional[int] = None, semester_id: Optional[int] = None) -> int:
        """Count courses"""
        query = select(func.count(CollegeCourse.id))

        if department_id:
            query = query.where(CollegeCourse.department_id == department_id)
        if semester_id:
            query = query.where(CollegeCourse.semester_id == semester_id)

        result = await self.db.execute(query)
        return result.scalar() or 0

    async def update(self, course_id: int, **kwargs) -> Optional[CollegeCourse]:
        """Update course"""
        course = await self.get(course_id)
        if course:
            for key, value in kwargs.items():
                if value is not None and hasattr(course, key):
                    setattr(course, key, value)
            await self.db.commit()
            await self.db.refresh(course)
        return course

    async def delete(self, course_id: int) -> bool:
        """Delete course"""
        course = await self.get(course_id)
        if course:
            await self.db.delete(course)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeCourseRepository"]