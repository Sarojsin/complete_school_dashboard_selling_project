"""
College Registrar Schemas
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class RegistrarDashboardResponse(BaseModel):
    total_students: int
    total_programs: int
    active_enrollments: int


class StudentDetailSchema(BaseModel):
    id: int
    user_id: int
    roll_number: str
    cgpa: Optional[float] = None
    total_credits_completed: Optional[int] = None
    program_name: Optional[str] = None
    program_code: Optional[str] = None
    semester_name: Optional[str] = None

    model_config = {"from_attributes": True}


class EnrollmentDetailSchema(BaseModel):
    id: int
    student_id: int
    course_id: int
    semester_id: Optional[int] = None
    enrollment_date: Optional[str] = None
    status: str
    grade: Optional[str] = None
    grade_points: Optional[float] = None

    model_config = {"from_attributes": True}


class StudentAcademicRecord(BaseModel):
    student: StudentDetailSchema
    enrollments: List[EnrollmentDetailSchema] = []
    total_courses: int = 0
    completed_courses: int = 0
    current_cgpa: Optional[float] = None


__all__ = [
    "RegistrarDashboardResponse",
    "StudentDetailSchema",
    "EnrollmentDetailSchema",
    "StudentAcademicRecord",
]
