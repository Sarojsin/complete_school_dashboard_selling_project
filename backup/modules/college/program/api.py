"""
Program API Routes

API routes for program management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.college.program.service import ProgramService
from backup.modules.college.program.schemas import (
    ProgramCreate,
    ProgramUpdate,
    ProgramResponse,
    ProgramListResponse,
)

router = APIRouter(prefix="/programs", tags=["College Programs"])


@router.get("/", response_model=ProgramListResponse)
async def list_programs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    service = ProgramService()
    return await service.list_programs(db, skip, limit)


@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(
    program_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    service = ProgramService()
    program = await service.get_program(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.post("/", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    program_data: ProgramCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    service = ProgramService()
    try:
        return await service.create_program(db, program_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
