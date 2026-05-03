"""
College Hostel API Routes

API endpoints for college hostel management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import Hostel, Room, HostelAllocation
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/hostel", tags=["College Hostel"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_hostel_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get hostel dashboard"""
    return {"message": "College hostel dashboard"}


@router.get("/hostels")
async def get_hostels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all hostels"""
    result = await db.execute(select(Hostel))
    hostels = result.scalars().all()
    return {"hostels": hostels}


@router.get("/rooms")
async def get_rooms(
    hostel_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get rooms"""
    query = select(Room)
    if hostel_id:
        query = query.where(Room.hostel_id == hostel_id)
    
    result = await db.execute(query)
    rooms = result.scalars().all()
    return {"rooms": rooms}


@router.get("/allocations")
async def get_allocations(
    student_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get hostel allocations"""
    query = select(HostelAllocation)
    if student_id:
        query = query.where(HostelAllocation.student_id == student_id)
    
    result = await db.execute(query)
    allocations = result.scalars().all()
    return {"allocations": allocations}


__all__ = ["router"]
