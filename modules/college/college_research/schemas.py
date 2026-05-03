"""
College Research Schemas

Pydantic schemas for college research API.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ── Project Schemas ─────────────────────────────────────────────
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    principal_investigator_id: Optional[int] = None
    co_investigators: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    funding_amount: Optional[str] = None
    funding_agency: Optional[str] = None
    status: Optional[str] = "ongoing"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    co_investigators: Optional[str] = None
    end_date: Optional[datetime] = None
    funding_amount: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Publication Schemas ─────────────────────────────────────────
class PublicationBase(BaseModel):
    title: str
    authors: Optional[str] = None
    journal_name: Optional[str] = None
    publication_date: Optional[datetime] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    faculty_id: Optional[int] = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    journal_name: Optional[str] = None
    publication_date: Optional[datetime] = None


class PublicationResponse(PublicationBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Patent Schemas ──────────────────────────────────────────────
class PatentBase(BaseModel):
    title: str
    inventors: Optional[str] = None
    patent_number: Optional[str] = None
    filing_date: Optional[datetime] = None
    grant_date: Optional[datetime] = None
    status: Optional[str] = "filed"
    description: Optional[str] = None
    faculty_id: Optional[int] = None


class PatentCreate(PatentBase):
    pass


class PatentUpdate(BaseModel):
    title: Optional[str] = None
    grant_date: Optional[datetime] = None
    status: Optional[str] = None


class PatentResponse(PatentBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)