# School Parent API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User
from backup.modules.school.parent.schemas import Parent, ParentCreate, ParentUpdate
from backup.modules.school.parent.service import ParentService
from backup.modules.school.parent.repository import ParentRepository

router = APIRouter(prefix="/parents", tags=["School Parents"])


def get_parent_service(db: AsyncSession = Depends(get_async_db)) -> ParentService:
    return ParentService(ParentRepository(db))


@router.post("/", response_model=Parent, status_code=status.HTTP_201_CREATED)
async def create_parent(
    data: ParentCreate,
    current_user: User = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service)
):
    return await service.create(data)


@router.get("/{parent_id}", response_model=Parent)
async def get_parent(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service)
):
    parent = await service.get(parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.get("/", response_model=List[Parent])
async def list_parents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service)
):
    return await service.get_all(skip, limit)


@router.put("/{parent_id}", response_model=Parent)
async def update_parent(
    parent_id: int,
    data: ParentUpdate,
    current_user: User = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service)
):
    parent = await service.update(parent_id, data)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.delete("/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parent(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service)
):
    success = await service.delete(parent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Parent not found")


__all__ = ["router"]
