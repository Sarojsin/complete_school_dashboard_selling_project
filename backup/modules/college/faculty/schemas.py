"""
Faculty Schemas

Pydantic schemas for faculty validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FacultyBase(BaseModel):
    """Base schema for faculty"""
    user_id: int
    employee_id: str
    department_id: int
    designation: str
    qualification: Optional[str] = None
    specialisation: Optional[str] = None
    experience_years: Optional[int] = 0


class FacultyCreate(FacultyBase):
    """Schema for creating faculty"""
    pass


class FacultyUpdate(BaseModel):
    """Schema for updating faculty"""
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialisation: Optional[str] = None
    experience_years: Optional[int] = None
    is_active: Optional[bool] = None


class FacultyResponse(FacultyBase):
    """Schema for faculty response"""
    id: int
    hire_date: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class FacultyListResponse(BaseModel):
    """Schema for listing faculty"""
    faculty: list[FacultyResponse]
    total: int
