from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database.database import get_db
from dependencies import get_current_teacher, get_current_student, get_current_user
from models.models import User
from repositories.attendance_repository import AttendanceRepository
from repositories.teacher_repository import TeacherRepository
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from tables.tables import AttendanceCreate, AttendanceResponse

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/", response_model=AttendanceResponse)
async def mark_attendance(
    attendance: AttendanceCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Mark attendance for a student (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, attendance.course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    # Check if attendance already exists
    existing = AttendanceRepository.get_by_date(
        db, attendance.student_id, attendance.course_id, attendance.date
    )
    
    if existing:
        # Update existing attendance
        updated = AttendanceRepository.update(
            db, existing,
            status=attendance.status,
            remarks=attendance.remarks
        )
        return updated
    
    # Create new attendance record
    created = AttendanceRepository.create(db, attendance.dict())
    return created

@router.post("/bulk")
async def mark_bulk_attendance(
    attendance_list: List[AttendanceCreate],
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Mark attendance for multiple students at once (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    if not attendance_list:
        raise HTTPException(status_code=400, detail="No attendance records provided")
    
    # Verify teacher teaches this course
    course_id = attendance_list[0].course_id
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    created_records = []
    for attendance in attendance_list:
        # Check if exists
        existing = AttendanceRepository.get_by_date(
            db, attendance.student_id, attendance.course_id, attendance.date
        )
        
        if existing:
            updated = AttendanceRepository.update(
                db, existing,
                status=attendance.status,
                remarks=attendance.remarks
            )
            created_records.append(updated)
        else:
            created = AttendanceRepository.create(db, attendance.dict())
            created_records.append(created)
    
    return {
        "message": f"Attendance marked for {len(created_records)} students",
        "records": created_records
    }

@router.get("/course/{course_id}")
async def get_course_attendance(
    course_id: int,
    date_value: date = None,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get attendance records for a course (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    attendance_records = AttendanceRepository.get_course_attendance(db, course_id, date_value)
    
    # Get enrolled students
    enrolled_students = CourseRepository.get_enrolled_students(db, course_id)
    
    if date_value:
        # Check which students are missing attendance for this date
        recorded_student_ids = [a.student_id for a in attendance_records]
        missing_students = [s for s in enrolled_students if s.id not in recorded_student_ids]
        
        return {
            "course": course,
            "date": date_value,
            "attendance": attendance_records,
            "missing_students": missing_students,
            "total_enrolled": len(enrolled_students),
            "total_recorded": len(attendance_records)
        }
    
    return {
        "course": course,
        "attendance": attendance_records,
        "total_enrolled": len(enrolled_students)
    }

@router.get("/course/{course_id}/stats")
async def get_course_attendance_stats(
    course_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get attendance statistics for a course (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher teaches this course
    course = CourseRepository.get_by_id(db, course_id)
    if not course or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized for this course")
    
    # Get low attendance students
    low_attendance = AttendanceRepository.get_low_attendance_students(db, course_id, 75.0)
    
    return {
        "course": course,
        "low_attendance_students": low_attendance
    }

# STUDENT ENDPOINTS

@router.get("/my-attendance")
async def get_my_attendance(
    course_id: int = None,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student's attendance records"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    attendance = AttendanceRepository.get_student_attendance(db, student.id, course_id)
    stats = AttendanceRepository.get_attendance_stats(db, student.id, course_id)
    
    return {
        "attendance": attendance,
        "statistics": stats
    }

@router.get("/my-attendance/course/{course_id}")
async def get_my_course_attendance(
    course_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student's attendance for a specific course"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Check if student is enrolled in the course
    enrolled_courses = StudentRepository.get_enrolled_courses(db, student.id)
    if not any(c.id == course_id for c in enrolled_courses):
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    attendance = AttendanceRepository.get_student_attendance(db, student.id, course_id)
    stats = AttendanceRepository.get_attendance_stats(db, student.id, course_id)
    
    return {
        "course_id": course_id,
        "attendance": attendance,
        "statistics": stats
    }