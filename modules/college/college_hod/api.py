"""
College HOD API Routes

API endpoints for college department heads.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college import Department, Faculty, CollegeCourse
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/hod", tags=["College HOD"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_hod_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get HOD dashboard"""
    # Get departments where user is HOD
    result = await db.execute(
        select(Department).where(Department.hod_teacher_id == current_user.id)
    )
    departments = result.scalars().all()
    
    return {
        "departments_count": len(list(departments)),
        "departments": departments
    }


@router.get("/department/{dept_id}")
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


@router.get("/faculty")
async def get_department_faculty(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get faculty in department"""
    result = await db.execute(
        select(Faculty).where(Faculty.department_id == department_id)
    )
    faculty = result.scalars().all()
    return {"faculty": faculty}


@router.get("/courses")
async def get_department_courses(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get courses in department"""
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.department_id == department_id)
    )
    courses = result.scalars().all()
    return {"courses": courses}


__all__ = ["router"]
