"""
College Lab Router

FastAPI endpoints for college lab operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import LabService
from .schemas import (
    LabResponse, LabCreate, LabUpdate,
    EquipmentResponse, EquipmentCreate, EquipmentUpdate,
    ScheduleResponse, ScheduleCreate, ScheduleUpdate
)

router = APIRouter(prefix="/labs", tags=["College Labs"], dependencies=[Depends(require_college_portal)])


# ── Lab Endpoints ───────────────────────────────────────────────
@router.post("/", response_model=LabResponse, status_code=status.HTTP_201_CREATED)
async def create_lab(
    data: LabCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new lab (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = LabService(db)
    return await service.create_lab(data)


@router.get("/", response_model=List[LabResponse])
async def list_labs(
    skip: int = 0,
    limit: int = 20,
    department_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List labs (Protected)"""
    service = LabService(db)
    if department_id:
        return await service.list_by_department(department_id, skip, limit)
    return await service.list_labs(skip, limit)


@router.get("/{lab_id}", response_model=LabResponse)
async def get_lab(
    lab_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get lab by ID (Protected)"""
    service = LabService(db)
    lab = await service.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab not found")
    return lab


# ── Equipment Endpoints ─────────────────────────────────────────
@router.post("/{lab_id}/equipment", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def add_equipment(
    lab_id: int,
    data: EquipmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add equipment to lab (Protected - Dean/Faculty)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = LabService(db)
    data.lab_id = lab_id
    return await service.add_equipment(data)


@router.get("/{lab_id}/equipment", response_model=List[EquipmentResponse])
async def list_equipment(
    lab_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List lab equipment (Protected)"""
    service = LabService(db)
    return await service.list_equipment(lab_id, skip, limit)


# ── Schedule Endpoints ──────────────────────────────────────────
@router.post("/{lab_id}/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    lab_id: int,
    data: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create lab schedule (Protected - Dean/Faculty)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = LabService(db)
    data.lab_id = lab_id
    return await service.create_schedule(data)


@router.get("/{lab_id}/schedules", response_model=List[ScheduleResponse])
async def list_schedules(
    lab_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List lab schedules (Protected)"""
    service = LabService(db)
    return await service.list_schedules(lab_id, skip, limit)


__all__ = ["router"]