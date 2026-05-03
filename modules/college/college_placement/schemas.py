"""
College Placement Schemas

Pydantic schemas for college placement API.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ── Company Schemas ─────────────────────────────────────────────
class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyResponse(CompanyBase):
    id: int
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Job Schemas ────────────────────────────────────────────────
class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    eligibility_criteria: Optional[str] = None
    deadline: Optional[datetime] = None


class JobCreate(JobBase):
    company_id: int


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    eligibility_criteria: Optional[str] = None
    deadline: Optional[datetime] = None
    is_active: Optional[bool] = None


class JobResponse(JobBase):
    id: int
    company_id: int
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Application Schemas ────────────────────────────────────────
class ApplicationBase(BaseModel):
    student_id: int
    job_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: int
    status: Optional[str] = "applied"
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)