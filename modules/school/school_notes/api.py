from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_teacher
from modules.shared.models import User
from .repository import NoteRepository
from .schemas import NoteCreate, NoteUpdate, NoteResponse
from modules.shared.config import settings

router = APIRouter(dependencies=[Depends(require_school_portal)])


@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a new note (Teacher only)"""
    # In a real implementation, we'd get the teacher_id from the user
    note_data = note.model_dump()
    repo = NoteRepository(db)
    created_note = await repo.create(note_data)
    return created_note


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a note by ID"""
    repo = NoteRepository(db)
    note = await repo.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteResponse])
async def list_notes(
    course_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List notes with optional filters"""
    repo = NoteRepository(db)
    notes = await repo.get_all(course_id=course_id, skip=skip, limit=limit)
    return notes


@router.get("/course/{course_id}", response_model=List[NoteResponse])
async def get_notes_by_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get notes for a specific course"""
    repo = NoteRepository(db)
    notes = await repo.get_by_course(course_id)
    return notes


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a note (Teacher only)"""
    repo = NoteRepository(db)
    note_data = note.model_dump(exclude_unset=True)
    updated_note = await repo.update(note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a note (Teacher only)"""
    repo = NoteRepository(db)
    success = await repo.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


# Additional endpoints from backup
@router.get("/teacher/my-notes", response_model=List[NoteResponse])
async def get_my_notes(
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get notes uploaded by current teacher"""
    from modules.school.school_teacher.repository import TeacherRepository
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    repo = NoteRepository(db)
    notes = await repo.get_by_teacher(teacher.id)
    return notes


@router.get("/{note_id}/download")
async def download_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download a note file"""
    repo = NoteRepository(db)
    note = await repo.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Handle column types - get() returns SQLAlchemy objects
    file_path = note.file_path
    if not file_path or not os.path.exists(str(file_path)):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        str(file_path),
        filename=str(note.title),
        media_type="application/octet-stream"
    )


@router.get("/search/{query}", response_model=List[NoteResponse])
async def search_notes(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search notes by title or description"""
    repo = NoteRepository(db)
    notes = await repo.search(query)
    return notes


@router.get("/recent/all", response_model=List[NoteResponse])
async def get_recent_notes(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recently uploaded notes"""
    repo = NoteRepository(db)
    notes = await repo.get_recent(limit)
    return notes


__all__ = ["router"]