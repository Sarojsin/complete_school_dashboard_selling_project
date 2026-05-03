"""
College Programs API
===================
Program endpoints for college mode.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.college import Program

router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/")
async def list_programs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """List all programs"""
    res = await db.execute(
        select(Program).offset(skip).limit(limit)
    )
    programs = res.scalars().all()
    return programs


@router.get("/{program_id}")
async def get_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get program by ID"""
    res = await db.execute(
        select(Program).filter(Program.id == program_id)
    )
    program = res.scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


__all__ = ["router"]
