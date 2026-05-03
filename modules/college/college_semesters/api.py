"""
College Semesters API
===================
Semester endpoints for college mode.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from modules.college.database import get_college_async_db as get_async_db
from modules.shared.models import User
from backup.models.college import Semester
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/semesters", tags=["Semesters"], dependencies=[Depends(require_college_portal)])


@router.get("/")
async def list_semesters(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """List all semesters"""
    res = await db.execute(
        select(Semester).offset(skip).limit(limit)
    )
    semesters = res.scalars().all()
    return semesters


@router.get("/{semester_id}")
async def get_semester(
    semester_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get semester by ID"""
    res = await db.execute(
        select(Semester).filter(Semester.id == semester_id)
    )
    semester = res.scalar_one_or_none()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


__all__ = ["router"]
