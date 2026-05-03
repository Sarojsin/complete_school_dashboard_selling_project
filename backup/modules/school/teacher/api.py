# School Teacher API Routes
# ======================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.school.teacher.schemas import Teacher, TeacherCreate, TeacherUpdate
from backup.modules.school.teacher.service import TeacherService
from backup.modules.school.teacher.repository import TeacherRepository

router = APIRouter(prefix="/teachers", tags=["School Teachers"])


def get_teacher_service(db: AsyncSession = Depends(get_async_db)) -> TeacherService:
    repository = TeacherRepository(db)
    return TeacherService(repository)


@router.post("/", response_model=Teacher, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    data: TeacherCreate,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{teacher_id}", response_model=Teacher)
async def get_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    teacher = await service.get(teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.get("/by-user/{user_id}", response_model=Teacher)
async def get_teacher_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    teacher = await service.get_by_user_id(user_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.get("/", response_model=List[Teacher])
async def list_teachers(
    department: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    return await service.get_all(department, status, skip, limit)


@router.put("/{teacher_id}", response_model=Teacher)
async def update_teacher(
    teacher_id: int,
    data: TeacherUpdate,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    teacher = await service.update(teacher_id, data)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    success = await service.delete(teacher_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")


@router.post("/{teacher_id}/deactivate", response_model=Teacher)
async def deactivate_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    service: TeacherService = Depends(get_teacher_service)
):
    teacher = await service.deactivate(teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


__all__ = ["router"]
