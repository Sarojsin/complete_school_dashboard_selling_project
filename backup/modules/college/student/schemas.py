"""
Student Schemas

Pydantic schemas for student validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StudentBase(BaseModel):
    """Base schema for student"""
    user_id: int
    student_id: str  # Roll number / enrollment number
    program_id: int
    semester_id: int
    admission_date: Optional[datetime] = None
    batch: Optional[str] = None


class StudentCreate(StudentBase):
    """Schema for creating student"""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating student"""
    program_id: Optional[int] = None
    semester_id: Optional[int] = None
    batch: Optional[str] = None
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    """Schema for student response"""
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """Schema for listing students"""
    students: list[StudentResponse]
    total: int
