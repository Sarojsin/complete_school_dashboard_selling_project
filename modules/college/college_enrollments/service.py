"""
College Enrollment Service

Business logic for course enrollment management.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import CollegeEnrollmentRepository
from .schemas import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse, EnrollmentDetail
from modules.shared.exceptions import NotFoundError, ForbiddenError, ValidationError


class CollegeEnrollmentService:
    """Service for enrollment operations"""

    def __init__(self, db: AsyncSession):
        self.repository = CollegeEnrollmentRepository(db)

    async def enroll_student(self, data: EnrollmentCreate) -> Dict[str, Any]:
        """Enroll a student in a course (with validation)"""
        # Validate student exists (via repository will fail if not, but we can pre-check)
        # Validate course exists, capacity not exceeded, prerequisites met
        try:
            enrollment = await self.repository.create(data)
            return {"enrollment": EnrollmentResponse.model_validate(enrollment)}
        except ValueError as e:
            raise ValidationError(str(e))

    async def get_enrollment(self, enrollment_id: int) -> Dict[str, Any]:
        """Get single enrollment"""
        enrollment = await self.repository.get(enrollment_id)
        if not enrollment:
            raise NotFoundError("Enrollment not found")
        return {"enrollment": EnrollmentResponse.model_validate(enrollment)}

    async def list_enrollments(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EnrollmentResponse]:
        """List enrollments with filters"""
        enrollments = await self.repository.get_all(student_id, course_id, semester_id, skip, limit)
        return [EnrollmentResponse.model_validate(e) for e in enrollments]

    async def get_student_enrollments(self, student_id: int) -> List[EnrollmentResponse]:
        """Get all enrollments for a student"""
        enrollments = await self.repository.get_by_student(student_id)
        return [EnrollmentResponse.model_validate(e) for e in enrollments]

    async def get_course_enrollments(self, course_id: int) -> List[EnrollmentResponse]:
        """Get all students enrolled in a course"""
        enrollments = await self.repository.get_by_course(course_id)
        return [EnrollmentResponse.model_validate(e) for e in enrollments]

    async def update_enrollment(self, enrollment_id: int, data: EnrollmentUpdate) -> Dict[str, Any]:
        """Update enrollment status or grade"""
        enrollment = await self.repository.update(enrollment_id, data)
        if not enrollment:
            raise NotFoundError("Enrollment not found")
        return {"enrollment": EnrollmentResponse.model_validate(enrollment)}

    async def drop_course(self, enrollment_id: int) -> Dict[str, str]:
        """Drop a course enrollment (delete)"""
        success = await self.repository.delete(enrollment_id)
        if not success:
            raise NotFoundError("Enrollment not found")
        return {"message": "Course dropped successfully"}

    async def get_enrollment_stats(self, course_id: Optional[int] = None, semester_id: Optional[int] = None) -> Dict[str, Any]:
        """Get enrollment statistics"""
        count = await self.repository.count(course_id, semester_id)
        # Could also add breakdown by status
        return {"total_enrollments": count}


__all__ = ["EnrollmentService"]
