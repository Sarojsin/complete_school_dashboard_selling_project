"""
College Exam Section API Routes

API endpoints for college exams and results.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.college.database import get_college_async_db
from modules.shared.models import User
from backup.models.exam_models import ExamResult
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/exam-section", tags=["College Exam Section"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_exam_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get exam section dashboard"""
    return {"message": "College exam section dashboard"}


@router.get("/results")
async def get_results(
    student_id: int = None,
    course_id: int = None,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get exam results"""
    query = select(ExamResult)
    if student_id:
        query = query.where(ExamResult.student_id == student_id)
    if course_id:
        query = query.where(ExamResult.course_id == course_id)
    
    result = await db.execute(query)
    results = result.scalars().all()
    return {"results": results}


__all__ = ["router"]
