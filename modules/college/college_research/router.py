"""
College Research Router

FastAPI endpoints for college research operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import ResearchService
from .schemas import (
    ProjectResponse, ProjectCreate, ProjectUpdate,
    PublicationResponse, PublicationCreate, PublicationUpdate,
    PatentResponse, PatentCreate, PatentUpdate
)

router = APIRouter(prefix="/research", tags=["College Research"], dependencies=[Depends(require_college_portal)])


# ── Project Endpoints ──────────────────────────────────────────
@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a research project (Protected - Dean/Faculty)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = ResearchService(db)
    return await service.create_project(data)


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 20,
    faculty_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List research projects (Protected)"""
    service = ResearchService(db)
    if faculty_id:
        return await service.list_projects_by_faculty(faculty_id, skip, limit)
    return await service.list_projects(skip, limit)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get project by ID (Protected)"""
    service = ResearchService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


# ── Publication Endpoints ────────────────────────────────────────
@router.post("/publications", response_model=PublicationResponse, status_code=status.HTTP_201_CREATED)
async def create_publication(
    data: PublicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a publication (Protected - Dean/Faculty)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = ResearchService(db)
    return await service.create_publication(data)


@router.get("/publications", response_model=List[PublicationResponse])
async def list_publications(
    skip: int = 0,
    limit: int = 20,
    faculty_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List publications (Protected)"""
    service = ResearchService(db)
    if faculty_id:
        return await service.list_publications_by_faculty(faculty_id, skip, limit)
    return await service.list_publications(skip, limit)


@router.get("/publications/{pub_id}", response_model=PublicationResponse)
async def get_publication(
    pub_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get publication by ID (Protected)"""
    service = ResearchService(db)
    publication = await service.get_publication(pub_id)
    if not publication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    return publication


# ── Patent Endpoints ─────────────────────────────────────────────
@router.post("/patents", response_model=PatentResponse, status_code=status.HTTP_201_CREATED)
async def create_patent(
    data: PatentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a patent (Protected - Dean/Faculty)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = ResearchService(db)
    return await service.create_patent(data)


@router.get("/patents", response_model=List[PatentResponse])
async def list_patents(
    skip: int = 0,
    limit: int = 20,
    faculty_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List patents (Protected)"""
    service = ResearchService(db)
    if faculty_id:
        return await service.list_patents_by_faculty(faculty_id, skip, limit)
    return await service.list_patents(skip, limit)


__all__ = ["router"]