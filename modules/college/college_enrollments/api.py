"""
College Enrollment API Endpoints
================================

Enrollment endpoints for college mode (student course enrollment).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from modules.college.database import get_college_async_db as get_async_db
from modules.shared.models import User
# Importing from consolidated models file
from backup.models.college import Enrollment, CollegeCourse, Semester
from backup.models.college.student import CollegeStudent
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/enrollments", tags=["College Enrollments"], dependencies=[Depends(require_college_portal)])


@router.get("")
async def get_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get enrollments with optional filters"""
    query = select(Enrollment)
    
    if student_id:
        query = query.where(Enrollment.student_id == student_id)
    if course_id:
        query = query.where(Enrollment.course_id == course_id)
    if semester_id:
        query = query.where(Enrollment.semester_id == semester_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    enrollments = result.scalars().all()
    
    return {
        "enrollments": [
            {
                "id": e.id,
                "student_id": e.student_id,
                "course_id": e.course_id,
                "semester_id": e.semester_id,
                "enrollment_date": e.enrollment_date.isoformat() if e.enrollment_date else None,
                "status": e.status,
                "grade": e.grade,
                "grade_points": e.grade_points
            }
            for e in enrollments
        ]
    }


@router.get("/{enrollment_id}")
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get enrollment by ID"""
    result = await db.execute(
        select(Enrollment).where(Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    return {
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "semester_id": enrollment.semester_id,
        "enrollment_date": enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
        "status": enrollment.status,
        "grade": enrollment.grade,
        "grade_points": enrollment.grade_points
    }


@router.post("")
async def enroll_student(
    student_id: int,
    course_id: int,
    semester_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Enroll a student in a course"""
    # Check if student exists
    result = await db.execute(
        select(CollegeStudent).where(CollegeStudent.id == student_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Student not found")
    
    # Check if course exists
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.id == course_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Course not found")
    
    # Check if already enrolled
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.semester_id == semester_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        semester_id=semester_id,
        status="enrolled"
    )
    
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    
    return {
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "message": "Student enrolled successfully"
    }


@router.patch("/{enrollment_id}")
async def update_enrollment(
    enrollment_id: int,
    status: Optional[str] = None,
    grade: Optional[str] = None,
    grade_points: Optional[float] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update enrollment (status, grade)"""
    result = await db.execute(
        select(Enrollment).where(Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    if status:
        enrollment.status = status
    if grade:
        enrollment.grade = grade
    if grade_points is not None:
        enrollment.grade_points = grade_points
    
    await db.commit()
    await db.refresh(enrollment)
    
    return {
        "id": enrollment.id,
        "status": enrollment.status,
        "grade": enrollment.grade,
        "message": "Enrollment updated successfully"
    }


@router.delete("/{enrollment_id}")
async def drop_course(
    enrollment_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Drop a course enrollment"""
    result = await db.execute(
        select(Enrollment).where(Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    await db.delete(enrollment)
    await db.commit()
    
    return {"message": "Course dropped successfully"}
