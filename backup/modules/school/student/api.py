# School Student API Routes
# ======================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.school.student.schemas import Student, StudentCreate, StudentUpdate
from backup.modules.school.student.service import StudentService
from backup.modules.school.student.repository import StudentRepository

router = APIRouter(prefix="/students", tags=["School Students"])


def get_student_service(db: AsyncSession = Depends(get_async_db)) -> StudentService:
    repository = StudentRepository(db)
    return StudentService(repository)


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(
    data: StudentCreate,
    current_user: User = Depends(get_current_user),
    service: StudentService = Depends(get_student_service)
):
    return await service.create(data)


@router.get("/{student_id}", response_model=Student)
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    service: StudentService = Depends(get_student_service)
):
    student = await service.get(student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.get("/", response_model=List[Student])
async def list_students(
    grade_level: Optional[str] = None,
    section: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: StudentService = Depends(get_student_service)
):
    return await service.get_all(grade_level, section, skip, limit)


@router.put("/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    data: StudentUpdate,
    current_user: User = Depends(get_current_user),
    service: StudentService = Depends(get_student_service)
):
    student = await service.update(student_id, data)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    service: StudentService = Depends(get_student_service)
):
    success = await service.delete(student_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


__all__ = ["router"]
