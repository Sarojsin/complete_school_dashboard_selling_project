# School Student Schemas
# ====================

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_id: Optional[int] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    roll_number: Optional[str] = None


class StudentCreate(StudentBase):
    user_id: int


class StudentUpdate(BaseModel):
    student_id: Optional[str] = Field(None, min_length=1, max_length=50)
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_id: Optional[int] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    roll_number: Optional[str] = None


class Student(StudentBase):
    id: int
    user_id: int
    enrollment_date: date

    class Config:
        from_attributes = True


__all__ = ["StudentBase", "StudentCreate", "StudentUpdate", "Student"]
