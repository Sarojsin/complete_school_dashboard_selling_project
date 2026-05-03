"""
Research API Routes

API routes for research project and publication management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.college.research.schemas import (
    ResearchProjectResponse,
    ResearchProjectListResponse,
    PublicationResponse,
    PublicationListResponse,
)
from backup.modules.college.research.service import ResearchService

router = APIRouter(prefix="/research", tags=["College Research"])


@router.get("/projects", response_model=ResearchProjectListResponse)
async def list_research_projects(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all research projects"""
    service = ResearchService()
    return await service.list_projects(db, skip, limit)


@router.get("/projects/{project_id}", response_model=ResearchProjectResponse)
async def get_research_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific research project"""
    service = ResearchService()
    return await service.get_project(db, project_id)


@router.get("/publications", response_model=PublicationListResponse)
async def list_publications(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all publications"""
    service = ResearchService()
    return await service.list_publications(db, skip, limit)


@router.get("/publications/{publication_id}", response_model=PublicationResponse)
async def get_publication(
    publication_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific publication"""
    service = ResearchService()
    return await service.get_publication(db, publication_id)
