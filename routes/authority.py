from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from database.database import get_db
from dependencies import get_current_authority
from models.models import User, Student, Teacher, Course, Assignment, Attendance, Grade, FeeRecord, UserRole
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from tables.tables import (
    StudentCreate, StudentResponse, StudentUpdate,
    TeacherCreate, TeacherResponse, TeacherUpdate
)

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get authority dashboard with system statistics"""
    
    # Count statistics
    total_students = db.query(func.count(Student.id)).scalar()
    total_teachers = db.query(func.count(Teacher.id)).scalar()
    total_courses = db.query(func.count(Course.id)).scalar()
    
    # Active students (enrolled this year)
    current_year = datetime.utcnow().year
    active_students = db.query(func.count(Student.id)).filter(
        func.extract('year', Student.enrollment_date) == current_year
    ).scalar()
    
    # Recent assignments
    recent_assignments = db.query(Assignment).order_by(
        Assignment.created_at.desc()
    ).limit(10).all()
    
    # Fee statistics
    total_fees = db.query(func.sum(FeeRecord.amount)).scalar() or 0
    collected_fees = db.query(func.sum(FeeRecord.paid_amount)).scalar() or 0
    pending_fees = total_fees - collected_fees
    
    # Attendance statistics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    attendance_stats = db.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.date >= thirty_days_ago.date()
    ).group_by(Attendance.status).all()
    
    # Grade statistics
    avg_score = db.query(
        func.avg(Grade.score / Grade.max_score * 100)
    ).scalar()
    
    return {
        "statistics": {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_courses": total_courses,
            "active_students": active_students
        },
        "recent_assignments": recent_assignments,
        "financial": {
            "total_fees": total_fees,
            "collected_fees": collected_fees,
            "pending_fees": pending_fees,
            "collection_rate": (collected_fees / total_fees * 100) if total_fees > 0 else 0
        },
        "attendance": {status: count for status, count in attendance_stats},
        "academic": {
            "average_score": round(avg_score, 2) if avg_score else 0
        }
    }

# STUDENT MANAGEMENT

@router.get("/students", response_model=List[StudentResponse])
async def get_all_students(
    skip: int = 0,
    limit: int = 100,
    grade_level: str = None,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all students"""
    students = StudentRepository.get_all(db, skip, limit, grade_level)
    return students

