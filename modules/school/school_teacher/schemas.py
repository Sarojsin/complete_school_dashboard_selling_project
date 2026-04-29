# School Teacher Schemas
# ====================
# Pydantic schemas for school teacher API validation

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TeacherBase(BaseModel):
    user_id: int
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    status: str = "active"


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    status: Optional[str] = None


class TeacherResponse(TeacherBase):
    id: int
    joining_date: Optional[date] = None
    
    model_config = {"from_attributes": True}


class Teacher(TeacherResponse):
    """Legacy alias for TeacherResponse"""
    pass


class TeacherWithUser(TeacherResponse):
    email: Optional[str] = None
    username: Optional[str] = None
    
    model_config = {"from_attributes": True}


__all__ = [
    "TeacherBase",
    "TeacherCreate",
    "TeacherUpdate",
    "TeacherResponse",
    "Teacher",
    "TeacherWithUser",
]
