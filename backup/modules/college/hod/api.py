# College HOD API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from modules.shared.database import get_async_db
from modules.shared.models import User
from modules.shared.auth import get_current_user
from backup.modules.college.hod.schemas import HOD, HODCreate, HODUpdate
from backup.modules.college.hod.service import HODService
from backup.modules.college.hod.repository import HODRepository

router = APIRouter(prefix="/hods", tags=["College HOD"])


def get_hod_service(db: AsyncSession = Depends(get_async_db)) -> HODService:
    return HODService(HODRepository(db))


@router.post("/", response_model=HOD, status_code=status.HTTP_201_CREATED)
async def create_hod(
    data: HODCreate,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    return await service.create(data)


@router.get("/{hod_id}", response_model=HOD)
async def get_hod(
    hod_id: int,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    hod = await service.get(hod_id)
    if not hod:
        raise HTTPException(status_code=404, detail="HOD not found")
    return hod


@router.get("/department/{department_id}", response_model=HOD)
async def get_hod_by_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    hod = await service.get_by_department(department_id)
    if not hod:
        raise HTTPException(status_code=404, detail="HOD not found for department")
    return hod


@router.get("/", response_model=List[HOD])
async def list_hods(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    return await service.get_all(skip, limit)


@router.put("/{hod_id}", response_model=HOD)
async def update_hod(
    hod_id: int,
    data: HODUpdate,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    hod = await service.update(hod_id, data)
    if not hod:
        raise HTTPException(status_code=404, detail="HOD not found")
    return hod


@router.delete("/{hod_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(
    hod_id: int,
    current_user: User = Depends(get_current_user),
    service: HODService = Depends(get_hod_service)
):
    success = await service.delete(hod_id)
    if not success:
        raise HTTPException(status_code=404, detail="HOD not found")


__all__ = ["router"]
