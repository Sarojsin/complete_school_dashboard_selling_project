# College Registrar API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from modules.shared.database import get_async_db
from modules.shared.models import User
from modules.shared.auth import get_current_user
from backup.modules.college.registrar.schemas import Registrar, RegistrarCreate, RegistrarUpdate
from backup.modules.college.registrar.service import RegistrarService
from backup.modules.college.registrar.repository import RegistrarRepository

router = APIRouter(prefix="/registrars", tags=["College Registrar"])


def get_registrar_service(db: AsyncSession = Depends(get_async_db)) -> RegistrarService:
    return RegistrarService(RegistrarRepository(db))


@router.post("/", response_model=Registrar, status_code=status.HTTP_201_CREATED)
async def create_registrar(
    data: RegistrarCreate,
    current_user: User = Depends(get_current_user),
    service: RegistrarService = Depends(get_registrar_service)
):
    return await service.create(data)


@router.get("/{registrar_id}", response_model=Registrar)
async def get_registrar(
    registrar_id: int,
    current_user: User = Depends(get_current_user),
    service: RegistrarService = Depends(get_registrar_service)
):
    registrar = await service.get(registrar_id)
    if not registrar:
        raise HTTPException(status_code=404, detail="Registrar not found")
    return registrar


@router.get("/", response_model=List[Registrar])
async def list_registrars(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    service: RegistrarService = Depends(get_registrar_service)
):
    return await service.get_all(skip, limit)


@router.put("/{registrar_id}", response_model=Registrar)
async def update_registrar(
    registrar_id: int,
    data: RegistrarUpdate,
    current_user: User = Depends(get_current_user),
    service: RegistrarService = Depends(get_registrar_service)
):
    registrar = await service.update(registrar_id, data)
    if not registrar:
        raise HTTPException(status_code=404, detail="Registrar not found")
    return registrar


@router.delete("/{registrar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registrar(
    registrar_id: int,
    current_user: User = Depends(get_current_user),
    service: RegistrarService = Depends(get_registrar_service)
):
    success = await service.delete(registrar_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registrar not found")


__all__ = ["router"]
