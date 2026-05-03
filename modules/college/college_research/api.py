"""
College Research API Routes

API endpoints for college research projects.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import ResearchProject, Publication, Patent
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/research", tags=["College Research"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_research_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get research dashboard"""
    return {"message": "College research dashboard"}


@router.get("/projects")
async def get_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get research projects"""
    result = await db.execute(select(ResearchProject))
    projects = result.scalars().all()
    return {"projects": projects}


@router.get("/publications")
async def get_publications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get publications"""
    result = await db.execute(select(Publication))
    pubs = result.scalars().all()
    return {"publications": pubs}


@router.get("/patents")
async def get_patents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get patents"""
    result = await db.execute(select(Patent))
    patents = result.scalars().all()
    return {"patents": patents}


__all__ = ["router"]
