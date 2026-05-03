"""
College Hostel Router

FastAPI endpoints for college hostel operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import HostelService
from .schemas import (
    HostelResponse, HostelCreate, HostelUpdate,
    RoomResponse, RoomCreate, RoomUpdate,
    AllocationResponse, AllocationCreate,
    ComplaintResponse, ComplaintCreate
)

router = APIRouter(prefix="/hostels", tags=["College Hostel"], dependencies=[Depends(require_college_portal)])


# ── Hostel Endpoints ───────────────────────────────────────────
@router.post("/", response_model=HostelResponse, status_code=status.HTTP_201_CREATED)
async def create_hostel(
    data: HostelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new hostel (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = HostelService(db)
    return await service.create_hostel(data)


@router.get("/", response_model=List[HostelResponse])
async def list_hostels(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List hostels (Protected)"""
    service = HostelService(db)
    return await service.list_hostels(skip, limit)


@router.get("/{hostel_id}", response_model=HostelResponse)
async def get_hostel(
    hostel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get hostel by ID (Protected)"""
    service = HostelService(db)
    hostel = await service.get_hostel(hostel_id)
    if not hostel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
    return hostel


@router.patch("/{hostel_id}", response_model=HostelResponse)
async def update_hostel(
    hostel_id: int,
    data: HostelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update hostel (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = HostelService(db)
    hostel = await service.update_hostel(hostel_id, data)
    if not hostel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
    return hostel


# ── Room Endpoints ──────────────────────────────────────────────
@router.post("/{hostel_id}/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    hostel_id: int,
    data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new room (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = HostelService(db)
    return await service.create_room(data)


@router.get("/{hostel_id}/rooms", response_model=List[RoomResponse])
async def list_rooms(
    hostel_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List rooms in a hostel (Protected)"""
    service = HostelService(db)
    return await service.list_rooms_by_hostel(hostel_id, skip, limit)


# ── Allocation Endpoints ────────────────────────────────────────
@router.post("/allocate", response_model=AllocationResponse, status_code=status.HTTP_201_CREATED)
async def allocate_room(
    data: AllocationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Allocate room to student (Protected - Dean/Warden)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = HostelService(db)
    try:
        return await service.allocate_room(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/student/{student_id}/allocation", response_model=dict)
async def get_student_allocation(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get student's hostel allocation (Protected)"""
    service = HostelService(db)
    allocation = await service.get_student_allocation(student_id)
    if not allocation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No allocation found")
    return allocation


@router.post("/vacate", status_code=status.HTTP_204_NO_CONTENT)
async def vacate_room(
    allocation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Vacate hostel room (Protected - Dean/Warden)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = HostelService(db)
    success = await service.vacate_room(allocation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")


# ── Complaint Endpoints ─────────────────────────────────────────
@router.post("/complaints", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    data: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a complaint (Protected - Student)"""
    if current_user.role not in ["student", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Get student profile
    from modules.college.college_student.repository import CollegeStudentRepository
    student_repo = CollegeStudentRepository(db)
    student = await student_repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    service = HostelService(db)
    return await service.create_complaint(student.id, data)


@router.get("/complaints", response_model=List[ComplaintResponse])
async def list_complaints(
    skip: int = 0,
    limit: int = 20,
    pending_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List complaints (Protected)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    service = HostelService(db)
    if pending_only:
        return await service.list_pending_complaints(skip, limit)
    return await service.list_complaints(skip, limit)


@router.put("/complaints/{complaint_id}/resolve")
async def resolve_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Resolve a complaint (Protected - Dean/Warden)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Get faculty profile
    from modules.college.college_faculty.repository import FacultyRepository
    faculty_repo = FacultyRepository(db)
    faculty = await faculty_repo.get_by_user_id(current_user.id)
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty profile not found")
    
    service = HostelService(db)
    success = await service.resolve_complaint(complaint_id, faculty.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return {"message": "Complaint resolved"}


__all__ = ["router"]