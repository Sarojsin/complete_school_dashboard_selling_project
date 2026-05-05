"""
College Exam Section Router

FastAPI endpoints for exam results and notices.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal, require_exam_section
from modules.shared.models import User
from .service import ExamSectionService
from .schemas import (
    CollegeExamResultCreate,
    CollegeExamResultUpdate,
    CollegeExamResultResponse,
    CollegeExamNoticeCreate,
    CollegeExamNoticeResponse,
    ExamSectionDashboard
)

router = APIRouter(
    prefix="/exam_section",
    tags=["College Exam Section"],
    dependencies=[Depends(require_college_portal)]
)


# ── Exam Results ───────────────────────────────────────────────────

@router.post("/results", response_model=CollegeExamResultResponse, status_code=status.HTTP_201_CREATED)
async def publish_exam_result(
    result_data: CollegeExamResultCreate,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Publish an exam result (Exam Section only)"""
    service = ExamSectionService(db)
    try:
        return await service.publish_result(result_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/results", response_model=List[CollegeExamResultResponse])
async def get_all_results(
    semester_id: Optional[int] = None,
    exam_type: Optional[str] = None,
    is_published: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all exam results with filters (Exam Section only)"""
    # Permission: only exam section or super_admin
    if current_user.role not in ["exam_section", "super_admin", "dean"]:
        raise HTTPException(status_code=403, detail="Not authorized to view all results")

    service = ExamSectionService(db)
    return await service.get_all_results(semester_id, exam_type, is_published, skip, limit)


@router.get("/results/student/{student_id}", response_model=List[CollegeExamResultResponse])
async def get_student_results(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get results for a specific student (student can view own, teachers can view their students)"""
    # Students can view their own results only
    if current_user.role == "college_student" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Can only view own results")

    service = ExamSectionService(db)
    return await service.get_student_results(student_id)


@router.get("/results/{result_id}", response_model=CollegeExamResultResponse)
async def get_result_detail(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get single exam result detail"""
    service = ExamSectionService(db)
    result = await service.get_result_detail(result_id)
    return result


@router.patch("/results/{result_id}", response_model=CollegeExamResultResponse)
async def update_result(
    result_id: int,
    data: CollegeExamResultUpdate,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update exam result (marks, remarks) – Exam Section only"""
    service = ExamSectionService(db)
    return await service.update_result(result_id, data)


@router.post("/results/{result_id}/publish", response_model=CollegeExamResultResponse)
async def publish_result(
    result_id: int,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Publish an unpublished result (makes it visible to students)"""
    service = ExamSectionService(db)
    return await service.publish_result_by_id(result_id, current_user.id)


@router.post("/results/{result_id}/unpublish", response_model=CollegeExamResultResponse)
async def unpublish_result(
    result_id: int,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Unpublish a result (hide from students)"""
    service = ExamSectionService(db)
    return await service.unpublish_result(result_id)


@router.delete("/results/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_result(
    result_id: int,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete exam result (Exam Section only)"""
    service = ExamSectionService(db)
    await service.delete_result(result_id)


# ── Exam Notices ──────────────────────────────────────────────────

@router.post("/notices", response_model=CollegeExamNoticeResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_notice(
    notice_data: CollegeExamNoticeCreate,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create exam notice (Exam Section only)"""
    service = ExamSectionService(db)
    return await service.create_notice(notice_data, current_user.id)


@router.get("/notices", response_model=List[CollegeExamNoticeResponse])
async def list_exam_notices(
    is_active: bool = Query(True),
    semester_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all exam notices (public to college users)"""
    service = ExamSectionService(db)
    return await service.get_notices(is_active, semester_id)


@router.get("/notices/{notice_id}", response_model=CollegeExamNoticeResponse)
async def get_exam_notice(
    notice_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get single exam notice"""
    service = ExamSectionService(db)
    notice = await service.get_notice_detail(notice_id)
    return notice


@router.post("/notices/{notice_id}/deactivate")
async def deactivate_notice(
    notice_id: int,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Deactivate exam notice (soft delete)"""
    service = ExamSectionService(db)
    return await service.deactivate_notice(notice_id)


# ── Dashboard ─────────────────────────────────────────────────────

@router.get("/dashboard", response_model=ExamSectionDashboard)
async def get_exam_section_dashboard(
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get exam section dashboard (Exam Section only)"""
    service = ExamSectionService(db)
    dashboard_data = await service.get_dashboard_stats()
    return dashboard_data["dashboard"]


__all__ = ["router"]
