"""
College Dean API Routes

API endpoints for college dean/authority management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import Department, Program, Faculty, CollegeStudent
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/dean", tags=["College Dean"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_dean_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dean dashboard with college overview"""
    # Get department count
    dept_count = await db.execute(select(func.count(Department.id)))
    
    # Get program count
    prog_count = await db.execute(select(func.count(Program.id)))
    
    # Get faculty count
    faculty_count = await db.execute(select(func.count(Faculty.id)))
    
    # Get student count
    student_count = await db.execute(select(func.count(CollegeStudent.id)))
    
    return {
        "departments": dept_count.scalar() or 0,
        "programs": prog_count.scalar() or 0,
        "faculty": faculty_count.scalar() or 0,
        "students": student_count.scalar() or 0
    }


@router.get("/departments")
async def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all departments"""
    result = await db.execute(
        select(Department).offset(skip).limit(limit)
    )
    departments = result.scalars().all()
    return {"departments": departments}


@router.get("/departments/{dept_id}")
async def get_department(
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get department details"""
    result = await db.execute(
        select(Department).where(Department.id == dept_id)
    )
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


@router.get("/programs")
async def get_programs(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all programs"""
    query = select(Program)
    if department_id:
        query = query.where(Program.department_id == department_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    programs = result.scalars().all()
    return {"programs": programs}


@router.get("/faculty")
async def get_faculty(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all faculty members"""
    query = select(Faculty)
    if department_id:
        query = query.where(Faculty.department_id == department_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    faculty = result.scalars().all()
    return {"faculty": [
        {
            "id": f.id,
            "employee_id": f.employee_id,
            "designation": f.designation,
            "qualification": f.qualification,
            "department_id": f.department_id
        }
        for f in faculty
    ]}


@router.get("/students")
async def get_students(
    program_id: Optional[int] = None,
    semester: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all college students"""
    query = select(CollegeStudent)
    if program_id:
        query = query.where(CollegeStudent.program_id == program_id)
    if semester:
        query = query.where(CollegeStudent.semester == semester)
    
    result = await db.execute(query.offset(skip).limit(limit))
    students = result.scalars().all()
    return {"students": [
        {
            "id": s.id,
            "roll_number": s.roll_number,
            "program_id": s.program_id,
            "semester_id": s.semester_id,
            "cgpa": s.cgpa
        }
        for s in students
    ]}


__all__ = ["router"]
