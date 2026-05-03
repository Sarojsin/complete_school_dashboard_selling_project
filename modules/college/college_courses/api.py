"""
College Course API Endpoints
============================

Course endpoints for college mode (with credits).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from modules.shared.database import get_db as get_async_db
from modules.shared.models import User
from modules.college.college_courses.models import CollegeCourse, Department, Semester
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/courses", tags=["College Courses"], dependencies=[Depends(require_college_portal)])


@router.get("")
async def get_courses(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    is_elective: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get all courses in the college"""
    query = select(CollegeCourse)
    
    if department_id:
        query = query.where(CollegeCourse.department_id == department_id)
    if semester_id:
        query = query.where(CollegeCourse.semester_id == semester_id)
    if is_elective is not None:
        query = query.where(CollegeCourse.is_elective == is_elective)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    courses = result.scalars().all()
    
    return {
        "courses": [
            {
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "credits": course.credits,
                "department_id": course.department_id,
                "semester_id": course.semester_id,
                "instructor_id": course.instructor_id,
                "is_elective": course.is_elective
            }
            for course in courses
        ]
    }


@router.get("/{course_id}")
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get course by ID"""
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.id == course_id)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "description": course.description,
        "credits": course.credits,
        "department_id": course.department_id,
        "semester_id": course.semester_id,
        "instructor_id": course.instructor_id,
        "is_elective": course.is_elective
    }


@router.post("")
async def create_course(
    code: str,
    name: str,
    credits: int,
    department_id: int,
    semester_id: int,
    description: Optional[str] = None,
    instructor_id: Optional[int] = None,
    is_elective: bool = False,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new course"""
    # Check if code already exists
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.code == code)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    # Verify department exists
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Department not found")
    
    course = CollegeCourse(
        code=code,
        name=name,
        description=description,
        credits=credits,
        department_id=department_id,
        semester_id=semester_id,
        instructor_id=instructor_id,
        is_elective=is_elective
    )
    
    db.add(course)
    await db.commit()
    await db.refresh(course)
    
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "credits": course.credits,
        "message": "Course created successfully"
    }


@router.patch("/{course_id}")
async def update_course(
    course_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    credits: Optional[int] = None,
    instructor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update a course"""
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.id == course_id)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if name:
        course.name = name
    if description:
        course.description = description
    if credits:
        course.credits = credits
    if instructor_id is not None:
        course.instructor_id = instructor_id
    
    await db.commit()
    await db.refresh(course)
    
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "message": "Course updated successfully"
    }


@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a course"""
    result = await db.execute(
        select(CollegeCourse).where(CollegeCourse.id == course_id)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await db.delete(course)
    await db.commit()
    
    return {"message": "Course deleted successfully"}
