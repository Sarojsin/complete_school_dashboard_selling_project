# School Student API Routes
# ======================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from modules.shared.database import get_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from modules.school.school_student.models import SchoolStudent

router = APIRouter(prefix="/students", tags=["School Students"])


@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the current logged-in student's profile."""
    result = await db.execute(
        select(SchoolStudent).where(SchoolStudent.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found for the current user"
        )
    return {
        "id": student.id,
        "user_id": student.user_id,
        "student_id": student.student_id,
        "full_name": student.full_name,
        "grade_level": student.grade_level,
        "section": student.section,
        "roll_number": student.roll_number,
        "phone": student.phone,
        "address": student.address,
        "parent_name": student.parent_name,
        "parent_phone": student.parent_phone,
        "enrollment_date": str(student.enrollment_date) if student.enrollment_date else None,
    }


@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the current student's dashboard data."""
    result = await db.execute(
        select(SchoolStudent).where(SchoolStudent.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found for the current user"
        )
    return {
        "student": {
            "id": student.id,
            "student_id": student.student_id,
            "full_name": student.full_name,
            "grade_level": student.grade_level,
            "section": student.section,
            "roll_number": student.roll_number,
        },
        "summary": {
            "assignments_pending": 0,
            "upcoming_tests": 0,
            "attendance_percentage": 0,
            "notices": 0,
        }
    }


@router.get("/{student_id}")
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(SchoolStudent).where(SchoolStudent.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.get("/")
async def list_students(
    grade_level: Optional[str] = None,
    section: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(SchoolStudent)
    if grade_level:
        query = query.where(SchoolStudent.grade_level == grade_level)
    if section:
        query = query.where(SchoolStudent.section == section)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


__all__ = ["router"]
