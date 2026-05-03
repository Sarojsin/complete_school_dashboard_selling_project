"""
Hostel Repository

Data access layer for hostel and room management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from backup.models.college.hostel import Hostel, Room


class HostelRepository:
    """Repository for hostel data access"""

    @staticmethod
    async def get_hostel(db: AsyncSession, hostel_id: int) -> Optional[Hostel]:
        """Get a hostel by ID"""
        result = await db.execute(
            select(Hostel).where(Hostel.id == hostel_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_hostels(
        db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> tuple[List[Hostel], int]:
        """List all hostels with pagination"""
        # Get total count
        count_result = await db.execute(select(Hostel))
        total = len(count_result.scalars().all())

        # Get paginated results
        result = await db.execute(
            select(Hostel)
            .offset(skip)
            .limit(limit)
            .order_by(Hostel.name)
        )
        hostels = result.scalars().all()
        return list(hostels), total

    @staticmethod
    async def get_room(db: AsyncSession, room_id: int) -> Optional[Room]:
        """Get a room by ID"""
        result = await db.execute(
            select(Room).where(Room.id == room_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_rooms(
        db: AsyncSession, hostel_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[List[Room], int]:
        """List rooms in a hostel with pagination"""
        # Get total count
        count_result = await db.execute(
            select(Room).where(Room.hostel_id == hostel_id)
        )
        total = len(count_result.scalars().all())

        # Get paginated results
        result = await db.execute(
            select(Room)
            .where(Room.hostel_id == hostel_id)
            .offset(skip)
            .limit(limit)
            .order_by(Room.room_number)
        )
        rooms = result.scalars().all()
        return list(rooms), total
