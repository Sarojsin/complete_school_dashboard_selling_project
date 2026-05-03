"""
Research Schemas

Pydantic schemas for research projects and publications.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResearchProjectBase(BaseModel):
    title: str
    description: str
    department_id: int
    faculty_id: int
    start_date: str
    end_date: Optional[str] = None
    funding_amount: Optional[int] = None
    funding_source: Optional[str] = None
    status: str = "ongoing"


class ResearchProjectResponse(ResearchProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResearchProjectListResponse(BaseModel):
    projects: list[ResearchProjectResponse]
    total: int


class PublicationBase(BaseModel):
    title: str
    abstract: str
    journal_name: str
    publication_date: str
    doi: Optional[str] = None
    authors: str
    department_id: int
    research_project_id: Optional[int] = None
    citation_count: int = 0


class PublicationResponse(PublicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublicationListResponse(BaseModel):
    publications: list[PublicationResponse]
    total: int
