"""
Student API Routes

API routes for student management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.college.student.service import StudentService
from backup.modules.college.student.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentListResponse,
)

router = APIRouter(prefix="/students", tags=["College Students"])


@router.get("/", response_model=StudentListResponse)
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all students"""
    service = StudentService()
    return await service.list_students(db, skip, limit)


@router.get("/program/{program_id}")
async def list_students_by_program(
    program_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List students by program"""
    service = StudentService()
    students = await service.list_students_by_program(db, program_id, skip, limit)
    return students


@router.get("/semester/{semester_id}")
async def list_students_by_semester(
    semester_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List students by semester"""
    service = StudentService()
    students = await service.list_students_by_semester(db, semester_id, skip, limit)
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get student by ID"""
    service = StudentService()
    student = await service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new student"""
    service = StudentService()
    try:
        return await service.create_student(db, student_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update student"""
    service = StudentService()
    student = await service.update_student(db, student_id, student_data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Delete student"""
    service = StudentService()
    student = await service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await service.delete_student(db, student_id)
