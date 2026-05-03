## backup/api/endpoints/teachers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from backup.core.database import get_async_db
from backup.dependencies.auth import get_current_teacher
from backup.models.models import User, Teacher, Course, AssignmentSubmission, Assignment, Grade, Attendance, Schedule
from backup.models.test_models import Test
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.course_repository import CourseRepository
from backup.repositories.student_repository import StudentRepository
from backup.schemas.misc import TeacherResponse, TeacherUpdate
from datetime import datetime

router = APIRouter()

@router.get("/me", response_model=TeacherResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current teacher's profile"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return teacher

@router.put("/me", response_model=TeacherResponse)
async def update_my_profile(
    teacher_update: TeacherUpdate,
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Update current teacher's profile"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    updated_teacher = await TeacherRepository.update(
        db, teacher, **teacher_update.dict(exclude_unset=True)
    )
    return updated_teacher

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get teacher dashboard data"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teaching courses
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Get total students across all courses
    total_students = 0
    for course in courses:
        total_students += await CourseRepository.get_enrollment_count(db, course.id)
    
    # Get pending assignments to grade
    res_p = await db.execute(select(func.count(AssignmentSubmission.id)).join(
        AssignmentSubmission.assignment
    ).filter(
        Assignment.teacher_id == teacher.id,
        AssignmentSubmission.score.is_(None)
    ))
    pending_grading = res_p.scalar() or 0
    
    # Get upcoming tests
    res_t = await db.execute(select(Test).filter(
        Test.teacher_id == teacher.id,
        Test.start_time >= datetime.utcnow(),
        Test.is_active == True
    ).order_by(Test.start_time).limit(5))
    upcoming_tests = res_t.scalars().all()
    
    # Get recent activity
    res_a = await db.execute(select(Assignment).filter(
        Assignment.teacher_id == teacher.id
    ).order_by(Assignment.created_at.desc()).limit(5))
    recent_assignments = res_a.scalars().all()
    
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
    db: AsyncSession = Depends(get_async_db)
):
    """Get teacher's courses"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Add enrollment count for each course
    courses_with_stats = []
    for course in courses:
        enrollment_count = await CourseRepository.get_enrollment_count(db, course.id)
        courses_with_stats.append({
            "course": course,
            "enrollment_count": enrollment_count
        })
    
    return courses_with_stats

@router.get("/students")
async def get_my_students(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all students enrolled in teacher's courses"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    
    # Get unique students across all courses
    all_students = set()
    students_by_course = {}
    
    for course in courses:
        students = await CourseRepository.get_enrolled_students(db, course.id)
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
    db: AsyncSession = Depends(get_async_db)
):
    """Get detailed information about a specific student"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    student = await StudentRepository.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if teacher teaches this student
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    student_courses = await StudentRepository.get_enrolled_courses(db, student.id)
    
    teacher_course_ids = {c.id for c in courses}
    common_courses = [c for c in student_courses if c.id in teacher_course_ids]
    
    if not common_courses:
        raise HTTPException(
            status_code=403, 
            detail="You don't teach this student in any course"
        )
    
    common_course_ids = [c.id for c in common_courses]
    
    # Get student performance data
    res_g = await db.execute(select(Grade).filter(
        Grade.student_id == student.id,
        Grade.course_id.in_(common_course_ids)
    ))
    grades = res_g.scalars().all()
    
    res_att = await db.execute(select(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.course_id.in_(common_course_ids)
    ))
    attendance = res_att.scalars().all()
    
    res_s = await db.execute(select(AssignmentSubmission).join(
        AssignmentSubmission.assignment
    ).filter(
        AssignmentSubmission.student_id == student.id,
        Assignment.teacher_id == teacher.id
    ))
    submissions = res_s.scalars().all()
    
    # Calculate statistics
    res_stats = await db.execute(select(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.student_id == student.id,
        Attendance.course_id.in_(common_course_ids)
    ).group_by(Attendance.status))
    attendance_stats = res_stats.all()
    
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
    db: AsyncSession = Depends(get_async_db)
):
    """Get assignments created by teacher"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    res_a = await db.execute(select(Assignment).filter(
        Assignment.teacher_id == teacher.id
    ).order_by(Assignment.due_date.desc()))
    assignments = res_a.scalars().all()
    
    return assignments

@router.get("/attendance")
async def get_my_attendance(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get attendance records for teacher's courses"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    course_ids = [c.id for c in courses]
    
    res_att = await db.execute(select(Attendance).filter(
        Attendance.course_id.in_(course_ids)
    ).order_by(Attendance.date.desc()))
    attendance = res_att.scalars().all()
    
    return attendance

@router.get("/grades")
async def get_my_grades(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get grades for teacher's courses"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    course_ids = [c.id for c in courses]
    
    res_g = await db.execute(select(Grade).filter(
        Grade.course_id.in_(course_ids)
    ).order_by(Grade.date.desc()))
    grades = res_g.scalars().all()
    
    return grades

@router.get("/tests")
async def get_my_tests(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get tests created by teacher"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    res_t = await db.execute(select(Test).filter(
        Test.teacher_id == teacher.id
    ).order_by(Test.created_at.desc()))
    tests = res_t.scalars().all()
    
    return tests

@router.get("/timetable")
async def get_my_timetable(
    current_user: User = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_async_db)
):
    """Get teacher's class schedule"""
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get teacher's courses
    courses = await TeacherRepository.get_teaching_courses(db, teacher.id)
    course_ids = [c.id for c in courses]
    
    res_s = await db.execute(select(Schedule).filter(
        Schedule.course_id.in_(course_ids)
    ).order_by(Schedule.day_of_week, Schedule.start_time))
    schedules = res_s.scalars().all()
    
    return schedules
