"""
Authority Schemas

Pydantic schemas for authority validation.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AuthorityBase(BaseModel):
    """Base schema for authority"""
    user_id: int
    position: str
    department: Optional[str] = None
    phone: Optional[str] = None


class AuthorityCreate(AuthorityBase):
    """Schema for creating authority"""
    pass


class AuthorityUpdate(BaseModel):
    """Schema for updating authority"""
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None


class AuthorityResponse(AuthorityBase):
    """Schema for authority response"""
    id: int
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AuthorityListResponse(BaseModel):
    """Schema for listing authorities"""
    authorities: list[AuthorityResponse]
    total: int
