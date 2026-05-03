"""
Admin Content and Media Management API

API endpoints for managing uploaded notes and videos.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from typing import Optional
from datetime import datetime
from pathlib import Path

from backup.core.database import get_async_db
from backup.models.models import User, Note, Video, Teacher
from backup.api.deps.admin import get_current_admin

router = APIRouter(prefix="/admin/media", tags=["Admin Media"])


def _safe_size(file_path: Optional[str]) -> int:
    if not file_path:
        return 0
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[3] / path
    try:
        return path.stat().st_size
    except Exception:
        return 0


def _basename(file_path: Optional[str]) -> str:
    if not file_path:
        return ""
    return Path(file_path).name


async def _load_notes(
    db: AsyncSession,
    is_approved: Optional[bool] = None,
    uploaded_by: Optional[int] = None,
):
    query = select(Note).options(joinedload(Note.teacher), joinedload(Note.course)).order_by(desc(Note.uploaded_at))
    if is_approved is not None:
        query = query.where(Note.is_approved == is_approved)
    if uploaded_by is not None:
        query = query.where(Note.teacher_id == uploaded_by)
    result = await db.execute(query)
    return list(result.scalars().all())


async def _load_videos(
    db: AsyncSession,
    is_approved: Optional[bool] = None,
    uploaded_by: Optional[int] = None,
):
    query = select(Video).options(joinedload(Video.teacher), joinedload(Video.course)).order_by(desc(Video.uploaded_at))
    if is_approved is not None:
        query = query.where(Video.is_approved == is_approved)
    if uploaded_by is not None:
        query = query.where(Video.teacher_id == uploaded_by)
    result = await db.execute(query)
    return list(result.scalars().all())


def _serialize_note(note: Note) -> dict:
    size = note.file_size or _safe_size(note.file_path)
    return {
        "id": note.id,
        "filename": _basename(note.file_path),
        "file_type": "note",
        "file_size": size,
        "uploaded_by": note.teacher_id,
        "uploader_name": note.teacher.full_name if note.teacher else None,
        "is_approved": bool(note.is_approved),
        "created_at": note.uploaded_at.isoformat() if note.uploaded_at else None,
        "title": note.title,
        "course_id": note.course_id,
    }


def _serialize_video(video: Video) -> dict:
    size = video.file_size or _safe_size(video.file_path)
    return {
        "id": video.id,
        "filename": _basename(video.file_path),
        "file_type": "video",
        "file_size": size,
        "uploaded_by": video.teacher_id,
        "uploader_name": video.teacher.full_name if video.teacher else None,
        "is_approved": bool(video.is_approved),
        "created_at": video.uploaded_at.isoformat() if video.uploaded_at else None,
        "title": video.title,
        "course_id": video.course_id,
        "duration": video.duration,
    }


# ============ FILE MANAGEMENT ============

@router.get("/files")
async def get_all_media_files(
    file_type: Optional[str] = None,  # note, video
    is_approved: Optional[bool] = None,
    uploaded_by: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get all media files"""
    items = []
    if file_type in (None, "note"):
        notes = await _load_notes(db, is_approved=is_approved, uploaded_by=uploaded_by)
        items.extend([_serialize_note(n) for n in notes])
    if file_type in (None, "video"):
        videos = await _load_videos(db, is_approved=is_approved, uploaded_by=uploaded_by)
        items.extend([_serialize_video(v) for v in videos])

    items.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    total = len(items)
    items = items[skip : skip + limit]
    return {"files": items, "total": total}


@router.post("/{file_id}/approve")
async def approve_media_file(
    file_id: int,
    file_type: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Approve a media file for publishing"""
    if file_type == "note":
        result = await db.execute(select(Note).where(Note.id == file_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Note not found")
        item.is_approved = True
    elif file_type == "video":
        result = await db.execute(select(Video).where(Video.id == file_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Video not found")
        item.is_approved = True
    else:
        raise HTTPException(status_code=400, detail="Invalid file_type")

    await db.commit()
    return {"success": True, "message": "File approved"}


@router.delete("/{file_id}")
async def delete_media_file(
    file_id: int,
    file_type: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Delete a media file"""
    if file_type == "note":
        result = await db.execute(select(Note).where(Note.id == file_id))
        item = result.scalar_one_or_none()
    elif file_type == "video":
        result = await db.execute(select(Video).where(Video.id == file_id))
        item = result.scalar_one_or_none()
    else:
        raise HTTPException(status_code=400, detail="Invalid file_type")

    if not item:
        raise HTTPException(status_code=404, detail="Media file not found")

    file_path = getattr(item, "file_path", None)
    await db.delete(item)
    await db.commit()

    if file_path:
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path(__file__).resolve().parents[3] / path
            if path.exists():
                path.unlink()
        except Exception:
            pass

    return {"success": True, "message": "File deleted"}


# ============ STORAGE MANAGEMENT ============

@router.get("/storage/usage")
async def get_storage_usage(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get storage usage statistics"""
    notes = await _load_notes(db)
    videos = await _load_videos(db)

    note_bytes = sum((n.file_size or _safe_size(n.file_path)) for n in notes)
    video_bytes = sum((v.file_size or _safe_size(v.file_path)) for v in videos)
    total = note_bytes + video_bytes
    total_mb = round(total / (1024 * 1024), 2)
    used_mb = total_mb

    return {
        "total_storage_mb": None,
        "used_storage_mb": used_mb,
        "available_storage_mb": None,
        "usage_percentage": None,
        "by_type": {
            "videos": round(video_bytes / (1024 * 1024), 2),
            "notes": round(note_bytes / (1024 * 1024), 2),
        },
    }


@router.get("/storage/by-user")
async def get_storage_by_user(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get storage usage by user"""
    notes = await _load_notes(db)
    videos = await _load_videos(db)

    usage = {}
    for n in notes:
        size = n.file_size or _safe_size(n.file_path)
        usage.setdefault(n.teacher_id, 0)
        usage[n.teacher_id] += size
    for v in videos:
        size = v.file_size or _safe_size(v.file_path)
        usage.setdefault(v.teacher_id, 0)
        usage[v.teacher_id] += size

    users = []
    for teacher_id, size in usage.items():
        users.append({
            "user_id": teacher_id,
            "storage_used_mb": round(size / (1024 * 1024), 2),
        })
    return {"users": users}


# ============ VIDEO MANAGEMENT ============

@router.get("/videos")
async def get_all_videos(
    is_approved: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get all videos"""
    videos = await _load_videos(db, is_approved=is_approved)
    total = len(videos)
    items = [_serialize_video(v) for v in videos][skip : skip + limit]
    return {"videos": items, "total": total}


# ============ NOTES MANAGEMENT ============

@router.get("/notes")
async def get_all_notes(
    is_approved: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get all notes"""
    notes = await _load_notes(db, is_approved=is_approved)
    total = len(notes)
    items = [_serialize_note(n) for n in notes][skip : skip + limit]
    return {"notes": items, "total": total}
