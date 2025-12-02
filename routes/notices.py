from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from database.database import get_db
from dependencies import get_current_authority, get_current_user
from models.models import User, Authority
from repositories.notice_repository import NoticeRepository
from tables.tables import NoticeCreate, NoticeUpdate, NoticeResponse
from config.config import settings

router = APIRouter()

# AUTHORITY ENDPOINTS

@router.post("/", response_model=NoticeResponse)
async def create_notice(
    notice: NoticeCreate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Create a new notice (Authority only)"""
    authority = db.query(Authority).filter(Authority.user_id == current_user.id).first()
    if not authority:
        raise HTTPException(status_code=404, detail="Authority profile not found")
    
    notice_data = notice.dict()
    notice_data['authority_id'] = authority.id
    
    created_notice = NoticeRepository.create(db, notice_data)
    return created_notice

@router.post("/{notice_id}/upload")
async def upload_notice_file(
    notice_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Upload file attachment for notice (Authority only)"""
    notice = NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    # Validate file
    file_ext = os.path.splitext(file.filename)[1].lower().replace('.', '')
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/notices"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{notice_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update notice
    updated_notice = NoticeRepository.update(db, notice, file_path=file_path)
    
    return {"message": "File uploaded successfully", "file_path": file_path}

@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    notice_update: NoticeUpdate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Update notice (Authority only)"""
    notice = NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    updated_notice = NoticeRepository.update(
        db, notice, **notice_update.dict(exclude_unset=True)
    )
    return updated_notice

@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Delete notice (Authority only)"""
    notice = NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    NoticeRepository.delete(db, notice)
    return {"message": "Notice deleted successfully"}

@router.get("/all")
async def get_all_notices_admin(
    skip: int = 0,
    limit: int = 100,
    priority: str = None,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all notices including expired (Authority only)"""
    from models.models import Notice
    
    query = db.query(Notice)
    
    if priority:
        query = query.filter(Notice.priority == priority)
    
    notices = query.order_by(Notice.created_at.desc()).offset(skip).limit(limit).all()
    
    return notices

# PUBLIC/USER ENDPOINTS

@router.get("/", response_model=List[NoticeResponse])
async def get_notices(
    skip: int = 0,
    limit: int = 100,
    priority: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active notices for current user"""
    notices = NoticeRepository.get_all(
        db, 
        skip=skip, 
        limit=limit, 
        target_role=current_user.role.value,
        priority=priority
    )
    return notices

@router.get("/urgent", response_model=List[NoticeResponse])
async def get_urgent_notices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get urgent notices"""
    notices = NoticeRepository.get_urgent_notices(db, current_user.role.value)
    return notices

@router.get("/recent", response_model=List[NoticeResponse])
async def get_recent_notices(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent notices from last N days"""
    notices = NoticeRepository.get_recent_notices(db, days, current_user.role.value)
    return notices

@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific notice"""
    notice = NoticeRepository.get_by_id(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    # Check if user has access to this notice
    if notice.target_role != "all" and notice.target_role != current_user.role.value:
        raise HTTPException(status_code=403, detail="Not authorized to view this notice")
    
    return notice

@router.get("/search/{query}")
async def search_notices(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search notices"""
    notices = NoticeRepository.search_notices(db, query, current_user.role.value)
    return notices