@router.post("/students", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Create new student"""
    # Check if user already exists
    existing_user = UserRepository.get_by_email(db, student.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserRepository.get_by_username(db, student.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user = UserRepository.create(
        db=db,
        email=student.email,
        username=student.username,
        password=student.password,
        full_name=student.full_name,
        role=UserRole.STUDENT
    )
    
    # Create student profile
    student_data = {
        "user_id": user.id,
        "student_id": student.student_id,
        "date_of_birth": student.date_of_birth,
        "phone": student.phone,
        "address": student.address,
        "parent_name": student.parent_name,
        "parent_phone": student.parent_phone,
        "grade_level": student.grade_level,
        "section": student.section
    }
    
    created_student = StudentRepository.create(db, student_data)
    return created_student

@router.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Update student"""
    student = StudentRepository.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    updated_student = StudentRepository.update(db, student, **student_update.dict(exclude_unset=True))
    return updated_student

@router.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Delete student"""
    student = StudentRepository.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    StudentRepository.delete(db, student)
    return {"message": "Student deleted successfully"}

# TEACHER MANAGEMENT

@router.get("/teachers", response_model=List[TeacherResponse])
async def get_all_teachers(
    skip: int = 0,
    limit: int = 100,
    department: str = None,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all teachers"""
    teachers = TeacherRepository.get_all(db, skip, limit, department)
    return teachers

@router.post("/teachers", response_model=TeacherResponse)
async def create_teacher(
    teacher: TeacherCreate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Create new teacher"""
    # Check if user already exists
    existing_user = UserRepository.get_by_email(db, teacher.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserRepository.get_by_username(db, teacher.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user = UserRepository.create(
        db=db,
        email=teacher.email,
        username=teacher.username,
        password=teacher.password,
        full_name=teacher.full_name,
        role=UserRole.TEACHER
    )
    
    # Create teacher profile
    teacher_data = {
        "user_id": user.id,
        "employee_id": teacher.employee_id,
        "phone": teacher.phone,
        "department": teacher.department,
        "qualification": teacher.qualification,
        "specialization": teacher.specialization
    }
    
    created_teacher = TeacherRepository.create(db, teacher_data)
    return created_teacher

@router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: int,
    teacher_update: TeacherUpdate,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Update teacher"""
    teacher = TeacherRepository.get_by_id(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    updated_teacher = TeacherRepository.update(db, teacher, **teacher_update.dict(exclude_unset=True))
    return updated_teacher

@router.delete("/teachers/{teacher_id}")
async def delete_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Delete teacher"""
    teacher = TeacherRepository.get_by_id(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    TeacherRepository.delete(db, teacher)
    return {"message": "Teacher deleted successfully"}

# ANALYTICS

@router.get("/analytics/students")
async def get_student_analytics(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get student analytics"""
    # Students by grade level
    by_grade = db.query(
        Student.grade_level,
        func.count(Student.id).label('count')
    ).group_by(Student.grade_level).all()
    
    # Enrollment trend (last 12 months)
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    enrollment_trend = db.query(
        func.extract('month', Student.enrollment_date).label('month'),
        func.count(Student.id).label('count')
    ).filter(
        Student.enrollment_date >= twelve_months_ago.date()
    ).group_by('month').all()
    
    return {
        "by_grade_level": {grade: count for grade, count in by_grade},
        "enrollment_trend": {int(month): count for month, count in enrollment_trend}
    }

@router.get("/analytics/attendance")
async def get_attendance_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get attendance analytics"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    stats = db.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.date >= cutoff_date.date()
    ).group_by(Attendance.status).all()
    
    total = sum(count for _, count in stats)
    
    return {
        "statistics": {status: count for status, count in stats},
        "total_records": total,
        "period_days": days
    }

@router.get("/analytics/performance")
async def get_performance_analytics(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get academic performance analytics"""
    # Average grades by course
    avg_by_course = db.query(
        Course.course_name,
        func.avg(Grade.score / Grade.max_score * 100).label('average')
    ).join(Grade).group_by(Course.course_name).all()
    
    # Grade distribution
    distribution = db.query(
        Grade.grade,
        func.count(Grade.id).label('count')
    ).filter(
        Grade.grade.isnot(None)
    ).group_by(Grade.grade).all()
    
    return {
        "average_by_course": {course: round(avg, 2) for course, avg in avg_by_course},
        "grade_distribution": {grade: count for grade, count in distribution}
    }
@router.get("/courses")
async def get_all_courses(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all courses"""
    from models.models import Course
    
    courses = db.query(Course).order_by(Course.course_name).all()
    return courses

@router.get("/fees")
async def get_all_fees(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all fee records"""
    from models.models import FeeRecord
    
    fees = db.query(FeeRecord).order_by(FeeRecord.due_date.desc()).all()
    
    # Calculate totals
    total_amount = sum(f.amount for f in fees)
    paid_amount = sum(f.paid_amount for f in fees)
    pending_amount = total_amount - paid_amount
    
    return {
        "fees": fees,
        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "pending_amount": pending_amount
    }

@router.get("/notices")
async def get_all_notices(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get all notices"""
    from models.models import Notice
    
    notices = db.query(Notice).order_by(Notice.created_at.desc()).all()
    return notices

@router.get("/analytics")
async def get_analytics(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get system analytics"""
    from models.models import Student, Teacher, Course, FeeRecord, Attendance
    from sqlalchemy import func
    
    # Count totals
    total_students = db.query(func.count(Student.id)).scalar()
    total_teachers = db.query(func.count(Teacher.id)).scalar()
    total_courses = db.query(func.count(Course.id)).scalar()
    
    # Fee statistics
    total_fees = db.query(func.sum(FeeRecord.amount)).scalar() or 0
    total_paid = db.query(func.sum(FeeRecord.paid_amount)).scalar() or 0
    
    # Attendance statistics
    attendance_stats = db.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).group_by(Attendance.status).all()
    
    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "total_fees": total_fees,
        "total_paid": total_paid,
        "total_pending": total_fees - total_paid,
        "attendance_stats": {status: count for status, count in attendance_stats}
    }

@router.get("/reports")
async def get_reports(
    current_user: User = Depends(get_current_authority),
    db: Session = Depends(get_db)
):
    """Get system reports"""
    from models.models import Student, Teacher, Course, Grade, Attendance, FeeRecord
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # New students
    new_students = db.query(func.count(Student.id)).filter(
        Student.enrollment_date >= thirty_days_ago.date()
    ).scalar()
    
    # Attendance summary
    recent_attendance = db.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.date >= thirty_days_ago.date()
    ).group_by(Attendance.status).all()
    
    # Fee collection
    recent_payments = db.query(func.sum(FeeRecord.paid_amount)).filter(
        FeeRecord.payment_date >= thirty_days_ago.date()
    ).scalar() or 0
    
    # Overdue fees
    overdue_fees = db.query(func.count(FeeRecord.id)).filter(
        FeeRecord.status == 'overdue'
    ).scalar()
    
    return {
        "period": "Last 30 days",
        "new_students": new_students,
        "attendance_summary": {status: count for status, count in recent_attendance},
        "recent_payments": recent_payments,
        "overdue_fees_count": overdue_fees
    }
