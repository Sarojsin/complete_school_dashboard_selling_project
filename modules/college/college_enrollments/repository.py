"""
College Enrollment Repository

Async CRUD operations for course enrollments.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from .models import CollegeEnrollment
from .schemas import EnrollmentCreate, EnrollmentUpdate


class CollegeEnrollmentRepository:
    """Repository for enrollment operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: EnrollmentCreate) -> CollegeEnrollment:
        """Enroll a student in a course"""
        # Check duplicates
        existing = await self.get_by_student_course_semester(
            data.student_id, data.course_id, data.semester_id
        )
        if existing:
            raise ValueError("Student already enrolled in this course for the semester")

        enrollment = CollegeEnrollment(**data.model_dump())
        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def get(self, enrollment_id: int) -> Optional[CollegeEnrollment]:
        """Get enrollment by ID"""
        result = await self.db.execute(
            select(CollegeEnrollment).where(CollegeEnrollment.id == enrollment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_student_course_semester(
        self, student_id: int, course_id: int, semester_id: Optional[int] = None
    ) -> Optional[CollegeEnrollment]:
        """Check if student already enrolled in this course/semester"""
        query = select(CollegeEnrollment).where(
            CollegeEnrollment.student_id == student_id,
            CollegeEnrollment.course_id == course_id
        )
        if semester_id is not None:
            query = query.where(CollegeEnrollment.semester_id == semester_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_student(self, student_id: int) -> List[CollegeEnrollment]:
        """Get all enrollments for a student"""
        result = await self.db.execute(
            select(CollegeEnrollment)
            .where(CollegeEnrollment.student_id == student_id)
            .order_by(CollegeEnrollment.enrollment_date.desc())
        )
        return list(result.scalars().all())

    async def get_by_course(self, course_id: int) -> List[CollegeEnrollment]:
        """Get all enrollments for a course"""
        result = await self.db.execute(
            select(CollegeEnrollment)
            .where(CollegeEnrollment.course_id == course_id)
            .order_by(CollegeEnrollment.enrollment_date.desc())
        )
        return list(result.scalars().all())

    async def get_all(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegeEnrollment]:
        """Get all enrollments with optional filters"""
        query = select(CollegeEnrollment)

        if student_id is not None:
            query = query.where(CollegeEnrollment.student_id == student_id)
        if course_id is not None:
            query = query.where(CollegeEnrollment.course_id == course_id)
        if semester_id is not None:
            query = query.where(CollegeEnrollment.semester_id == semester_id)

        query = query.order_by(CollegeEnrollment.enrollment_date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, enrollment_id: int, data: EnrollmentUpdate) -> Optional[CollegeEnrollment]:
        """Update enrollment (status, grade)"""
        enrollment = await self.get(enrollment_id)
        if not enrollment:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(enrollment, key, value)

        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def delete(self, enrollment_id: int) -> bool:
        """Drop/delete an enrollment"""
        enrollment = await self.get(enrollment_id)
        if enrollment:
            await self.db.delete(enrollment)
            await self.db.commit()
            return True
        return False

    async def count(self, course_id: Optional[int] = None, semester_id: Optional[int] = None) -> int:
        """Count enrollments"""
        query = select(func.count(CollegeEnrollment.id))
        if course_id is not None:
            query = query.where(CollegeEnrollment.course_id == course_id)
        if semester_id is not None:
            query = query.where(CollegeEnrollment.semester_id == semester_id)
        result = await self.db.execute(query)
        return result.scalar() or 0


__all__ = ["CollegeEnrollmentRepository"]
