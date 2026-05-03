"""
College Faculty Schemas

Pydantic schemas for college faculty API validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class FacultyBase(BaseModel):
    """Base schema for faculty"""
    user_id: int
    employee_id: str
    department_id: Optional[int] = None
    designation: str
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None


class FacultyCreate(FacultyBase):
    """Schema for creating a faculty"""
    pass


class FacultyUpdate(BaseModel):
    """Schema for updating a faculty"""
    department_id: Optional[int] = None
    designation: Optional[str] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None


class FacultyResponse(FacultyBase):
    """Schema for faculty response"""
    id: int
    joining_date: Optional[date] = None

    class Config:
        from_attributes = True


class FacultyListResponse(BaseModel):
    """Schema for faculty list response"""
    total: int
    faculty: List[FacultyResponse]


__all__ = [
    "FacultyBase",
    "FacultyCreate",
    "FacultyUpdate",
    "FacultyResponse",
    "FacultyListResponse",
]
