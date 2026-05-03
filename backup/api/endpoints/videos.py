from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
import shutil
from backup.core.database import get_async_db
from backup.dependencies.auth import get_current_teacher, get_current_user
from backup.models.models import User
from backup.repositories.videos_repository import VideosRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.student_repository import StudentRepository
from backup.schemas.misc import VideoResponse
from backup.core.config import settings

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    title: str = Form(...),
    course_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Upload course video (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Validate file type (videos only)
    file_ext = os.path.splitext(file.filename)[1].lower().replace('.', '')
    allowed_video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']
    
    if file_ext not in allowed_video_extensions:
        raise HTTPException(status_code=400, detail="Only video files are allowed")
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_FILE_SIZE * 10:  # 100MB for videos
        raise HTTPException(status_code=400, detail="File too large (max 100MB)")
    
    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/videos"
    os.makedirs(upload_dir, exist_ok=True)
    
    safe_filename = f"{course_id}_{file.filename}"
    file_path = f"{upload_dir}/{safe_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create video record
    video_data = {
        "title": title,
        "description": description,
        "course_id": course_id,
        "teacher_id": teacher.id,
        "file_path": file_path,
        "file_size": file_size
    }
    
    video = await VideosRepository.create(db, video_data)
    
    return video

@router.get("/teacher/my-videos")
async def get_my_videos(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all videos uploaded by current teacher"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    videos = await VideosRepository.get_by_teacher(db, teacher.id)
    return videos

@router.get("/{video_id}")
async def get_video(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get video details"""
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == video.course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return video

@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a video (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete file
    if os.path.exists(video.file_path):
        os.remove(video.file_path)
    
    await VideosRepository.delete(db, video)
    return {"message": "Video deleted successfully"}

# STUDENT/PUBLIC ENDPOINTS

@router.get("/course/{course_id}")
async def get_course_videos(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all videos for a course"""
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    videos = await VideosRepository.get_by_course(db, course_id)
    return videos

@router.get("/{video_id}/stream")
async def stream_video(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Stream video file"""
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(c.id == video.course_id for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        video.file_path,
        media_type="video/mp4",
        filename=os.path.basename(video.file_path)
    )

@router.get("/search/{query}")
async def search_videos(
    query: str,
    course_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Search videos"""
    videos = await VideosRepository.search_videos(db, query, course_id)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            ec = await StudentRepository.get_enrolled_courses(db, student.id)
            enrolled_course_ids = [c.id for c in ec]
            videos = [v for v in videos if v.course_id in enrolled_course_ids]
    
    return videos

@router.get("/recent/all")
async def get_recent_videos(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get recently uploaded videos"""
    videos = await VideosRepository.get_recent_videos(db, limit=limit)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            ec = await StudentRepository.get_enrolled_courses(db, student.id)
            enrolled_course_ids = [c.id for c in ec]
            videos = [v for v in videos if v.course_id in enrolled_course_ids]
    
    return videos