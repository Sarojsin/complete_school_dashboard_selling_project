# College Dean API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from modules.shared.database import get_async_db
from modules.shared.models import User
from modules.shared.auth import get_current_user
from backup.modules.college.dean.schemas import Dean, DeanCreate, DeanUpdate
from backup.modules.college.dean.service import DeanService
from backup.modules.college.dean.repository import DeanRepository

router = APIRouter(prefix="/deans", tags=["College Dean"])


def get_dean_service(db: AsyncSession = Depends(get_async_db)) -> DeanService:
    return DeanService(DeanRepository(db))


@router.post("/", response_model=Dean, status_code=status.HTTP_201_CREATED)
async def create_dean(
    data: DeanCreate,
    current_user: User = Depends(get_current_user),
    service: DeanService = Depends(get_dean_service)
):
    return await service.create(data)


@router.get("/{dean_id}", response_model=Dean)
async def get_dean(
    dean_id: int,
    current_user: User = Depends(get_current_user),
    service: DeanService = Depends(get_dean_service)
):
    dean = await service.get(dean_id)
    if not dean:
        raise HTTPException(status_code=404, detail="Dean not found")
    return dean


@router.get("/", response_model=List[Dean])
async def list_deans(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: DeanService = Depends(get_dean_service)
):
    return await service.get_all(skip, limit)


@router.put("/{dean_id}", response_model=Dean)
async def update_dean(
    dean_id: int,
    data: DeanUpdate,
    current_user: User = Depends(get_current_user),
    service: DeanService = Depends(get_dean_service)
):
    dean = await service.update(dean_id, data)
    if not dean:
        raise HTTPException(status_code=404, detail="Dean not found")
    return dean


@router.delete("/{dean_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dean(
    dean_id: int,
    current_user: User = Depends(get_current_user),
    service: DeanService = Depends(get_dean_service)
):
    success = await service.delete(dean_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dean not found")


__all__ = ["router"]
