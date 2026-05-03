"""
College Students API
=====================
Student endpoints for college mode.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.api.v1.college.auth import require_college_user
from backup.models.models import User
from backup.models.college import CollegeStudent
from backup.schemas.college_student import (
    CollegeStudentCreate,
    CollegeStudentUpdate,
    CollegeStudentResponse,
)

router = APIRouter(prefix="/students", tags=["College Students"])


@router.get("/me", response_model=CollegeStudentResponse)
async def get_my_profile(
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current college student's profile"""
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


@router.put("/me", response_model=CollegeStudentResponse)
async def update_my_profile(
    student_update: CollegeStudentUpdate,
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current college student's profile"""
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Update fields
    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/", response_model=List[CollegeStudentResponse])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    program_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """List all college students with optional filtering"""
    query = select(CollegeStudent)
    
    if program_id:
        query = query.filter(CollegeStudent.program_id == program_id)
    if semester_id:
        query = query.filter(CollegeStudent.semester_id == semester_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    students = result.scalars().all()
    return students


@router.get("/{student_id}", response_model=CollegeStudentResponse)
async def get_student(
    student_id: int,
    current_user: User = Depends(require_college_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get college student by ID"""
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=CollegeStudentResponse, status_code=201)
async def create_student(
    student_data: CollegeStudentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create new college student"""
    # Check if user already has a student profile
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.user_id == student_data.user_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Student profile already exists")
    
    # Check if roll_number is unique
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.roll_number == student_data.roll_number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Roll number already exists")
    
    student = CollegeStudent(**student_data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a college student"""
    result = await db.execute(
        select(CollegeStudent).filter(CollegeStudent.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted successfully"}


__all__ = ["router"]
