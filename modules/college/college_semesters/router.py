"""
College Semester Router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import SemesterService
from .schemas import SemesterResponse

router = APIRouter(prefix="/semesters", tags=["College Semesters"], dependencies=[Depends(require_college_portal)])


@router.get("/", response_model=List[SemesterResponse])
async def list_semesters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all academic semesters"""
    service = SemesterService(db)
    return await service.get_all_semesters(skip, limit)


@router.get("/{semester_id}", response_model=SemesterResponse)
async def get_semester(
    semester_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get semester details"""
    service = SemesterService(db)
    semester = await service.get_semester(semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@router.get("/current", response_model=SemesterResponse)
async def get_current_semester(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get currently active semester"""
    service = SemesterService(db)
    semester = await service.get_current_semester()
    if not semester:
        raise HTTPException(status_code=404, detail="No current semester set")
    return semester


__all__ = ["router"]
