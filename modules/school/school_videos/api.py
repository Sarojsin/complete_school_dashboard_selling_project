from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os
import shutil
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_teacher
from modules.shared.models import User
from modules.shared.config import settings

router = APIRouter(dependencies=[Depends(require_school_portal)])


# TEACHER ENDPOINTS

@router.post("/upload")
async def upload_video(
    title: str = Form(...),
    course_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Upload course video (Teacher only)"""
    from modules.school.school_teacher.repository import TeacherRepository
    from modules.school.school_videos.repository import VideosRepository
    
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
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get all videos uploaded by current teacher"""
    from modules.school.school_teacher.repository import TeacherRepository
    from modules.school.school_videos.repository import VideosRepository
    
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    videos = await VideosRepository.get_by_teacher(db, teacher.id)
    return videos


@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Delete a video (Teacher only)"""
    from modules.school.school_teacher.repository import TeacherRepository
    from modules.school.school_videos.repository import VideosRepository
    
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Note: comparison will work at runtime
    if video.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete file
    if os.path.exists(str(video.file_path)):
        os.remove(str(video.file_path))
    
    await VideosRepository.delete(db, video)
    return {"message": "Video deleted successfully"}


# STUDENT/PUBLIC ENDPOINTS

@router.get("/")
async def list_videos(
    course_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get videos with optional filters"""
    from modules.school.school_videos.repository import VideosRepository
    
    videos = await VideosRepository.get_all(db, course_id=course_id, skip=skip, limit=limit)
    return videos


@router.get("/{video_id}")
async def get_video(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get video details"""
    from modules.school.school_videos.repository import VideosRepository
    from modules.school.school_student.repository import StudentRepository
    
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(str(c.id) == str(video.course_id) for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return video


@router.get("/course/{course_id}")
async def get_course_videos(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all videos for a course"""
    from modules.school.school_videos.repository import VideosRepository
    from modules.school.school_student.repository import StudentRepository
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(str(c.id) == str(course_id) for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    videos = await VideosRepository.get_by_course(db, course_id)
    return videos


@router.get("/{video_id}/stream")
async def stream_video(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Stream video file"""
    from modules.school.school_videos.repository import VideosRepository
    from modules.school.school_student.repository import StudentRepository
    
    video = await VideosRepository.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # If student, verify enrollment
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            enrolled_courses = await StudentRepository.get_enrolled_courses(db, student.id)
            if not any(str(c.id) == str(video.course_id) for c in enrolled_courses):
                raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    file_path = str(video.file_path) if video.file_path else None
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=os.path.basename(file_path)
    )


@router.get("/search/{query}")
async def search_videos(
    query: str,
    course_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search videos"""
    from modules.school.school_videos.repository import VideosRepository
    from modules.school.school_student.repository import StudentRepository
    
    videos = await VideosRepository.search_videos(db, query, course_id)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            ec = await StudentRepository.get_enrolled_courses(db, student.id)
            enrolled_course_ids = [str(c.id) for c in ec]
            videos = [v for v in videos if str(v.course_id) in enrolled_course_ids]
    
    return videos


@router.get("/recent/all")
async def get_recent_videos(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recently uploaded videos"""
    from modules.school.school_videos.repository import VideosRepository
    from modules.school.school_student.repository import StudentRepository
    
    videos = await VideosRepository.get_recent_videos(db, limit=limit)
    
    # Filter by enrollment if student
    if current_user.role.value == "student":
        student = await StudentRepository.get_by_user_id(db, current_user.id)
        if student:
            ec = await StudentRepository.get_enrolled_courses(db, student.id)
            enrolled_course_ids = [str(c.id) for c in ec]
            videos = [v for v in videos if str(v.course_id) in enrolled_course_ids]
    
    return videos


__all__ = ["router"]