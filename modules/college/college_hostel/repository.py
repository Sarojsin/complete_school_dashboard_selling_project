"""
College Hostel Repository

Async CRUD operations for college hostel management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import Hostel, Room, HostelAllocation, HostelComplaint


# ── Hostel Repository ─────────────────────────────────────────
class HostelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, hostel_id: int) -> Optional[Hostel]:
        result = await self.db.execute(
            select(Hostel).filter(Hostel.id == hostel_id)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Hostel]:
        result = await self.db.execute(
            select(Hostel).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, hostel: Hostel) -> Hostel:
        self.db.add(hostel)
        await self.db.commit()
        await self.db.refresh(hostel)
        return hostel
    
    async def update(self, hostel: Hostel) -> Hostel:
        await self.db.commit()
        await self.db.refresh(hostel)
        return hostel
    
    async def delete(self, hostel_id: int) -> bool:
        hostel = await self.get_by_id(hostel_id)
        if hostel:
            await self.db.delete(hostel)
            await self.db.commit()
            return True
        return False


# ── Room Repository ────────────────────────────────────────────
class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, room_id: int) -> Optional[Room]:
        result = await self.db.execute(
            select(Room).filter(Room.id == room_id)
        )
        return result.scalars().first()
    
    async def list_by_hostel(self, hostel_id: int, skip: int = 0, limit: int = 100) -> List[Room]:
        result = await self.db.execute(
            select(Room)
            .filter(Room.hostel_id == hostel_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_available(self, hostel_id: int = None, skip: int = 0, limit: int = 100) -> List[Room]:
        query = select(Room).filter(Room.is_available == True)
        if hostel_id:
            query = query.filter(Room.hostel_id == hostel_id)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def create(self, room: Room) -> Room:
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room
    
    async def update(self, room: Room) -> Room:
        await self.db.commit()
        await self.db.refresh(room)
        return room
    
    async def delete(self, room_id: int) -> bool:
        room = await self.get_by_id(room_id)
        if room:
            await self.db.delete(room)
            await self.db.commit()
            return True
        return False


# ── Allocation Repository ──────────────────────────────────────
class AllocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, allocation_id: int) -> Optional[HostelAllocation]:
        result = await self.db.execute(
            select(HostelAllocation).filter(HostelAllocation.id == allocation_id)
        )
        return result.scalars().first()
    
    async def get_by_student_id(self, student_id: int) -> List[dict]:
        result = await self.db.execute(
            select(HostelAllocation).filter(HostelAllocation.student_id == student_id)
        )
        allocations = result.scalars().all()
        
        return [
            {
                "id": a.id,
                "student_id": a.student_id,
                "room_id": a.room_id,
                "allocation_date": a.allocation_date.isoformat() if a.allocation_date else None,
                "vacate_date": a.vacate_date.isoformat() if a.vacate_date else None,
                "status": a.status
            }
            for a in allocations
        ]
    
    async def get_allocation_by_student_id(self, student_id: int) -> Optional[dict]:
        """Get active allocation for student"""
        result = await self.db.execute(
            select(HostelAllocation)
            .filter(HostelAllocation.student_id == student_id)
            .filter(HostelAllocation.status == "active")
        )
        a = result.scalars().first()
        if not a:
            return None
        
        return {
            "id": a.id,
            "student_id": a.student_id,
            "room_id": a.room_id,
            "allocation_date": a.allocation_date.isoformat() if a.allocation_date else None,
            "status": a.status
        }
    
    async def get_by_room_id(self, room_id: int) -> List[HostelAllocation]:
        result = await self.db.execute(
            select(HostelAllocation)
            .filter(HostelAllocation.room_id == room_id)
            .filter(HostelAllocation.status == "active")
        )
        return list(result.scalars().all())
    
    async def create(self, allocation: HostelAllocation) -> HostelAllocation:
        self.db.add(allocation)
        await self.db.commit()
        await self.db.refresh(allocation)
        return allocation
    
    async def update(self, allocation: HostelAllocation) -> HostelAllocation:
        await self.db.commit()
        await self.db.refresh(allocation)
        return allocation
    
    async def vacate(self, allocation_id: int) -> bool:
        from datetime import datetime
        allocation = await self.get_by_id(allocation_id)
        if allocation:
            allocation.status = "vacated"
            allocation.vacate_date = datetime.utcnow()
            await self.db.commit()
            return True
        return False
    
    async def delete(self, allocation_id: int) -> bool:
        allocation = await self.get_by_id(allocation_id)
        if allocation:
            await self.db.delete(allocation)
            await self.db.commit()
            return True
        return False


# ── Complaint Repository ───────────────────────────────────────
class ComplaintRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, complaint_id: int) -> Optional[HostelComplaint]:
        result = await self.db.execute(
            select(HostelComplaint).filter(HostelComplaint.id == complaint_id)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        result = await self.db.execute(
            select(HostelComplaint).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        result = await self.db.execute(
            select(HostelComplaint)
            .filter(HostelComplaint.student_id == student_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_pending(self, skip: int = 0, limit: int = 100) -> List[HostelComplaint]:
        result = await self.db.execute(
            select(HostelComplaint)
            .filter(HostelComplaint.status == "pending")
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, complaint: HostelComplaint) -> HostelComplaint:
        self.db.add(complaint)
        await self.db.commit()
        await self.db.refresh(complaint)
        return complaint
    
    async def update(self, complaint: HostelComplaint) -> HostelComplaint:
        await self.db.commit()
        await self.db.refresh(complaint)
        return complaint
    
    async def resolve(self, complaint_id: int, resolved_by: int) -> bool:
        from datetime import datetime
        complaint = await self.get_by_id(complaint_id)
        if complaint:
            complaint.status = "resolved"
            complaint.resolved_by = resolved_by
            complaint.resolved_at = datetime.utcnow()
            await self.db.commit()
            return True
        return False
    
    async def delete(self, complaint_id: int) -> bool:
        complaint = await self.get_by_id(complaint_id)
        if complaint:
            await self.db.delete(complaint)
            await self.db.commit()
            return True
        return False