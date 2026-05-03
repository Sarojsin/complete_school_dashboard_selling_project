"""
College Lab API Routes

API endpoints for college lab management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.college.database import get_college_async_db
from modules.shared.models import User
from backup.models.college import Lab, LabEquipment, LabSchedule
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/lab", tags=["College Lab"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_lab_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get lab dashboard"""
    return {"message": "College lab dashboard"}


@router.get("/labs")
async def get_labs(
    department_id: int = None,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get all labs"""
    query = select(Lab)
    if department_id:
        query = query.where(Lab.department_id == department_id)
    
    result = await db.execute(query)
    labs = result.scalars().all()
    return {"labs": labs}


@router.get("/equipment")
async def get_equipment(
    lab_id: int = None,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get lab equipment"""
    query = select(LabEquipment)
    if lab_id:
        query = query.where(LabEquipment.lab_id == lab_id)
    
    result = await db.execute(query)
    equipment = result.scalars().all()
    return {"equipment": equipment}


@router.get("/schedules")
async def get_schedules(
    lab_id: int = None,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get lab schedules"""
    query = select(LabSchedule)
    if lab_id:
        query = query.where(LabSchedule.lab_id == lab_id)
    
    result = await db.execute(query)
    schedules = result.scalars().all()
    return {"schedules": schedules}


__all__ = ["router"]
