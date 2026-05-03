"""
College Student Schemas

Pydantic schemas for college student API endpoints.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class CollegeStudentBase(BaseModel):
    roll_number: str
    program_id: Optional[int] = None
    semester_id: Optional[int] = None
    enrollment_date: Optional[date] = None
    cgpa: Optional[float] = 0.0
    total_credits_completed: Optional[int] = 0


class CollegeStudentCreate(CollegeStudentBase):
    user_id: int


class CollegeStudentUpdate(BaseModel):
    roll_number: Optional[str] = None
    program_id: Optional[int] = None
    semester_id: Optional[int] = None
    enrollment_date: Optional[date] = None
    cgpa: Optional[float] = None
    total_credits_completed: Optional[int] = None


class CollegeStudentResponse(CollegeStudentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
