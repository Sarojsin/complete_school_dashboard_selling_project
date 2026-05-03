"""
College Student Router

FastAPI endpoints for college student operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import CollegeStudentService
from .schemas import (
    CollegeStudentResponse, CollegeStudentUpdate, CollegeStudentCreate,
    StudentCourseResponse, StudentGradeResponse, StudentEnrollmentResponse, HostelAllocationResponse
)

router = APIRouter(prefix="/students", tags=["College Students"], dependencies=[Depends(require_college_portal)])


@router.post("/", response_model=CollegeStudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    data: CollegeStudentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new college student (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create college students"
        )
    service = CollegeStudentService(db)
    return await service.create(data)


@router.get("/", response_model=List[CollegeStudentResponse])
async def list_students(
    skip: int = 0,
    limit: int = 20,
    program_id: int = None,
    semester_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all college students (Protected)"""
    service = CollegeStudentService(db)
    
    if program_id:
        return await service.list_by_program(program_id, skip, limit)
    elif semester_id:
        return await service.list_by_semester(semester_id, skip, limit)
    else:
        return await service.list_students(skip, limit)


@router.get("/me", response_model=CollegeStudentResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get current student profile (Protected)"""
    service = CollegeStudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student profile not found for current user")
    return student


@router.patch("/me", response_model=CollegeStudentResponse)
async def update_my_profile(
    student_data: CollegeStudentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update current student profile (Protected)"""
    service = CollegeStudentService(db)
    student = await service.update_profile(current_user.id, student_data)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student profile not found")
    return student


@router.get("/{student_id}", response_model=CollegeStudentResponse)
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get student by ID (Protected)"""
    service = CollegeStudentService(db)
    student = await service.get_student(student_id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student not found")
    return student


@router.put("/{student_id}", response_model=CollegeStudentResponse)
async def update_student(
    student_id: int,
    data: CollegeStudentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update student by ID (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update college students"
        )
    service = CollegeStudentService(db)
    student = await service.update(student_id, data)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete student by ID (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete college students"
        )
    service = CollegeStudentService(db)
    success = await service.delete(student_id)
    if not success:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student not found")


# ── Student Dashboard ─────────────────────────────────────
@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get college student dashboard (Protected)"""
    service = CollegeStudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("College student profile not found")
    
    return {
        "student_id": student.id,
        "roll_number": student.roll_number,
        "program_id": student.program_id,
        "semester_id": student.semester_id,
        "cgpa": student.cgpa,
        "total_credits": student.total_credits_completed,
        "message": "College student dashboard - extend with courses, enrollments, grades, etc."
    }


# ── Student's Courses ───────────────────────────────────────
@router.get("/my-courses", response_model=List[StudentCourseResponse])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get courses enrolled by current student (Protected)"""
    service = CollegeStudentService(db)
    return await service.get_my_courses(current_user.id)


# ── Student's Enrollments ───────────────────────────────────
@router.get("/my-enrollments", response_model=List[StudentEnrollmentResponse])
async def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get enrollments for current student (Protected)"""
    service = CollegeStudentService(db)
    return await service.get_my_enrollments(current_user.id)


# ── Student's Grades ─────────────────────────────────────────
@router.get("/my-grades", response_model=List[StudentGradeResponse])
async def get_my_grades(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get grades for current student (Protected)"""
    service = CollegeStudentService(db)
    return await service.get_my_grades(current_user.id)


# ── Student's Hostel ─────────────────────────────────────────
@router.get("/my-hostel", response_model=HostelAllocationResponse)
async def get_my_hostel(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get hostel allocation for current student (Protected)"""
    service = CollegeStudentService(db)
    allocation = await service.get_my_hostel_allocation(current_user.id)
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hostel allocation found"
        )
    return allocation


__all__ = ["router"]