"""
College Dean Schemas
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class DeanDashboardResponse(BaseModel):
    departments: int
    programs: int
    faculty: int
    students: int


class DepartmentListSchema(BaseModel):
    id: int
    name: str
    code: str

    model_config = {"from_attributes": True}


class ProgramListSchema(BaseModel):
    id: int
    name: str
    code: str
    department_id: Optional[int] = None

    model_config = {"from_attributes": True}


class FacultySummarySchema(BaseModel):
    id: int
    employee_id: str
    designation: Optional[str] = None
    qualification: Optional[str] = None
    department_id: Optional[int] = None

    model_config = {"from_attributes": True}


class StudentSummarySchema(BaseModel):
    id: int
    roll_number: str
    program_id: Optional[int] = None
    semester_id: Optional[int] = None
    cgpa: Optional[float] = None

    model_config = {"from_attributes": True}


__all__ = [
    "DeanDashboardResponse",
    "DepartmentListSchema",
    "ProgramListSchema",
    "FacultySummarySchema",
    "StudentSummarySchema",
]
