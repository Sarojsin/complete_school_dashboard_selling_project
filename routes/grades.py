from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from dependencies import get_current_teacher, get_current_student
from models.models import User
from repositories.grade_repository import GradeRepository
from repositories.teacher_repository import TeacherRepository
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from tables.tables import GradeCreate, GradeUpdate, GradeResponse

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/", response_model=GradeResponse)
async def add_grade(
    grade: GradeCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Add grade for a student (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    # Verify student is enrolled in course
    enrolled_students = CourseRepository.get_enrolled_students(db, grade.course_id)
    if not any(s.id == grade.student_id for s in enrolled_students):
        raise HTTPException(status_code=400, detail="Student not enrolled in this course")
    
    created_grade = GradeRepository.create(db, grade.dict())
    return created_grade

@router.post("/bulk")
async def add_bulk_grades(
    grades: List[GradeCreate],
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Add multiple grades at once (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    if not grades:
        raise HTTPException(status_code=400, detail="No grades provided")
    
    # Verify teacher teaches this course
    course_id = grades[0].course_id
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    created_grades = GradeRepository.create_bulk(db, [g.dict() for g in grades])
    
    return {
        "message": f"Added {len(created_grades)} grades",
        "grades": created_grades
    }

@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_update: GradeUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update a grade (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    grade = GradeRepository.get_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_grade = GradeRepository.update(db, grade, **grade_update.dict(exclude_unset=True))
    return updated_grade

@router.delete("/{grade_id}")
async def delete_grade(
    grade_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete a grade (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    grade = GradeRepository.get_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, grade.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    GradeRepository.delete(db, grade)
    return {"message": "Grade deleted successfully"}

@router.get("/course/{course_id}")
async def get_course_grades(
    course_id: int,
    grade_type: str = None,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all grades for a course (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    grades = GradeRepository.get_course_grades(db, course_id, grade_type)
    stats = GradeRepository.get_class_statistics(db, course_id, grade_type)
    distribution = GradeRepository.get_grade_distribution(db, course_id)
    
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
    db: Session = Depends(get_db)
):
    """Get top performing students (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    top_performers = GradeRepository.get_top_performers(db, course_id, limit)
    
    return {
        "course": course,
        "top_performers": top_performers
    }

# STUDENT ENDPOINTS

@router.get("/my-grades")
async def get_my_grades(
    course_id: int = None,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student's grades"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    grades = GradeRepository.get_student_grades(db, student.id, course_id)
    stats = GradeRepository.get_grade_statistics(db, student.id, course_id)
    gpa = GradeRepository.get_gpa(db, student.id)
    
    return {
        "grades": grades,
        "statistics": stats,
        "gpa": gpa
    }