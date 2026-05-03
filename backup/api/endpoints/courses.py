from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backup.core.database import get_async_db
from backup.dependencies.auth import get_current_user, get_current_authority
from backup.models.models import User
from backup.repositories.course_repository import CourseRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.schemas.misc import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def get_all_courses(
    skip: int = 0,
    limit: int = 100,
    grade_level: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get all courses"""
    courses = await CourseRepository.get_all(db, skip=skip, limit=limit, grade_level=grade_level)
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get course by ID"""
    course = await CourseRepository.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Create new course (Authority only)"""
    # Check if course code already exists
    existing = await CourseRepository.get_by_code(db, course.course_code)
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    # Verify teacher exists if provided
    if course.teacher_id:
        teacher = await TeacherRepository.get_by_id(db, course.teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
    
    created_course = await CourseRepository.create(db, course.dict())
    return created_course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Update course (Authority only)"""
    course = await CourseRepository.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verify teacher exists if updating teacher_id
    if course_update.teacher_id:
        teacher = await TeacherRepository.get_by_id(db, course_update.teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
    
    updated_course = await CourseRepository.update(db, course, **course_update.dict(exclude_unset=True))
    return updated_course

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_authority)
):
    """Delete course (Authority only)"""
    course = await CourseRepository.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await CourseRepository.delete(db, course)
    return {"message": "Course deleted successfully"}

@router.get("/{course_id}/students")
async def get_course_students(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get all students enrolled in a course"""
    course = await CourseRepository.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    students = await CourseRepository.get_enrolled_students(db, course_id)
    enrollment_count = await CourseRepository.get_enrollment_count(db, course_id)
    
    return {
        "course": course,
        "students": students,
        "enrollment_count": enrollment_count
    }

@router.get("/search/{query}")
async def search_courses(
    query: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Search courses"""
    courses = await CourseRepository.search(db, query)
    return courses