"""
Authority API Routes

API routes for authority management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_authority
from backup.modules.school.authority.service import AuthorityService
from backup.modules.school.authority.schemas import (
    AuthorityCreate,
    AuthorityUpdate,
    AuthorityResponse,
    AuthorityListResponse,
)
from modules.shared.models import User

router = APIRouter(prefix="/authorities", tags=["School Authority"])


@router.get("/", response_model=AuthorityListResponse)
async def list_authorities(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """List all authorities"""
    service = AuthorityService()
    return await service.list_authorities(db, skip, limit)


@router.get("/{authority_id}", response_model=AuthorityResponse)
async def get_authority(
    authority_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Get authority by ID"""
    service = AuthorityService()
    authority = await service.get_authority(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    return authority


@router.post("/", response_model=AuthorityResponse, status_code=status.HTTP_201_CREATED)
async def create_authority(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Create new authority"""
    service = AuthorityService()
    try:
        return await service.create_authority(db, authority_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{authority_id}", response_model=AuthorityResponse)
async def update_authority(
    authority_id: int,
    authority_data: AuthorityUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Update authority"""
    service = AuthorityService()
    authority = await service.update_authority(db, authority_id, authority_data)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    return authority


@router.delete("/{authority_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_authority(
    authority_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Delete authority"""
    service = AuthorityService()
    authority = await service.get_authority(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    await service.delete_authority(db, authority_id)
