"""
Admin Exam & Result Management API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API endpoints for managing exams, grading scales, and results.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminExamService`.
- No direct database manipulations in the routing layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.core.database import get_async_db
from backup.models.models import User
from backup.api.deps.admin import get_current_admin
from backup.services.admin_exam_service import AdminExamService, ExamNoticeCreateDto


# Create router
router = APIRouter(prefix="/admin/exams", tags=["Admin Exams"])


# ============ EXAM TYPES ============

@router.get("/types")
async def get_exam_types():
    """Get all exam types"""
    return AdminExamService.get_exam_types()


# ============ GRADING SCALE ============

@router.get("/grading-scale")
async def get_grading_scale():
    """Get the default grading scale"""
    return AdminExamService.get_grading_scale()


# ============ EXAM RESULTS ============

@router.get("/results")
async def get_exam_results(
    course_id: Optional[int] = None,
    exam_type: Optional[str] = None,
    is_published: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get exam results with filtering"""
    return await AdminExamService.get_exam_results(db, course_id, exam_type, is_published, skip, limit)


@router.post("/results/publish")
async def publish_results(
    course_id: int,
    exam_type: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Publish exam results for a specific course and exam type"""
    return await AdminExamService.publish_results(db, course_id, exam_type, current_user.id)


@router.post("/results/unpublish")
async def unpublish_results(
    course_id: int,
    exam_type: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Unpublish (lock) exam results"""
    return await AdminExamService.unpublish_results(db, course_id, exam_type)


# ============ EXAM NOTICES ============

@router.get("/notices")
async def get_exam_notices(
    notice_type: Optional[str] = None,
    upcoming: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get exam notices"""
    return await AdminExamService.get_exam_notices(db, notice_type, upcoming, skip, limit)


@router.post("/notices")
async def create_exam_notice(
    notice_data: ExamNoticeCreateDto,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new exam notice"""
    return await AdminExamService.create_exam_notice(db, notice_data, current_user.id)


# ============ STATISTICS ============

@router.get("/stats")
async def get_exam_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get exam statistics"""
    return await AdminExamService.get_exam_stats(db)


# ============ REPORT CARDS (PDF GENERATION) ============

@router.get("/report-card/{student_id}")
async def generate_report_card(
    student_id: int,
    semester: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate report card data for a student"""
    return await AdminExamService.generate_report_card(db, student_id, semester)
