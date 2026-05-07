"""
College Faculty Schemas

Pydantic schemas for college faculty API validation.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List
from datetime import date, datetime


class FacultyBase(BaseModel):
    """Base schema for faculty"""
    user_id: int = Field(..., gt=0, description="User ID must be positive")
    employee_id: str = Field(..., min_length=1, max_length=20, pattern=r'^[A-Z0-9]+$', description="Employee ID must be alphanumeric uppercase")
    department_id: Optional[int] = Field(None, gt=0, description="Department ID must be positive")
    designation: str = Field(..., min_length=2, max_length=100, description="Designation must be 2-100 characters")
    specialization: Optional[str] = Field(None, min_length=2, max_length=200, description="Specialization must be 2-200 characters")
    qualification: Optional[str] = Field(None, min_length=2, max_length=200, description="Qualification must be 2-200 characters")
    experience_years: Optional[int] = Field(None, ge=0, le=50, description="Experience years must be 0-50")

    @field_validator('employee_id')
    @classmethod
    def validate_employee_id(cls, v):
        """Validate employee ID format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Employee ID must contain only alphanumeric characters, underscores, and hyphens')
        return v.upper()

    @field_validator('designation')
    @classmethod
    def validate_designation(cls, v):
        """Validate designation is title case"""
        return v.strip().title()


class FacultyCreate(FacultyBase):
    """Schema for creating a faculty"""
    pass


class FacultyUpdate(BaseModel):
    """Schema for updating a faculty"""
    department_id: Optional[int] = Field(None, gt=0, description="Department ID must be positive")
    designation: Optional[str] = Field(None, min_length=2, max_length=100, description="Designation must be 2-100 characters")
    specialization: Optional[str] = Field(None, min_length=2, max_length=200, description="Specialization must be 2-200 characters")
    qualification: Optional[str] = Field(None, min_length=2, max_length=200, description="Qualification must be 2-200 characters")
    experience_years: Optional[int] = Field(None, ge=0, le=50, description="Experience years must be 0-50")

    @field_validator('designation')
    @classmethod
    def validate_designation(cls, v):
        """Validate designation is title case"""
        if v is not None:
            return v.strip().title()
        return v


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
