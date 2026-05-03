"""
College Hostel Service

Business logic for college hostel operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import HostelRepository, RoomRepository, AllocationRepository, ComplaintRepository
from .models import Hostel, Room, HostelAllocation, HostelComplaint
from .schemas import (
    HostelCreate, HostelUpdate,
    RoomCreate, RoomUpdate,
    AllocationCreate,
    ComplaintCreate, ComplaintUpdate
)


class HostelService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.hostel_repo = HostelRepository(db)
        self.room_repo = RoomRepository(db)
        self.alloc_repo = AllocationRepository(db)
        self.complaint_repo = ComplaintRepository(db)
    
    # ── Hostel Methods ──────────────────────────────────────────
    async def create_hostel(self, data: HostelCreate) -> Hostel:
        hostel = Hostel(**data.model_dump())
        return await self.hostel_repo.create(hostel)
    
    async def get_hostel(self, hostel_id: int) -> Optional[Hostel]:
        return await self.hostel_repo.get_by_id(hostel_id)
    
    async def list_hostels(self, skip: int = 0, limit: int = 100) -> List[Hostel]:
        return await self.hostel_repo.list(skip, limit)
    
    async def update_hostel(self, hostel_id: int, data: HostelUpdate) -> Optional[Hostel]:
        hostel = await self.hostel_repo.get_by_id(hostel_id)
        if not hostel:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(hostel, key, value)
        return await self.hostel_repo.update(hostel)
    
    async def delete_hostel(self, hostel_id: int) -> bool:
        return await self.hostel_repo.delete(hostel_id)
    
    # ── Room Methods ────────────────────────────────────────────
    async def create_room(self, data: RoomCreate) -> Room:
        room = Room(**data.model_dump())
        return await self.room_repo.create(room)
    
    async def get_room(self, room_id: int) -> Optional[Room]:
        return await self.room_repo.get_by_id(room_id)
    
    async def list_rooms_by_hostel(self, hostel_id: int, skip: int = 0, limit: int = 100) -> List[Room]:
        return await self.room_repo.list_by_hostel(hostel_id, skip, limit)
    
    async def list_available_rooms(self, hostel_id: int = None, skip: int = 0, limit: int = 100) -> List[Room]:
        return await self.room_repo.list_available(hostel_id, skip, limit)
    
    async def update_room(self, room_id: int, data: RoomUpdate) -> Optional[Room]:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(room, key, value)
        return await self.room_repo.update(room)
    
    async def delete_room(self, room_id: int) -> bool:
        return await self.room_repo.delete(room_id)
    
    # ── Allocation Methods ───────────────────────────────────────
    async def allocate_room(self, data: AllocationCreate) -> HostelAllocation:
        # Check room availability
        room = await self.room_repo.get_by_id(data.room_id)
        if not room or not room.is_available:
            raise ValueError("Room not available")
        
        if room.occupied >= room.capacity:
            raise ValueError("Room is full")
        
        allocation = HostelAllocation(**data.model_dump())
        result = await self.alloc_repo.create(allocation)
        
        # Update room occupied count
        room.occupied += 1
        if room.occupied >= room.capacity:
            room.is_available = False
        await self.room_repo.update(room)
        
        return result
    
    async def get_allocation(self, allocation_id: int) -> Optional[HostelAllocation]:
        return await self.alloc_repo.get_by_id(allocation_id)
    
    async def get_student_allocation(self, student_id: int) -> Optional[dict]:
        return await self.alloc_repo.get_allocation_by_student_id(student_id)
    
    async def get_room_allocations(self, room_id: int) -> List[HostelAllocation]:
        return await self.alloc_repo.get_by_room_id(room_id)
    
    async def vacate_room(self, allocation_id: int) -> bool:
        allocation = await self.alloc_repo.get_by_id(allocation_id)
        if not allocation:
            return False
        
        # Update room occupied count
        room = await self.room_repo.get_by_id(allocation.room_id)
        if room:
            room.occupied = max(0, room.occupied - 1)
            room.is_available = True
            await self.room_repo.update(room)
        
        return await self.alloc_repo.vacate(allocation_id)
    
    # ── Complaint Methods ────────────────────────────────────────
    async def create_complaint(self, student_id: int, data: ComplaintCreate) -> HostelComplaint:
        complaint = HostelComplaint(student_id=student_id, **data.model_dump())
        return await self.complaint_repo.create(complaint)
    
    async def get_complaint(self, complaint_id: int) -> Optional[HostelComplaint]:
        return await self.complaint_repo.get_by_id(complaint_id)
    
    async def list_complaints(self, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        return await self.complaint_repo.list(skip, limit)
    
    async def list_my_complaints(self, student_id: int, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        return await self.complaint_repo.list_by_student(student_id, skip, limit)
    
    async def list_pending_complaints(self, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        return await self.complaint_repo.list_pending(skip, limit)
    
    async def resolve_complaint(self, complaint_id: int, resolved_by: int) -> bool:
        return await self.complaint_repo.resolve(complaint_id, resolved_by)