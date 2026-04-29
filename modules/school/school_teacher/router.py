# School Teacher API Routes
# ======================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user
from modules.shared.models import User
from .service import TeacherService
from .schemas import TeacherResponse, TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["School Teachers"])


@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    data: TeacherCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new teacher (Protected)"""
    service = TeacherService(db)
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))




@router.get("/by-user/{user_id}", response_model=TeacherResponse)
async def get_teacher_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get teacher by user ID (Protected)"""
    service = TeacherService(db)
    teacher = await service.get_by_user_id(user_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.get("/", response_model=List[TeacherResponse])
async def list_teachers(
    department: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all teachers with optional filtering (Protected)"""
    service = TeacherService(db)
    return await service.get_all(department, status, skip, limit)


# Legacy endpoints for backward compatibility
@router.get("/me", response_model=TeacherResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current teacher profile (Protected)"""
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found for current user")
    return teacher


@router.put("/me", response_model=TeacherResponse)
async def update_my_profile(
    data: TeacherUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current teacher profile (Protected)"""
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found for current user")
    return await service.update(teacher.id, data)


@router.get("/dashboard")
async def get_teacher_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get teacher dashboard (Protected)"""
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Return basic dashboard data
    return {
        "teacher_id": teacher.id,
        "employee_id": teacher.employee_id,
        "full_name": teacher.full_name,
        "department": teacher.department,
        "status": teacher.status,
        "message": "Teacher dashboard - extend with courses, students, assignments, etc."
    }


# ── Teacher's Courses ───────────────────────────────────
@router.get("/my-courses", response_model=List[dict])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get courses assigned to current teacher (Protected)"""
    from modules.school.school_courses.repository import CourseRepository
    repo = CourseRepository(db)
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get courses by teacher_id
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id)
    return courses


# ── Teacher's Students ──────────────────────────────────
@router.get("/my-students", response_model=List[dict])
async def get_my_students(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get students taught by current teacher (Protected)"""
    from modules.school.school_student.repository import StudentRepository
    repo = StudentRepository(db)
    
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get students by teacher_id
    students = await repo.get_by_teacher_id(teacher.id)
    return students


# ── Teacher's Assignments ───────────────────────────────
@router.get("/my-assignments", response_model=List[dict])
async def get_my_assignments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assignments created by current teacher (Protected)"""
    from modules.school.school_assignments.repository import AssignmentRepository
    repo = AssignmentRepository(db)
    
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get assignments by teacher_id
    assignments = await AssignmentRepository.get_all(db, teacher_id=teacher.id)
    return assignments


# ── Teacher's Tests ─────────────────────────────────────
@router.get("/my-tests", response_model=List[dict])
async def get_my_tests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get tests created by current teacher (Protected)"""
    from modules.school.school_tests.repository import TestRepository
    repo = TestRepository(db)
    
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get tests by teacher_id
    tests = await TestRepository.get_all(db, teacher_id=teacher.id)
    return tests


# ── Teacher's Attendance ────────────────────────────────
@router.get("/my-attendance", response_model=List[dict])
async def get_my_attendance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance records for current teacher (Protected)"""
    from modules.school.school_attendance.repository import AttendanceRepository
    repo = AttendanceRepository(db)
    
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get attendance by teacher_id
    records = await repo.get_by_teacher_id(teacher.id)
    return records


# ── Teacher's Timetable ──────────────────────────────────
@router.get("/my-timetable", response_model=List[dict])
async def get_my_timetable(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get timetable for current teacher (Protected)"""
    from modules.school.school_timetable.repository import TimetableRepository
    repo = TimetableRepository(db)
    
    # Get teacher profile first
    service = TeacherService(db)
    teacher = await service.get_my_profile(current_user.id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found")
    
    # Get timetable by teacher_id
    timetable = await repo.get_by_teacher_id(teacher.id)
    return timetable



@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get teacher by ID (Protected)"""
    service = TeacherService(db)
    teacher = await service.get(teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher

@router.put("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: int,
    data: TeacherUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update teacher (Protected)"""
    service = TeacherService(db)
    teacher = await service.update(teacher_id, data)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete teacher (Protected)"""
    service = TeacherService(db)
    success = await service.delete(teacher_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

@router.post("/{teacher_id}/deactivate", response_model=TeacherResponse)
async def deactivate_teacher(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deactivate teacher (Protected)"""
    service = TeacherService(db)
    teacher = await service.deactivate(teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher

__all__ = ["router"]
