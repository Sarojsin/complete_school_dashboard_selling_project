"""
Faculty API Routes

API routes for faculty management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.college.faculty.service import FacultyService
from backup.modules.college.faculty.schemas import (
    FacultyCreate,
    FacultyUpdate,
    FacultyResponse,
    FacultyListResponse,
)

router = APIRouter(prefix="/faculty", tags=["College Faculty"])


@router.get("/", response_model=FacultyListResponse)
async def list_faculty(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all faculty"""
    service = FacultyService()
    return await service.list_faculty(db, skip, limit)


@router.get("/department/{department_id}")
async def list_faculty_by_department(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List faculty by department"""
    service = FacultyService()
    faculty = await service.list_faculty_by_department(db, department_id, skip, limit)
    return faculty


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get faculty by ID"""
    service = FacultyService()
    faculty = await service.get_faculty(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty


@router.post("/", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    faculty_data: FacultyCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new faculty"""
    service = FacultyService()
    try:
        return await service.create_faculty(db, faculty_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: int,
    faculty_data: FacultyUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update faculty"""
    service = FacultyService()
    faculty = await service.update_faculty(db, faculty_id, faculty_data)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Delete faculty"""
    service = FacultyService()
    faculty = await service.get_faculty(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    await service.delete_faculty(db, faculty_id)
