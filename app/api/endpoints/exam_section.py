from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_async_db, get_current_user
from app.models.models import User, UserRole
from app.repositories.exam_repository import ExamRepository
from app.services.exam_service import ExamService
from app.schemas.exam_schemas import ExamResultCreate, ExamResultResponse

router = APIRouter(prefix="/api/exam", tags=["Exam Section"])

@router.post("/results", response_model=ExamResultResponse)
async def publish_exam_result(
    result_data: ExamResultCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Only Exam Section can publish results")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    return await service.publish_result(result_data, current_user.id)

@router.get("/results", response_model=List[ExamResultResponse])
async def get_all_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Only Exam Section can view all results")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    return await service.get_all_results()

@router.get("/results/student/{student_id}", response_model=List[ExamResultResponse])
async def get_student_results(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    # Students can view their own results, teachers can view their students
    if current_user.role == UserRole.STUDENT and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Can only view own results")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    return await service.get_student_results(student_id)
