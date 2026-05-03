"""
College Placement API Routes

API endpoints for college placement cell.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import Company, Job, Application
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/placement", tags=["College Placement"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_placement_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get placement dashboard"""
    return {"message": "College placement dashboard"}


@router.get("/companies")
async def get_companies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all companies"""
    result = await db.execute(select(Company))
    companies = result.scalars().all()
    return {"companies": companies}


@router.get("/jobs")
async def get_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all jobs"""
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    return {"jobs": jobs}


@router.get("/applications")
async def get_applications(
    job_id: int = None,
    student_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get applications"""
    query = select(Application)
    if job_id:
        query = query.where(Application.job_id == job_id)
    if student_id:
        query = query.where(Application.student_id == student_id)
    
    result = await db.execute(query)
    apps = result.scalars().all()
    return {"applications": apps}


__all__ = ["router"]
