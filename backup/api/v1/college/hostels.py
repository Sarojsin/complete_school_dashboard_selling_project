"""
College Hostels API
=================
API endpoints for hostel management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.college import Hostel, Room, HostelAllocation, HostelComplaint

router = APIRouter(prefix="/hostels", tags=["Hostels"])


# Hostel Endpoints
@router.get("/")
async def list_hostels(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all hostels"""
    res = await db.execute(select(Hostel).offset(skip).limit(limit))
    hostels = res.scalars().all()
    return hostels


@router.get("/{hostel_id}")
async def get_hostel(
    hostel_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get hostel details"""
    res = await db.execute(select(Hostel).filter(Hostel.id == hostel_id))
    hostel = res.scalar_one_or_none()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")
    return hostel


@router.post("/")
async def create_hostel(
    name: str,
    capacity: int = 0,
    address: str = None,
    contact_number: str = None,
    email: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new hostel"""
    hostel = Hostel(
        name=name,
        capacity=capacity,
        address=address,
        contact_number=contact_number,
        email=email
    )
    db.add(hostel)
    await db.commit()
    await db.refresh(hostel)
    return hostel


# Room Endpoints
@router.get("/{hostel_id}/rooms")
async def list_rooms(
    hostel_id: int,
    available_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List rooms in a hostel"""
    query = select(Room).filter(Room.hostel_id == hostel_id)
    if available_only:
        query = query.filter(Room.occupied < Room.capacity)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    rooms = res.scalars().all()
    return rooms


@router.post("/{hostel_id}/rooms")
async def create_room(
    hostel_id: int,
    room_number: str,
    floor: int = 1,
    capacity: int = 2,
    room_type: str = "double",
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new room"""
    # Check hostel exists
    res = await db.execute(select(Hostel).filter(Hostel.id == hostel_id))
    hostel = res.scalar_one_or_none()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")
    
    room = Room(
        hostel_id=hostel_id,
        room_number=room_number,
        floor=floor,
        capacity=capacity,
        room_type=room_type
    )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room


# Allocation Endpoints
@router.post("/allocate")
async def allocate_room(
    student_id: int,
    room_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Allocate room to student"""
    # Check room exists and has capacity
    res = await db.execute(select(Room).filter(Room.id == room_id))
    room = res.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.occupied >= room.capacity:
        raise HTTPException(status_code=400, detail="Room is full")
    
    # Check student not already allocated
    res = await db.execute(
        select(HostelAllocation).filter(
            HostelAllocation.student_id == student_id,
            HostelAllocation.status == "active"
        )
    )
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Student already has a room")
    
    allocation = HostelAllocation(
        student_id=student_id,
        room_id=room_id,
        status="active"
    )
    room.occupied += 1
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    return allocation


@router.get("/student/{student_id}/allocation")
async def get_student_allocation(
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get student's hostel allocation"""
    res = await db.execute(
        select(HostelAllocation).filter(
            HostelAllocation.student_id == student_id,
            HostelAllocation.status == "active"
        )
    )
    allocation = res.scalar_one_or_none()
    return allocation


@router.post("/vacate")
async def vacate_room(
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Vacate hostel room"""
    res = await db.execute(
        select(HostelAllocation).filter(
            HostelAllocation.student_id == student_id,
            HostelAllocation.status == "active"
        )
    )
    allocation = res.scalar_one_or_none()
    if not allocation:
        raise HTTPException(status_code=404, detail="No active allocation found")
    
    # Update room count
    res = await db.execute(select(Room).filter(Room.id == allocation.room_id))
    room = res.scalar_one_or_none()
    if room and room.occupied > 0:
        room.occupied -= 1
    
    allocation.status = "vacated"
    await db.commit()
    await db.refresh(allocation)
    return allocation


# Complaint Endpoints
@router.get("/complaints")
async def list_complaints(
    student_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List hostel complaints"""
    query = select(HostelComplaint)
    if student_id:
        query = query.filter(HostelComplaint.student_id == student_id)
    if status:
        query = query.filter(HostelComplaint.status == status)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    complaints = res.scalars().all()
    return complaints


@router.post("/complaints")
async def create_complaint(
    student_id: int,
    subject: str,
    description: str,
    category: str = "maintenance",
    hostel_id: int = None,
    room_id: int = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Register new complaint"""
    complaint = HostelComplaint(
        student_id=student_id,
        subject=subject,
        description=description,
        category=category,
        hostel_id=hostel_id,
        room_id=room_id,
        status="pending"
    )
    db.add(complaint)
    await db.commit()
    await db.refresh(complaint)
    return complaint


@router.put("/complaints/{complaint_id}/resolve")
async def resolve_complaint(
    complaint_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Resolve complaint"""
    res = await db.execute(select(HostelComplaint).filter(HostelComplaint.id == complaint_id))
    complaint = res.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    complaint.status = "resolved"
    await db.commit()
    await db.refresh(complaint)
    return complaint


__all__ = ["router"]
