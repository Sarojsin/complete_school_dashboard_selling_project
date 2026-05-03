"""
College Faculty Schemas

Pydantic schemas for college faculty API endpoints.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class FacultyBase(BaseModel):
    employee_id: str
    department_id: Optional[int] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    joining_date: Optional[date] = None


class FacultyCreate(FacultyBase):
    user_id: int


class FacultyUpdate(BaseModel):
    employee_id: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    joining_date: Optional[date] = None


class FacultyResponse(FacultyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
