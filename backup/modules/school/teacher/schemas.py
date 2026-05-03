# School Teacher Schemas
# ====================
# Pydantic schemas for school teacher API validation

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class TeacherBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    status: str = "active"


class TeacherCreate(TeacherBase):
    user_id: int


class TeacherUpdate(BaseModel):
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    status: Optional[str] = None


class Teacher(TeacherBase):
    id: int
    user_id: int
    joining_date: date

    class Config:
        from_attributes = True


class TeacherWithUser(Teacher):
    email: Optional[str] = None
    username: Optional[str] = None

    class Config:
        from_attributes = True


__all__ = [
    "TeacherBase",
    "TeacherCreate",
    "TeacherUpdate",
    "Teacher",
    "TeacherWithUser",
]
