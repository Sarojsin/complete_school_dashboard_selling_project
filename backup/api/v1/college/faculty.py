"""
College Faculty API
===================
Faculty endpoints for college mode.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.api.v1.college.auth import require_college_user
from backup.models.models import User
from backup.models.college import Faculty
from backup.schemas.college_faculty import (
    FacultyCreate,
    FacultyUpdate,
    FacultyResponse,
)

router = APIRouter(prefix="/faculty", tags=["Faculty"])


@router.get("/me", response_model=FacultyResponse)
async def get_my_profile(
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current faculty member's profile"""
    result = await db.execute(
        select(Faculty).filter(Faculty.user_id == current_user.id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    return faculty


@router.put("/me", response_model=FacultyResponse)
async def update_my_profile(
    faculty_update: FacultyUpdate,
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current faculty member's profile"""
    result = await db.execute(
        select(Faculty).filter(Faculty.user_id == current_user.id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    
    # Update fields
    update_data = faculty_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faculty, field, value)
    
    await db.commit()
    await db.refresh(faculty)
    return faculty


@router.get("/", response_model=List[FacultyResponse])
async def list_faculty(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    designation: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """List all faculty members with optional filtering"""
    query = select(Faculty)
    
    if department_id:
        query = query.filter(Faculty.department_id == department_id)
    if designation:
        query = query.filter(Faculty.designation == designation)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    faculty = result.scalars().all()
    return faculty


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get faculty member by ID"""
    result = await db.execute(
        select(Faculty).filter(Faculty.id == faculty_id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty


@router.post("/", response_model=FacultyResponse, status_code=201)
async def create_faculty(
    faculty_data: FacultyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create new faculty member"""
    # Check if user already has a faculty profile
    result = await db.execute(
        select(Faculty).filter(Faculty.user_id == faculty_data.user_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Faculty profile already exists")
    
    # Check if employee_id is unique
    result = await db.execute(
        select(Faculty).filter(Faculty.employee_id == faculty_data.employee_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    faculty = Faculty(**faculty_data.model_dump())
    db.add(faculty)
    await db.commit()
    await db.refresh(faculty)
    return faculty


@router.delete("/{faculty_id}")
async def delete_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a faculty member"""
    result = await db.execute(
        select(Faculty).filter(Faculty.id == faculty_id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    await db.delete(faculty)
    await db.commit()
    return {"message": "Faculty deleted successfully"}


__all__ = ["router"]
