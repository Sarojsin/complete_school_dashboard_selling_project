from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backup.core.database import get_async_db
from backup.dependencies.auth import get_current_teacher, get_current_student
from backup.models.models import User
from backup.repositories.grade_repository import GradeRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.student_repository import StudentRepository
from backup.repositories.course_repository import CourseRepository
from backup.schemas.misc import GradeCreate, GradeUpdate, GradeResponse

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/", response_model=GradeResponse)
async def add_grade(
    grade: GradeCreate,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Add grade for a student (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = await CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    # Verify student is enrolled in course
    enrolled_students = await CourseRepository.get_enrolled_students(db, grade.course_id)
    if not any(s.id == grade.student_id for s in enrolled_students):
        raise HTTPException(status_code=400, detail="Student not enrolled in this course")
    
    created_grade = await GradeRepository.create(db, grade.dict())
    return created_grade

@router.post("/bulk")
async def add_bulk_grades(
    grades: List[GradeCreate],
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Add multiple grades at once (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    if not grades:
        raise HTTPException(status_code=400, detail="No grades provided")
    
    # Verify teacher teaches this course
    course_id = grades[0].course_id
    course = await CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    created_grades = await GradeRepository.create_bulk(db, [g.dict() for g in grades])
    
    return {
        "message": f"Added {len(created_grades)} grades",
        "grades": created_grades
    }

@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_update: GradeUpdate,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Update a grade (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    grade = await GradeRepository.get_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Verify teacher teaches this course
    course = await CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_grade = await GradeRepository.update(db, grade, **grade_update.dict(exclude_unset=True))
    return updated_grade

@router.delete("/{grade_id}")
async def delete_grade(
    grade_id: int,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a grade (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    grade = await GradeRepository.get_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Verify teacher teaches this course
    course = await CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await GradeRepository.delete(db, grade)
    return {"message": "Grade deleted successfully"}

@router.get("/course/{course_id}")
async def get_course_grades(
    course_id: int,
    grade_type: str = None,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all grades for a course (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = await CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    grades = await GradeRepository.get_course_grades(db, course_id, grade_type)
    stats = await GradeRepository.get_class_statistics(db, course_id, grade_type)
    distribution = await GradeRepository.get_grade_distribution(db, course_id)
    
    return {
        "course": course,
        "grades": grades,
        "statistics": stats,
        "distribution": distribution
    }

@router.get("/course/{course_id}/top-performers")
async def get_top_performers(
    course_id: int,
    limit: int = 10,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get top performing students (Teacher only)"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = await CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    top_performers = await GradeRepository.get_top_performers(db, course_id, limit)
    
    return {
        "course": course,
        "top_performers": top_performers
    }

# STUDENT ENDPOINTS

@router.get("/my-grades")
async def get_my_grades(
    course_id: int = None,
    current_user: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's grades"""
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    grades = await GradeRepository.get_student_grades(db, student.id, course_id)
    stats = await GradeRepository.get_grade_statistics(db, student.id, course_id)
    gpa = await GradeRepository.get_gpa(db, student.id)
    
    return {
        "grades": grades,
        "statistics": stats,
        "gpa": gpa
    }