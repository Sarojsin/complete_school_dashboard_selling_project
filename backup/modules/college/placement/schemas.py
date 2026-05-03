# College Placement Schemas
# ========================
# Pydantic schemas for placement API validation

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


# Company Schemas
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None


class Company(CompanyBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True


# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    deadline: Optional[date] = None
    is_active: bool = True


class JobCreate(JobBase):
    company_id: int


class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    deadline: Optional[date] = None
    is_active: Optional[bool] = None


class Job(JobBase):
    id: int
    company_id: int
    created_at: date

    class Config:
        from_attributes = True


class JobWithCompany(Job):
    company: Company

    class Config:
        from_attributes = True


# Application Schemas
class ApplicationBase(BaseModel):
    status: str = "applied"


class ApplicationCreate(BaseModel):
    job_id: int
    student_id: int
    resume: Optional[str] = None
    cover_letter: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    resume: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None


class Application(ApplicationBase):
    id: int
    job_id: int
    student_id: int
    applied_date: date
    resume: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationWithDetails(Application):
    job: JobWithCompany

    class Config:
        from_attributes = True


# Placement Drive Schemas
class PlacementDriveBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True


class PlacementDriveCreate(PlacementDriveBase):
    company_id: Optional[int] = None


class PlacementDriveUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class PlacementDrive(PlacementDriveBase):
    id: int
    company_id: Optional[int] = None
    created_at: date

    class Config:
        from_attributes = True


__all__ = [
    "CompanyBase",
    "CompanyCreate",
    "CompanyUpdate",
    "Company",
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "Job",
    "JobWithCompany",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "Application",
    "ApplicationWithDetails",
    "PlacementDriveBase",
    "PlacementDriveCreate",
    "PlacementDriveUpdate",
    "PlacementDrive",
]
