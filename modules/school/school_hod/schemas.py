"""
School HOD Schemas

Pydantic schemas for HOD endpoints.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DepartmentSchema(BaseModel):
    """Schema for department listing"""
    name: str


class TeacherShortSchema(BaseModel):
    """Compact teacher schema for HOD department view"""
    id: int
    user_id: int
    employee_id: str
    full_name: Optional[str] = None
    department: str
    designation: Optional[str] = None

    model_config = {"from_attributes": True}


class CourseSchema(BaseModel):
    """Course schema for HOD department view"""
    id: int
    title: str
    grade_level: Optional[str] = None
    subject_code: Optional[str] = None

    model_config = {"from_attributes": True}


class HODDashboardSchema(BaseModel):
    """Response for HOD dashboard"""
    department: str
    total_teachers: int
    total_students: int
    total_courses: int


class DepartmentListResponse(BaseModel):
    """List of distinct departments"""
    departments: List[DepartmentSchema]


class TeacherListResponse(BaseModel):
    """Teachers in HOD's department"""
    teachers: List[TeacherShortSchema]


class CourseListResponse(BaseModel):
    """Courses in HOD's department"""
    courses: List[CourseSchema]


__all__ = [
    "DepartmentSchema",
    "TeacherShortSchema",
    "CourseSchema",
    "HODDashboardSchema",
    "DepartmentListResponse",
    "TeacherListResponse",
    "CourseListResponse",
]
