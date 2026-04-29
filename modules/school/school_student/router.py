from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User, UserRole
from .service import StudentService
from .schemas import StudentResponse, StudentUpdate, StudentCreate

router = APIRouter(prefix="/students", tags=["School Students"], dependencies=[Depends(require_school_portal)])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    data: StudentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new student (Protected - Authority/Admin only)"""
    # Check permission - only authority or admin can create students
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create students")
    service = StudentService(db)
    return await service.create(data)

@router.get("/", response_model=List[StudentResponse])
async def list_students(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all students (Protected)"""
    service = StudentService(db)
    return await service.list_students(skip, limit)

@router.get("/me", response_model=StudentResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current student profile (Protected)"""
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student profile not found for current user")
    return student

@router.patch("/me", response_model=StudentResponse)
async def update_my_profile(
    student_data: StudentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current student profile (Protected)"""
    service = StudentService(db)
    student = await service.update_profile(current_user.id, student_data)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student profile not found")
    return student

@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get student dashboard (Protected)"""
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student profile not found")
    
    # Return basic dashboard data
    return {
        "student_id": student.id,
        "student_id_value": student.student_id,
        "full_name": student.full_name,
        "grade_level": student.grade_level,
        "section": student.section,
        "message": "Student dashboard - extend with courses, assignments, grades, etc."
    }





# ── Student's Courses ───────────────────────────────────
@router.get("/my-courses", response_model=List[dict])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get courses enrolled by current student (Protected)"""
    from modules.school.school_courses.repository import CourseRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get enrolled courses
    courses = await CourseRepository.get_enrolled_courses(db, student.id)
    return courses


# ── Student's Assignments ───────────────────────────────
@router.get("/my-assignments", response_model=List[dict])
async def get_my_assignments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assignments for current student (Protected)"""
    from modules.school.school_assignments.repository import AssignmentRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get assignments for student
    from modules.school.school_courses.repository import CourseRepository
    courses = await CourseRepository.get_enrolled_courses(db, student.id)
    course_ids = [c.course_id for c in courses] if courses else []
    assignments = await AssignmentRepository.get_student_assignments(
        db, student.id, course_ids, student.grade_level, student.section
    )
    return assignments


# ── Student's Grades ─────────────────────────────────────
@router.get("/my-grades", response_model=List[dict])
async def get_my_grades(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get grades for current student (Protected)"""
    from modules.school.school_grades.repository import GradeRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get grades for student
    repo = GradeRepository(db)
    grades = await repo.get_by_student(student.id)
    return grades


# ── Student's Attendance ─────────────────────────────────
@router.get("/my-attendance", response_model=List[dict])
async def get_my_attendance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance records for current student (Protected)"""
    from modules.school.school_attendance.repository import AttendanceRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get attendance for student
    repo = AttendanceRepository(db)
    summary = await repo.get_student_attendance_summary(student.id)
    return [summary]


# ── Student's Fees ────────────────────────────────────────
@router.get("/my-fees", response_model=List[dict])
async def get_my_fees(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get fee records for current student (Protected)"""
    from modules.school.school_account_section.repository import AccountSectionRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get fees for student
    repo = AccountSectionRepository(db)
    fees = await repo.list_fees(student_id=student.id)
    return fees


# ── Student's Tests ───────────────────────────────────────
@router.get("/my-tests", response_model=List[dict])
async def get_my_tests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get available tests for current student (Protected)"""
    from modules.school.school_tests.repository import TestRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get available tests for student
    tests = await TestRepository.get_available_tests_for_student(db, student.id, student.section, student.grade_level)
    return tests


# ── Student's Notices ─────────────────────────────────────
@router.get("/my-notices", response_model=List[dict])
async def get_my_notices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get notices for current student (Protected)"""
    from modules.school.school_notices.repository import NoticeRepository
    
    # Get all notices
    notices = await NoticeRepository.get_recent_notices(db, days=30)
    return notices


# ── Student's Timetable ───────────────────────────────────
@router.get("/my-timetable", response_model=List[dict])
async def get_my_timetable(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get timetable for current student (Protected)"""
    from modules.school.school_timetable.repository import TimetableRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get timetable for student
    timetable = await TimetableRepository.get_all(db, skip=0, limit=20)
    return timetable


# ── Student's Notes ───────────────────────────────────────
@router.get("/my-notes", response_model=List[dict])
async def get_my_notes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get notes for current student (Protected)"""
    from modules.school.school_notes.repository import NoteRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get notes for student
    repo = NoteRepository(db)
    notes = await repo.get_recent(limit=20)
    return notes


# ── Student's Videos ─────────────────────────────────────
@router.get("/my-videos", response_model=List[dict])
async def get_my_videos(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get videos for current student (Protected)"""
    from modules.school.school_videos.repository import VideoRepository
    
    # Get student profile first
    service = StudentService(db)
    student = await service.get_my_profile(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    # Get videos for student's grade level
    videos = await VideoRepository.get_recent_videos(db, limit=20)
    return videos



@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get student by ID (Protected)"""
    service = StudentService(db)
    student = await service.get_student(student_id)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student not found")
    return student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    data: StudentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update student by ID (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update students")
    service = StudentService(db)
    student = await service.update(student_id, data)
    if not student:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student not found")
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete student by ID (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete students")
    service = StudentService(db)
    success = await service.delete(student_id)
    if not success:
        from modules.shared.exceptions import NotFoundError
        raise NotFoundError("Student not found")

__all__ = ["router"]
