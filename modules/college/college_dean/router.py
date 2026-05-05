"""
College Dean Router

FastAPI endpoints for dean-level oversight.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal, require_dean
from modules.shared.models import User
from .service import DeanService
from .schemas import (
    DeanDashboardResponse,
    DepartmentListSchema,
    ProgramListSchema,
    FacultySummarySchema,
    StudentSummarySchema
)

router = APIRouter(
    prefix="/dean",
    tags=["College Dean"],
    dependencies=[Depends(require_college_portal)]
)


@router.get("/dashboard", response_model=DeanDashboardResponse)
async def get_dean_dashboard(
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get dean dashboard with college overview"""
    service = DeanService(db)
    return await service.get_dashboard()


@router.get("/departments", response_model=List[DepartmentListSchema])
async def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all departments"""
    service = DeanService(db)
    return await service.get_departments(skip, limit)


@router.get("/departments/{dept_id}", response_model=DepartmentListSchema)
async def get_department(
    dept_id: int,
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get department details"""
    service = DeanService(db)
    dept = await service.get_department_detail(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


@router.get("/programs", response_model=List[ProgramListSchema])
async def list_programs(
    department_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all academic programs"""
    service = DeanService(db)
    return await service.get_programs(department_id, skip, limit)


@router.get("/faculty", response_model=List[FacultySummarySchema])
async def list_faculty(
    department_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all faculty members"""
    service = DeanService(db)
    return await service.get_faculty(department_id, skip, limit)


@router.get("/students", response_model=List[StudentSummarySchema])
async def list_students(
    program_id: Optional[int] = None,
    semester: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all college students"""
    service = DeanService(db)
    return await service.get_students(program_id, semester, skip, limit)


__all__ = ["router"]
