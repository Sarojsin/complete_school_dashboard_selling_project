"""
College Registrar Router

FastAPI endpoints for academic records and enrollment oversight.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal, require_registrar
from modules.shared.models import User
from .service import RegistrarService
from .schemas import RegistrarDashboardResponse, StudentDetailSchema, EnrollmentDetailSchema, StudentAcademicRecord

router = APIRouter(
    prefix="/registrar",
    tags=["College Registrar"],
    dependencies=[Depends(require_college_portal)]
)


@router.get("/dashboard", response_model=RegistrarDashboardResponse)
async def get_registrar_dashboard(
    current_user: User = Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get registrar dashboard statistics"""
    service = RegistrarService(db)
    data = await service.get_dashboard()
    return data["stats"]


@router.get("/students", response_model=List[StudentDetailSchema])
async def list_students(
    program_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all students (Registrar, Dean)"""
    service = RegistrarService(db)
    return await service.list_students(program_id, skip, limit)


@router.get("/students/{student_id}", response_model=Dict)
async def get_student_detail(
    student_id: int,
    current_user: User = Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get student details with enrollments"""
    service = RegistrarService(db)
    return await service.get_student_detail(student_id)


@router.get("/students/{student_id}/academic-record", response_model=StudentAcademicRecord)
async def get_student_academic_record(
    student_id: int,
    current_user: User = Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get full academic record (transcript) for a student"""
    service = RegistrarService(db)
    return await service.get_academic_record(student_id)


@router.get("/enrollments", response_model=List[EnrollmentDetailSchema])
async def list_enrollments(
    student_id: Optional[int] = None,
    program_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all enrollments (Registrar, Dean)"""
    service = RegistrarService(db)
    return await service.list_enrollments(student_id, program_id, skip, limit)


# Note: Full enrollment CRUD is handled by college_enrollments module.
# Registrar may have additional privileges to modify grades/status via that module.


__all__ = ["router"]
