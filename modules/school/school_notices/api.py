from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os
import shutil
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_authority, require_school_teacher
from modules.shared.models import User
from .repository import NoticeRepository
from .schemas import NoticeCreate, NoticeUpdate, NoticeResponse
from modules.shared.config import settings

router = APIRouter(dependencies=[Depends(require_school_portal)])


# AUTHORITY/TEACHER ENDPOINTS

@router.post("/", response_model=NoticeResponse)
async def create_notice(
    notice: NoticeCreate,
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Create a new notice (Authority only)"""
    authority = await AuthorityRepository().get_by_user_id(db, current_user.id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority profile not found")

    notice_data = notice.model_dump()
    notice_data['authority_id'] = authority.id

    created_notice = await NoticeRepository.create(db, notice_data)
    return created_notice


@router.post("/{notice_id}/upload")
async def upload_notice_file(
    notice_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Upload file attachment for notice (Authority only)"""
    notice = await NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/notices"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{notice_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update notice
    updated_notice = await NoticeRepository.update(db, notice, file_path=file_path)

    return {"message": "File uploaded successfully", "file_path": file_path}


@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    notice_update: NoticeUpdate,
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Update notice (Authority only)"""
    notice = await NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    updated_notice = await NoticeRepository.update(
        db, notice, **notice_update.model_dump(exclude_unset=True)
    )
    return updated_notice


@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Delete notice (Authority only)"""
    notice = await NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    await NoticeRepository.delete(db, notice)
    return {"message": "Notice deleted successfully"}


# COMMON ENDPOINTS

@router.get("/", response_model=List[NoticeResponse])
async def get_notices(
    skip: int = 0,
    limit: int = 100,
    priority: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get active notices for current user"""
    target_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    notices = await NoticeRepository.get_all(
        db, skip=skip, limit=limit, priority=priority, target_role=target_role
    )
    return notices


@router.get("/urgent", response_model=List[NoticeResponse])
async def get_urgent_notices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get urgent notices"""
    target_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    notices = await NoticeRepository.get_urgent_notices(db, target_role=target_role)
    return notices


@router.get("/recent", response_model=List[NoticeResponse])
async def get_recent_notices(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recent notices from last N days"""
    target_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    notices = await NoticeRepository.get_recent_notices(db, days=days, target_role=target_role)
    return notices


@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific notice"""
    notice = await NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice


@router.get("/search/", response_model=List[NoticeResponse])
async def search_notices(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search notices"""
    target_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    notices = await NoticeRepository.search_notices(db, query, target_role=target_role)
    return notices