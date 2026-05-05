"""
College HOD Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DepartmentSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class FacultySchema(BaseModel):
    id: int
    user_id: int
    employee_id: str
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

    model_config = {"from_attributes": True}


class CourseSchema(BaseModel):
    id: int
    code: str
    name: str
    credits: Optional[int] = None

    model_config = {"from_attributes": True}


class HODDashboardResponse(BaseModel):
    departments_count: int
    departments: List[DepartmentSchema] = []
    # Could extend: total_faculty, total_courses, total_students per dept


class DepartmentDetailResponse(DepartmentSchema):
    faculty_count: Optional[int] = None
    programs_count: Optional[int] = None


__all__ = [
    "DepartmentSchema",
    "FacultySchema",
    "CourseSchema",
    "HODDashboardResponse",
    "DepartmentDetailResponse",
]
