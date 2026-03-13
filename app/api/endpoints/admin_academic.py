"""
Admin Academic Management API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Endpoints for managing courses, departments, and timetables.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminAcademicService`.
- No direct database manipulations in the routing layer.
"""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin
from app.api.schemas.admin.academic import (
    CourseCreateRequest, CourseUpdateRequest,
    DepartmentCreateRequest, DepartmentUpdateRequest
)
from app.services.admin_academic_service import AdminAcademicService


router = APIRouter(prefix="/admin/academic", tags=["Admin Academic"])


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------

@router.get("/courses")
async def get_all_courses_admin(
    grade_level: Optional[str] = None,
    teacher_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all courses with optional grade, teacher, and text filters."""
    return await AdminAcademicService.get_all_courses(
        db, grade_level, teacher_id, search, skip, limit
    )


@router.post("/courses", status_code=201)
async def create_course_admin(
    course_data: CourseCreateRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Create a new course, enforcing unique code and valid teacher reference."""
    return await AdminAcademicService.create_course(db, course_data)


@router.patch("/courses/{course_id}")
async def update_course_admin(
    course_id: int,
    course_data: CourseUpdateRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Partially update a course."""
    return await AdminAcademicService.update_course(db, course_id, course_data)


@router.delete("/courses/{course_id}")
async def delete_course_admin(
    course_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Delete a course by ID."""
    return await AdminAcademicService.delete_course(db, course_id)


# ---------------------------------------------------------------------------
# Departments
# ---------------------------------------------------------------------------

@router.get("/departments")
async def get_all_departments_admin(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all departments with optional name filter."""
    return await AdminAcademicService.get_all_departments(db, search, skip, limit)


@router.post("/departments", status_code=201)
async def create_department_admin(
    dept_data: DepartmentCreateRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Create a new department, enforcing unique code and valid HOD reference."""
    return await AdminAcademicService.create_department(db, dept_data)


@router.patch("/departments/{dept_id}")
async def update_department_admin(
    dept_id: int,
    dept_data: DepartmentUpdateRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Partially update a department using exclude_unset pattern."""
    return await AdminAcademicService.update_department(db, dept_id, dept_data)


@router.delete("/departments/{dept_id}")
async def delete_department_admin(
    dept_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Delete a department by ID."""
    return await AdminAcademicService.delete_department(db, dept_id)


# ---------------------------------------------------------------------------
# Timetable
# ---------------------------------------------------------------------------

@router.get("/timetable")
async def get_timetable_admin(
    course_id: Optional[int] = None,
    day: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return timetable entries."""
    entries = await AdminAcademicService.get_timetable(db, course_id, day)
    return {"entries": entries, "total": len(entries)}


@router.get("/timetable/conflicts")
async def check_timetable_conflicts(
    course_id: int,
    day_of_week: str,
    start_time: str,
    end_time: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Check for scheduling conflicts (pending TimetableEntry model)."""
    return await AdminAcademicService.check_timetable_conflicts(
        db, course_id, day_of_week, start_time, end_time
    )


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

@router.get("/stats")
async def get_academic_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return academic statistics for courses, departments, teachers, and students."""
    return await AdminAcademicService.get_academic_stats(db)
