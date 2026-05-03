"""
Hostel API Routes

API routes for hostel management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.college.hostel.schemas import (
    HostelResponse,
    HostelListResponse,
    RoomResponse,
    RoomListResponse,
)
from backup.modules.college.hostel.service import HostelService

router = APIRouter(prefix="/hostels", tags=["College Hostels"])


@router.get("/", response_model=HostelListResponse)
async def list_hostels(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all hostels"""
    service = HostelService()
    return await service.list_hostels(db, skip, limit)


@router.get("/{hostel_id}", response_model=HostelResponse)
async def get_hostel(
    hostel_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific hostel"""
    service = HostelService()
    return await service.get_hostel(db, hostel_id)


@router.get("/{hostel_id}/rooms", response_model=RoomListResponse)
async def list_rooms(
    hostel_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List rooms in a hostel"""
    service = HostelService()
    return await service.list_rooms(db, hostel_id, skip, limit)
