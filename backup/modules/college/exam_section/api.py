# College Exam Section API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_async_db
from modules.shared.models import User
from modules.shared.auth import get_current_user
from backup.modules.college.exam_section.schemas import ExamSchedule, ExamScheduleCreate, ExamScheduleUpdate
from backup.modules.college.exam_section.service import ExamScheduleService
from backup.modules.college.exam_section.repository import ExamScheduleRepository

router = APIRouter(prefix="/exam-schedules", tags=["College Exam Section"])


def get_exam_service(db: AsyncSession = Depends(get_async_db)) -> ExamScheduleService:
    return ExamScheduleService(ExamScheduleRepository(db))


@router.post("/", response_model=ExamSchedule, status_code=status.HTTP_201_CREATED)
async def create_exam(
    data: ExamScheduleCreate,
    current_user: User = Depends(get_current_user),
    service: ExamScheduleService = Depends(get_exam_service)
):
    return await service.create(data)


@router.get("/{exam_id}", response_model=ExamSchedule)
async def get_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    service: ExamScheduleService = Depends(get_exam_service)
):
    exam = await service.get(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.get("/", response_model=List[ExamSchedule])
async def list_exams(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: ExamScheduleService = Depends(get_exam_service)
):
    return await service.get_all(skip, limit)


@router.put("/{exam_id}", response_model=ExamSchedule)
async def update_exam(
    exam_id: int,
    data: ExamScheduleUpdate,
    current_user: User = Depends(get_current_user),
    service: ExamScheduleService = Depends(get_exam_service)
):
    exam = await service.update(exam_id, data)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    service: ExamScheduleService = Depends(get_exam_service)
):
    success = await service.delete(exam_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exam not found")


__all__ = ["router"]
