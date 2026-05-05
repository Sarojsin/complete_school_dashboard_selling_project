"""
College Program Router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import ProgramService
from .schemas import ProgramResponse

router = APIRouter(prefix="/programs", tags=["College Programs"], dependencies=[Depends(require_college_portal)])


@router.get("/", response_model=List[ProgramResponse])
async def list_programs(
    department_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all academic programs (optionally filtered by department)"""
    service = ProgramService(db)
    if department_id:
        return await service.get_programs_by_department(department_id)
    return await service.get_all_programs(skip, limit)


@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get program details"""
    service = ProgramService(db)
    program = await service.get_program(program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


__all__ = ["router"]
