# College Lab API
# =============

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_async_db
from backup.modules.college.lab.repository import LabRepository
from backup.modules.college.lab.service import LabService
from backup.modules.college.lab.schemas import (
    LabCreate,
    LabUpdate,
    Lab,
    LabEquipmentCreate,
    LabEquipmentUpdate,
    LabEquipment,
    LabScheduleCreate,
    LabScheduleUpdate,
    LabSchedule,
)

router = APIRouter(prefix="/labs", tags=["College Labs"])


def get_service(db: AsyncSession = Depends(get_async_db)) -> LabService:
    repository = LabRepository(db)
    return LabService(repository)


# Lab endpoints
@router.post("", response_model=dict)
async def create_lab(
    data: LabCreate,
    service: LabService = Depends(get_service)
):
    return await service.create_lab(data)


@router.get("/{lab_id}", response_model=dict)
async def get_lab(
    lab_id: int,
    service: LabService = Depends(get_service)
):
    result = await service.get_lab(lab_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lab not found")
    return result


@router.get("", response_model=list)
async def get_all_labs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    department_id: Optional[int] = None,
    service: LabService = Depends(get_service)
):
    if department_id:
        return await service.get_labs_by_department(department_id)
    return await service.get_all_labs(skip, limit)


@router.put("/{lab_id}", response_model=dict)
async def update_lab(
    lab_id: int,
    data: LabUpdate,
    service: LabService = Depends(get_service)
):
    result = await service.update_lab(lab_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Lab not found")
    return result


@router.delete("/{lab_id}")
async def delete_lab(
    lab_id: int,
    service: LabService = Depends(get_service)
):
    if not await service.delete_lab(lab_id):
        raise HTTPException(status_code=404, detail="Lab not found")
    return {"message": "Lab deleted successfully"}


# Equipment endpoints
@router.post("/equipment", response_model=dict)
async def create_equipment(
    data: LabEquipmentCreate,
    service: LabService = Depends(get_service)
):
    return await service.create_equipment(data)


@router.get("/equipment/{equipment_id}", response_model=dict)
async def get_equipment(
    equipment_id: int,
    service: LabService = Depends(get_service)
):
    result = await service.get_equipment(equipment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result


@router.get("/equipment", response_model=list)
async def get_all_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    lab_id: Optional[int] = None,
    service: LabService = Depends(get_service)
):
    if lab_id:
        return await service.get_equipment_by_lab(lab_id)
    return await service.get_all_equipment(skip, limit)


@router.put("/equipment/{equipment_id}", response_model=dict)
async def update_equipment(
    equipment_id: int,
    data: LabEquipmentUpdate,
    service: LabService = Depends(get_service)
):
    result = await service.update_equipment(equipment_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result


@router.delete("/equipment/{equipment_id}")
async def delete_equipment(
    equipment_id: int,
    service: LabService = Depends(get_service)
):
    if not await service.delete_equipment(equipment_id):
        raise HTTPException(status_code=404, detail="Equipment not found")
    return {"message": "Equipment deleted successfully"}


# Schedule endpoints
@router.post("/schedule", response_model=dict)
async def create_schedule(
    data: LabScheduleCreate,
    service: LabService = Depends(get_service)
):
    return await service.create_schedule(data)


@router.get("/schedule/{schedule_id}", response_model=dict)
async def get_schedule(
    schedule_id: int,
    service: LabService = Depends(get_service)
):
    result = await service.get_schedule(schedule_id)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return result


@router.get("/schedule", response_model=list)
async def get_all_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    lab_id: Optional[int] = None,
    service: LabService = Depends(get_service)
):
    if lab_id:
        return await service.get_schedules_by_lab(lab_id)
    return await service.get_all_schedules(skip, limit)


@router.put("/schedule/{schedule_id}", response_model=dict)
async def update_schedule(
    schedule_id: int,
    data: LabScheduleUpdate,
    service: LabService = Depends(get_service)
):
    result = await service.update_schedule(schedule_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return result


@router.delete("/schedule/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    service: LabService = Depends(get_service)
):
    if not await service.delete_schedule(schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}


__all__ = ["router"]
