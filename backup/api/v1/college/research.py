"""
College Research API
==================
API endpoints for research projects and publications.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.college import ResearchProject, Publication, Patent

router = APIRouter(prefix="/research", tags=["Research"])


# Research Project Endpoints
@router.get("/projects")
async def list_projects(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List research projects"""
    query = select(ResearchProject)
    if status:
        query = query.filter(ResearchProject.status == status)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    projects = res.scalars().all()
    return projects


@router.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get research project details"""
    res = await db.execute(select(ResearchProject).filter(ResearchProject.id == project_id))
    project = res.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/projects")
async def create_project(
    title: str,
    description: str = None,
    principal_investigator_id: int = None,
    funding_amount: int = None,
    funding_agency: str = None,
    start_date: str = None,
    end_date: str = None,
    status: str = "ongoing",
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new research project"""
    from datetime import datetime
    
    project = ResearchProject(
        title=title,
        description=description,
        principal_investigator_id=principal_investigator_id,
        funding_amount=funding_amount,
        funding_agency=funding_agency,
        start_date=datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None,
        end_date=datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None,
        status=status
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


# Publication Endpoints
@router.get("/publications")
async def list_publications(
    faculty_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List publications"""
    query = select(Publication)
    if faculty_id:
        query = query.filter(Publication.faculty_id == faculty_id)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    publications = res.scalars().all()
    return publications


@router.get("/publications/{publication_id}")
async def get_publication(
    publication_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get publication details"""
    res = await db.execute(select(Publication).filter(Publication.id == publication_id))
    publication = res.scalar_one_or_none()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication


@router.post("/publications")
async def create_publication(
    title: str,
    authors: list = None,
    journal: str = None,
    conference: str = None,
    publication_date: str = None,
    doi: str = None,
    abstract: str = None,
    faculty_id: int = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new publication"""
    from datetime import datetime
    
    publication = Publication(
        title=title,
        authors=authors,
        journal=journal,
        conference=conference,
        publication_date=datetime.strptime(publication_date, "%Y-%m-%d").date() if publication_date else None,
        doi=doi,
        abstract=abstract,
        faculty_id=faculty_id
    )
    db.add(publication)
    await db.commit()
    await db.refresh(publication)
    return publication


# Patent Endpoints
@router.get("/patents")
async def list_patents(
    faculty_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List patents"""
    query = select(Patent)
    if faculty_id:
        query = query.filter(Patent.faculty_id == faculty_id)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    patents = res.scalars().all()
    return patents


__all__ = ["router"]
