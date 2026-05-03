from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_exam_section
from modules.shared.models import User
from .models import ExamResult, ExamNotice, SchoolExamSchedule, ExamGrade

router = APIRouter()


# Exam Results Endpoints (for publishing and viewing results)

@router.post("/results")
async def publish_exam_result(
    student_id: int,
    exam_id: int,
    marks_obtained: float,
    max_marks: float,
    grade: Optional[str] = None,
    remarks: Optional[str] = None,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_db)
):
    """Publish exam result for a student (Exam Section only)"""
    # Use modular ExamResult
    result = ExamResult(
        student_id=student_id,
        exam_id=exam_id,
        marks_obtained=marks_obtained,
        max_marks=max_marks,
        grade=grade,
        remarks=remarks,
        published_at=datetime.utcnow()
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    
    return result


@router.get("/results")
async def get_all_results(
    exam_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_exam_section),
    db: AsyncSession = Depends(get_db)
):
    """Get all exam results (Exam Section only)"""
    # Use modular ExamResult
    from sqlalchemy import select
    query = select(ExamResult)
    if exam_id:
        query = query.where(ExamResult.exam_id == exam_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    results = result.scalars().all()
    
    return {"results": results}


@router.get("/results/student/{student_id}")
async def get_student_results(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get exam results for a specific student"""
    # Use modular ExamResult
    from sqlalchemy import select
    results_q = await db.execute(
        select(ExamResult).where(ExamResult.student_id == student_id)
    )
    results = result.scalars().all()
    
    return {"student_id": student_id, "results": results}


# Student results endpoint

@router.get("/my-results")
async def get_my_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current student's exam results"""
    # Use modular ExamResult
    from sqlalchemy import select
    from modules.school.school_student.repository import StudentRepository
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    repo = StudentRepository(db)
    student = await repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    results_q = await db.execute(
        select(ExamResult).where(ExamResult.student_id == student.id)
    )
    results = results_q.scalars().all()
    
    return {"results": results}


__all__ = ["router"]