"""
Authority API Routes

API routes for authority management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from typing import List, Optional
from modules.shared.models import User, UserRole
from .service import AuthorityService
from .schemas import (
    AuthorityCreate,
    AuthorityUpdate,
    AuthorityResponse,
    AuthorityListResponse,
)

router = APIRouter(prefix="/authorities", tags=["School Authority"], dependencies=[Depends(require_school_portal)])


@router.get("/", response_model=AuthorityListResponse)
async def list_authorities(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all authorities (Protected)"""
    service = AuthorityService(db)
    return await service.list_authorities(skip, limit)


@router.get("/me", response_model=AuthorityResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current authority profile (Protected)"""
    service = AuthorityService(db)
    authority = await service.get_authority_by_user(current_user.id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority profile not found")
    return authority




@router.post("/", response_model=AuthorityResponse, status_code=status.HTTP_201_CREATED)
async def create_authority(
    authority_data: AuthorityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new authority (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create authorities")
    service = AuthorityService(db)
    try:
        return await service.create_authority(authority_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/dashboard")
async def get_authority_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get authority dashboard (Protected)"""
    service = AuthorityService(db)
    authority = await service.get_authority_by_user(current_user.id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority profile not found")
    
    # Return basic dashboard data
    return {
        "authority_id": authority.id,
        "full_name": authority.full_name,
        "position": authority.position,
        "department": authority.department,
        "message": "Authority dashboard - extend with analytics, students, teachers, etc."
    }


# ── Authority's Students (manage all students) ─────────────────────
@router.get("/students", response_model=List[dict])
async def get_all_students(
    skip: int = 0,
    limit: int = 100,
    grade_level: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all students (Authority only)"""
    from modules.school.school_student.repository import StudentRepository
    repo = StudentRepository(db)
    students = await repo.list(skip, limit)
    return students


# ── Authority's Teachers (manage all teachers) ─────────────────────
@router.get("/teachers", response_model=List[dict])
async def get_all_teachers(
    skip: int = 0,
    limit: int = 100,
    department: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all teachers (Authority only)"""
    from modules.school.school_teacher.repository import TeacherRepository
    repo = TeacherRepository(db)
    teachers = await repo.get_all(department, None, skip, limit)
    return teachers


# ── Authority's Courses (manage all courses) ─────────────────────
@router.get("/courses", response_model=List[dict])
async def get_all_courses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all courses (Authority only)"""
    from modules.school.school_courses.repository import CourseRepository
    courses = await CourseRepository.get_all(db, skip, limit)
    return courses


# ── Authority's Fees (manage all fees) ─────────────────────────────
@router.get("/fees", response_model=List[dict])
async def get_all_fees(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all fee records (Authority only)"""
    from modules.school.school_account_section.repository import FeeRepository
    fees = await FeeRepository.get_all(db, skip, limit)
    return fees


# ── Authority's Notices (manage all notices) ──────────────────────
@router.get("/notices", response_model=List[dict])
async def get_all_notices(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all notices (Authority only)"""
    from modules.school.school_notices.repository import NoticeRepository
    notices = await NoticeRepository.get_all(db, skip, limit)
    return notices


# ── Analytics: Student Analytics ───────────────────────────────────
@router.get("/analytics/students")
async def get_student_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get student analytics (Authority only)"""
    from modules.school.school_student.repository import StudentRepository
    repo = StudentRepository(db)
    students = await repo.list(skip=0, limit=1000)
    
    # Simple analytics
    grade_counts = {}
    for s in students:
        grade = s.grade_level or "unknown"
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    return {
        "total_students": len(students),
        "by_grade": grade_counts
    }


# ── Analytics: Attendance Analytics ────────────────────────────────
@router.get("/analytics/attendance")
async def get_attendance_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance analytics (Authority only)"""
    from modules.school.school_attendance.repository import AttendanceRepository
    from modules.school.school_attendance.models import AttendanceRecord
    from sqlalchemy import select
    repo = AttendanceRepository(db)
    
    # Get recent attendance records
    result = await db.execute(select(AttendanceRecord).order_by(AttendanceRecord.id.desc()).limit(500))
    records = list(result.scalars().all())
    
    total_records = len(records)
    present_count = sum(1 for r in records if getattr(r, 'status', None) == 'present')
    
    return {
        "total_records": total_records,
        "present": present_count,
        "absent": total_records - present_count,
        "attendance_rate": round(present_count / total_records * 100, 2) if total_records > 0 else 0
    }


# ── Analytics: Performance Analytics ────────────────────────────────
@router.get("/analytics/performance")
async def get_performance_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get performance analytics (Authority only)"""
    from modules.school.school_grades.repository import GradeRepository
    repo = GradeRepository(db)
    
    # This is simplified - in real implementation would aggregate properly
    return {
        "message": "Performance analytics - extend with grade aggregation"
    }


# ── Reports ───────────────────────────────────────────────────────
@router.get("/reports")
async def get_reports(
    report_type: str = "summary",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get reports (Authority only)"""
    return {
        "report_type": report_type,
        "message": f"{report_type} report generation"
    }



@router.get("/{authority_id}", response_model=AuthorityResponse)
async def get_authority(
    authority_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get authority by ID (Protected)"""
    service = AuthorityService(db)
    authority = await service.get_authority(authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    return authority

@router.patch("/{authority_id}", response_model=AuthorityResponse)
async def update_authority(
    authority_id: int,
    authority_data: AuthorityUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update authority (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update authorities")
    service = AuthorityService(db)
    authority = await service.update_authority(authority_id, authority_data)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    return authority

@router.delete("/{authority_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_authority(
    authority_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete authority (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete authorities")
    service = AuthorityService(db)
    authority = await service.get_authority(authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")
    await service.delete_authority(authority_id)

__all__ = ["router"]