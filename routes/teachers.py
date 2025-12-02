from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from dependencies import get_current_teacher
from models.models import User
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.student_repository import StudentRepository
from tables.tables import TeacherResponse, TeacherUpdate

router = APIRouter()

@router.get("/me", response_model=TeacherResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get current teacher's profile"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return teacher

@router.put("/me", response_model=TeacherResponse)
async def update_my_profile(
    teacher_update: TeacherUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update current teacher's profile"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    updated_teacher = TeacherRepository.update(
        db, teacher, **teacher_update.dict(exclude_unset=True)
    )
    return updated_teacher

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get teacher dashboard data"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teaching courses
    courses = TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Get total students across all courses
    total_students = 0
    for course in courses:
        total_students += CourseRepository.get_enrollment_count(db, course.id)
    
    # Get pending assignments to grade
    from models.models import AssignmentSubmission
    pending_grading = db.query(AssignmentSubmission).join(
        AssignmentSubmission.assignment
    ).filter(
        AssignmentSubmission.assignment.has(teacher_id=teacher.id),
        AssignmentSubmission.score.is_(None)
    ).count()
    
    # Get upcoming tests
    from models.test_models import Test
    from datetime import datetime
    upcoming_tests = db.query(Test).filter(
        Test.teacher_id == teacher.id,
        Test.start_time >= datetime.utcnow(),
        Test.is_active == True
    ).order_by(Test.start_time).limit(5).all()
    
    # Get recent activity
    from models.models import Assignment
    recent_assignments = db.query(Assignment).filter(
        Assignment.teacher_id == teacher.id
    ).order_by(Assignment.created_at.desc()).limit(5).all()
    
    return {
        "teacher": teacher,
        "courses": courses,
        "total_students": total_students,
        "pending_grading": pending_grading,
        "upcoming_tests": upcoming_tests,
        "recent_assignments": recent_assignments
    }

@router.get("/courses")
async def get_my_courses(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get teacher's courses"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    courses = TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Add enrollment count for each course
    courses_with_stats = []
    for course in courses:
        enrollment_count = CourseRepository.get_enrollment_count(db, course.id)
        courses_with_stats.append({
            "course": course,
            "enrollment_count": enrollment_count
        })
    
    return courses_with_stats

@router.get("/students")
async def get_my_students(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all students enrolled in teacher's courses"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    courses = TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Get unique students across all courses
    all_students = set()
    students_by_course = {}
    
    for course in courses:
        students = CourseRepository.get_enrolled_students(db, course.id)
        students_by_course[course.id] = students
        all_students.update(students)
    
    return {
        "total_students": len(all_students),
        "students": list(all_students),
        "students_by_course": students_by_course
    }

@router.get("/students/{student_id}")
async def get_student_detail(
    student_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific student"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    student = StudentRepository.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if teacher teaches this student
    courses = TeacherRepository.get_teaching_courses(db, teacher.id)
    student_courses = StudentRepository.get_enrolled_courses(db, student.id)
    
    common_courses = [c for c in student_courses if c in courses]
    
    if not common_courses:
        raise HTTPException(
            status_code=403, 
            detail="You don't teach this student in any course"
        )
    
    # Get student performance data
    from models.models import Grade, Attendance, AssignmentSubmission
    
    grades = db.query(Grade).filter(
        Grade.student_id == student.id,
        Grade.course_id.in_([c.id for c in common_courses])
    ).all()
    
    attendance = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.course_id.in_([c.id for c in common_courses])
    ).all()
    
    submissions = db.query(AssignmentSubmission).join(
        AssignmentSubmission.assignment
    ).filter(
        AssignmentSubmission.student_id == student.id,
        AssignmentSubmission.assignment.has(teacher_id=teacher.id)
    ).all()
    
    # Calculate statistics
    from sqlalchemy import func
    attendance_stats = db.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.student_id == student.id,
        Attendance.course_id.in_([c.id for c in common_courses])
    ).group_by(Attendance.status).all()
    
    return {
        "student": student,
        "courses": common_courses,
        "grades": grades,
        "attendance": attendance,
        "attendance_stats": {status: count for status, count in attendance_stats},
        "submissions": submissions
    }
@router.get("/assignments")
async def get_my_assignments(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get assignments created by teacher"""
    from models.models import Assignment
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignments = db.query(Assignment).filter(
        Assignment.teacher_id == teacher.id
    ).order_by(Assignment.due_date.desc()).all()
    
    return assignments

@router.get("/attendance")
async def get_my_attendance(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get attendance records for teacher's courses"""
    from models.models import Attendance, Course
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()
    course_ids = [c.id for c in courses]
    
    attendance = db.query(Attendance).filter(
        Attendance.course_id.in_(course_ids)
    ).order_by(Attendance.date.desc()).all()
    
    return attendance

@router.get("/grades")
async def get_my_grades(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get grades for teacher's courses"""
    from models.models import Grade, Course
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()
    course_ids = [c.id for c in courses]
    
    grades = db.query(Grade).filter(
        Grade.course_id.in_(course_ids)
    ).order_by(Grade.date.desc()).all()
    
    return grades

@router.get("/tests")
async def get_my_tests(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get tests created by teacher"""
    from models.models import Test
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    tests = db.query(Test).filter(
        Test.teacher_id == teacher.id
    ).order_by(Test.created_at.desc()).all()
    
    return tests

@router.get("/timetable")
async def get_my_timetable(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get teacher's class schedule"""
    from models.models import Schedule, Course
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()
    course_ids = [c.id for c in courses]
    
    schedules = db.query(Schedule).filter(
        Schedule.course_id.in_(course_ids)
    ).order_by(Schedule.day_of_week, Schedule.start_time).all()
    
    return schedules
