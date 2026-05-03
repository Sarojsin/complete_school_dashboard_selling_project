"""
College Registrar API Routes

API endpoints for college registrar (student records).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import CollegeStudent, Enrollment, Program
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/registrar", tags=["College Registrar"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_registrar_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get registrar dashboard"""
    total_students = await db.execute(select(func.count(CollegeStudent.id)))
    total_programs = await db.execute(select(func.count(Program.id)))
    
    return {
        "total_students": total_students.scalar() or 0,
        "total_programs": total_programs.scalar() or 0
    }


@router.get("/students")
async def get_all_students(
    program_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all students"""
    query = select(CollegeStudent)
    if program_id:
        query = query.where(CollegeStudent.program_id == program_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    students = result.scalars().all()
    return {"students": students}


@router.get("/students/{student_id}")
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get student details"""
    result = await db.execute(
        select(CollegeStudent).where(CollegeStudent.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/enrollments")
async def get_enrollments(
    student_id: int = None,
    program_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get student enrollments"""
    query = select(Enrollment)
    if student_id:
        query = query.where(Enrollment.student_id == student_id)
    
    result = await db.execute(query)
    enrollments = result.scalars().all()
    return {"enrollments": enrollments}


__all__ = ["router"]
