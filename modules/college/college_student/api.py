"""
College Student API Routes

API endpoints for managing college students.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from modules.college.database import get_college_async_db
from modules.shared.models import User
from backup.models.college.student import CollegeStudent
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/students", tags=["College Students"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get college student dashboard with overview stats"""
    total_students = await db.execute(select(func.count(CollegeStudent.id)))
    
    # Get average CGPA
    avg_cgpa = await db.execute(
        select(func.avg(CollegeStudent.cgpa)).where(CollegeStudent.cgpa > 0)
    )
    
    return {
        "total_students": total_students.scalar() or 0,
        "average_cgpa": float(avg_cgpa.scalar() or 0)
    }


@router.get("/list")
async def list_students(
    program_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all college students"""
    query = select(CollegeStudent)
    
    if program_id:
        query = query.where(CollegeStudent.program_id == program_id)
    if semester_id:
        query = query.where(CollegeStudent.semester_id == semester_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    students = result.scalars().all()
    
    return {"students": [
        {
            "id": s.id,
            "user_id": s.user_id,
            "roll_number": s.roll_number,
            "program_id": s.program_id,
            "semester_id": s.semester_id,
            "cgpa": s.cgpa,
            "total_credits_completed": s.total_credits_completed,
            "enrollment_date": str(s.enrollment_date) if s.enrollment_date is not None else None
        }
        for s in students
    ]}


@router.get("/{student_id}")
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get college student details by ID"""
    result = await db.execute(select(CollegeStudent).where(CollegeStudent.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "id": student.id,
        "user_id": student.user_id,
        "roll_number": student.roll_number,
        "program_id": student.program_id,
        "semester_id": student.semester_id,
        "cgpa": student.cgpa,
        "total_credits_completed": student.total_credits_completed,
        "enrollment_date": str(student.enrollment_date) if student.enrollment_date else None
    }


@router.post("/")
async def create_student(
    user_id: int,
    roll_number: str,
    program_id: int,
    semester_id: Optional[int] = None,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new college student"""
    student = CollegeStudent(
        user_id=user_id,
        roll_number=roll_number,
        program_id=program_id,
        semester_id=semester_id
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    
    return {"student": student, "message": "Student created successfully"}


@router.put("/{student_id}/cgpa")
async def update_cgpa(
    student_id: int,
    cgpa: float,
    db: AsyncSession = Depends(get_college_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update student CGPA"""
    result = await db.execute(select(CollegeStudent).where(CollegeStudent.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.cgpa = float(cgpa)
    await db.commit()
    await db.refresh(student)
    
    return {"student": student, "message": "CGPA updated successfully"}


__all__ = ["router"]
