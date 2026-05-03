"""
Program Schemas

Pydantic schemas for program validation.
"""

from pydantic import BaseModel
from typing import Optional


class ProgramBase(BaseModel):
    """Base schema for program"""
    name: str
    code: str
    department_id: int
    duration_years: int
    total_credits: int
    description: Optional[str] = None


class ProgramCreate(ProgramBase):
    """Schema for creating program"""
    pass


class ProgramUpdate(BaseModel):
    """Schema for updating program"""
    name: Optional[str] = None
    duration_years: Optional[int] = None
    total_credits: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ProgramResponse(ProgramBase):
    """Schema for program response"""
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class ProgramListResponse(BaseModel):
    """Schema for listing programs"""
    programs: list[ProgramResponse]
    total: int
