# School Exam Section Router
# ==========================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_db, get_async_db, get_db, get_sync_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User, UserRole

from .repository import ExamSectionRepository
from .service import ExamSectionService
from .schemas import (
    ExamScheduleCreate,
    ExamScheduleUpdate,
    ExamSchedule,
    GradeCreate,
    GradeUpdate,
    Grade,
)

router = APIRouter(prefix="/exams", tags=["School Exams"], dependencies=[Depends(require_school_portal)])


def get_service(db: AsyncSession = Depends(get_db)) -> ExamSectionService:
    repository = ExamSectionRepository(db)
    return ExamSectionService(repository)


# Exam endpoints
@router.post("", response_model=dict)
async def create_exam(
    data: ExamScheduleCreate,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new exam schedule (teacher or authority only)"""
    if current_user.role not in [UserRole.TEACHER, UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create exams")
    return await service.create_exam(data)





@router.get("", response_model=list)
async def get_all_exams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    class_id: Optional[int] = None,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Get all exams or filter by class_id"""
    if class_id:
        return await service.get_exams_by_class(class_id)
    return await service.get_all_exams(skip, limit)





# Grade endpoints
@router.post("/grades", response_model=dict)
async def create_grade(
    data: GradeCreate,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new grade entry (teacher or authority only)"""
    if current_user.role not in [UserRole.TEACHER, UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create grades")
    return await service.create_grade(data)


@router.get("/grades/{grade_id}", response_model=dict)
async def get_grade(
    grade_id: int,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Get a specific grade by ID"""
    result = await service.get_grade(grade_id)
    if not result:
        raise HTTPException(status_code=404, detail="Grade not found")
    return result


@router.get("/grades", response_model=list)
async def get_all_grades(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    student_id: Optional[int] = None,
    exam_id: Optional[int] = None,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Get all grades or filter by student_id or exam_id"""
    if student_id:
        return await service.get_grades_by_student(student_id)
    if exam_id:
        return await service.get_grades_by_exam(exam_id)
    return await service.get_all_grades(skip, limit)


@router.put("/grades/{grade_id}", response_model=dict)
async def update_grade(
    grade_id: int,
    data: GradeUpdate,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Update a grade (teacher or authority only)"""
    if current_user.role not in [UserRole.TEACHER, UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to update grades")
    result = await service.update_grade(grade_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Grade not found")
    return result


@router.delete("/grades/{grade_id}")
async def delete_grade(
    grade_id: int,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Delete a grade (authority only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to delete grades")
    if not await service.delete_grade(grade_id):
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"message": "Grade deleted successfully"}



@router.get("/{exam_id}", response_model=dict)
async def get_exam(
    exam_id: int,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Get a specific exam by ID"""
    result = await service.get_exam(exam_id)
    if not result:
        raise HTTPException(status_code=404, detail="Exam not found")
    return result

@router.put("/{exam_id}", response_model=dict)
async def update_exam(
    exam_id: int,
    data: ExamScheduleUpdate,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Update an exam schedule (teacher or authority only)"""
    if current_user.role not in [UserRole.TEACHER, UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to update exams")
    result = await service.update_exam(exam_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Exam not found")
    return result

@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: int,
    service: ExamSectionService = Depends(get_service),
    current_user: User = Depends(get_current_user)
):
    """Delete an exam (authority only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to delete exams")
    if not await service.delete_exam(exam_id):
        raise HTTPException(status_code=404, detail="Exam not found")
    return {"message": "Exam deleted successfully"}

__all__ = ["router"]