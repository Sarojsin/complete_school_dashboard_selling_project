from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from database.database import get_db
from dependencies import get_current_teacher, get_current_user
from models.models import User
from repositories.notes_repository import NotesRepository
from repositories.teacher_repository import TeacherRepository
from repositories.student_repository import StudentRepository
from tables.tables import NoteResponse
from config.config import settings

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/upload", response_model=NoteResponse)
async def upload_note(
    title: str = Form(...),
    course_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Upload course notes (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Validate file
    file_ext = os.path.splitext(file.filename)[1].lower().replace('.', '')
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/notes"
    os.makedirs(upload_dir, exist_ok=True)
    
    safe_filename = f"{course_id}_{file.filename}"
    file_path = f"{upload_dir}/{safe_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create note record
    note_data = {
        "title": title,
        "description": description,
        "course_id": course_id,
        "teacher_id": teacher.id,
        "file_path": file_path,
        "file_size": file_size,
        "file_type": file_ext
    }
    
    note = NotesRepository.create(db, note_data)
    
    return note

@router.get("/teacher/my-notes")
async def get_my_notes(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all notes uploaded by current teacher"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    notes = NotesRepository.get_by_teacher(db, teacher.id)
    return notes

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete a note (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    note = NotesRepository.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete file
    if os.path.exists(note.file_path):
        os.remove(note.file_path)
    
    NotesRepository.delete(db, note)
    return {"message": "Note deleted successfully"}

# STUDENT/PUBLIC ENDPOINTS

@router.get("/course/{course_id}")
async def get_course_notes(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all notes for a course"""
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    notes = NotesRepository.get_by_course(db, course_id)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get note details"""
    note = NotesRepository.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == note.course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return note

@router.get("/{note_id}/download")
async def download_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download note file"""
    note = NotesRepository.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == note.course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    if not os.path.exists(note.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        note.file_path,
        media_type="application/octet-stream",
        filename=os.path.basename(note.file_path)
    )

@router.get("/search/{query}")
async def search_notes(
    query: str,
    course_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search notes"""
    notes = NotesRepository.search_notes(db, query, course_id)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_course_ids = [c.id for c in StudentRepository.get_enrolled_courses(db, student.id)]
            notes = [n for n in notes if n.course_id in enrolled_course_ids]
    
    return notes

@router.get("/recent/all")
async def get_recent_notes(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recently uploaded notes"""
    notes = NotesRepository.get_recent_notes(db, limit=limit)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_course_ids = [c.id for c in StudentRepository.get_enrolled_courses(db, student.id)]
            notes = [n for n in notes if n.course_id in enrolled_course_ids]
    
    return notes