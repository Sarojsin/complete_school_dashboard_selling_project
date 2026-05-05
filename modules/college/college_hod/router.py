"""
College HOD Router

FastAPI endpoints for department head operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal, require_hod
from modules.shared.models import User
from .service import HodService
from .schemas import HODDashboardResponse, DepartmentDetailResponse, FacultySchema, CourseSchema

router = APIRouter(
    prefix="/hod",
    tags=["College HOD"],
    dependencies=[Depends(require_college_portal)]
)


@router.get("/dashboard", response_model=HODDashboardResponse)
async def get_hod_dashboard(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get HOD dashboard with overview of departments"""
    service = HodService(db)
    return await service.get_dashboard(current_user.id)


@router.get("/departments", response_model=List[dict])
async def list_my_departments(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get departments where current user is HOD"""
    service = HodService(db)
    departments = await service.get_dashboard(current_user.id)
    return departments.departments


@router.get("/departments/{dept_id}", response_model=DepartmentDetailResponse)
async def get_department_detail(
    dept_id: int,
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get detailed info for a department (HOD access only)"""
    service = HodService(db)
    return await service.get_department_details(dept_id, current_user.id)


@router.get("/faculty", response_model=List[FacultySchema])
async def get_department_faculty(
    department_id: int,
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get faculty members in HOD's department"""
    service = HodService(db)
    return await service.get_department_faculty(department_id, current_user.id)


@router.get("/courses", response_model=List[CourseSchema])
async def get_department_courses(
    department_id: int,
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get courses in HOD's department"""
    service = HodService(db)
    return await service.get_department_courses(department_id, current_user.id)


__all__ = ["router"]
