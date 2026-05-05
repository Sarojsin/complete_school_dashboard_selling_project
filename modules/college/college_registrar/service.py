"""
College Registrar Service

Business logic for academic records and enrollment management.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .repository import RegistrarRepository
from .schemas import (
    RegistrarDashboardResponse,
    StudentDetailSchema,
    EnrollmentDetailSchema,
    StudentAcademicRecord
)
from modules.shared.exceptions import NotFoundError, ForbiddenError


class RegistrarService:
    """Service for registrar operations"""

    def __init__(self, db: AsyncSession):
        self.repository = RegistrarRepository(db)

    async def get_dashboard(self) -> Dict[str, Any]:
        """Get registrar dashboard statistics"""
        stats = RegistrarDashboardResponse(
            total_students=await self.repository.count_students(),
            total_programs=await self.repository.count_programs(),
            active_enrollments=await self.repository.count_enrollments()
        )
        return {"stats": stats}

    async def get_student_detail(self, student_id: int) -> Dict[str, Any]:
        """Get detailed student record with enrollments"""
        student = await self.repository.get_student(student_id)
        if not student:
            raise NotFoundError("Student not found")

        enrollments = await self.repository.get_student_enrollments(student_id)

        return {
            "student": StudentDetailSchema.model_validate(student),
            "enrollments": [EnrollmentDetailSchema.model_validate(e) for e in enrollments]
        }

    async def list_students(
        self,
        program_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[StudentDetailSchema]:
        students = await self.repository.get_all_students(program_id, skip, limit)
        return [StudentDetailSchema.model_validate(s) for s in students]

    async def list_enrollments(
        self,
        student_id: Optional[int] = None,
        program_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EnrollmentDetailSchema]:
        enrollments = await self.repository.get_all_enrollments(student_id, program_id, skip, limit)
        return [EnrollmentDetailSchema.model_validate(e) for e in enrollments]

    async def get_academic_record(self, student_id: int) -> StudentAcademicRecord:
        """Get full academic record (transcript-style)"""
        student = await self.repository.get_student(student_id)
        if not student:
            raise NotFoundError("Student not found")

        enrollments = await self.repository.get_student_enrollments(student_id)
        completed = [e for e in enrollments if e.status == "completed" and e.grade_points]
        total_courses = len(enrollments)
        completed_courses = len(completed)

        current_cgpa = student.cgpa if student.cgpa else None

        record = StudentAcademicRecord(
            student=StudentDetailSchema.model_validate(student),
            enrollments=[EnrollmentDetailSchema.model_validate(e) for e in enrollments],
            total_courses=total_courses,
            completed_courses=completed_courses,
            current_cgpa=current_cgpa
        )
        return record


__all__ = ["RegistrarService"]
