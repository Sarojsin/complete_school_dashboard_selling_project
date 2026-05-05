"""
College Enrollment Schemas

Pydantic schemas for enrollment validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    semester_id: Optional[int] = None
    status: str = "enrolled"
    grade: Optional[str] = None
    grade_points: Optional[float] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    grade: Optional[str] = None
    grade_points: Optional[float] = None


class EnrollmentResponse(EnrollmentBase):
    id: int
    enrollment_date: Optional[date] = None

    model_config = {"from_attributes": True}


# For listings with student/course names (joined)
class EnrollmentDetail(EnrollmentResponse):
    student_name: Optional[str] = None
    student_roll: Optional[str] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None


__all__ = [
    "EnrollmentBase",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentDetail",
]
