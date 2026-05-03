"""
Hostel Service

Business logic for hostel and room management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from backup.modules.college.hostel.schemas import (
    HostelResponse,
    HostelListResponse,
    RoomResponse,
    RoomListResponse,
)
from backup.modules.college.hostel.repository import HostelRepository


class HostelService:
    """Service for hostel business logic"""

    async def list_hostels(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> HostelListResponse:
        """List all hostels"""
        hostels, total = await HostelRepository.list_hostels(db, skip, limit)
        return HostelListResponse(
            hostels=[HostelResponse.model_validate(h) for h in hostels],
            total=total
        )

    async def get_hostel(
        self, db: AsyncSession, hostel_id: int
    ) -> Optional[HostelResponse]:
        """Get a hostel by ID"""
        hostel = await HostelRepository.get_hostel(db, hostel_id)
        if hostel:
            return HostelResponse.model_validate(hostel)
        return None

    async def list_rooms(
        self, db: AsyncSession, hostel_id: int, skip: int = 0, limit: int = 20
    ) -> RoomListResponse:
        """List rooms in a hostel"""
        rooms, total = await HostelRepository.list_rooms(db, hostel_id, skip, limit)
        return RoomListResponse(
            rooms=[RoomResponse.model_validate(r) for r in rooms],
            total=total
        )

    async def get_room(
        self, db: AsyncSession, room_id: int
    ) -> Optional[RoomResponse]:
        """Get a room by ID"""
        room = await HostelRepository.get_room(db, room_id)
        if room:
            return RoomResponse.model_validate(room)
        return None
