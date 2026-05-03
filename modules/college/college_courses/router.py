"""
College Courses Router

FastAPI endpoints for college courses, departments, programs, semesters, enrollments.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import CollegeCoursesService
from .schemas import (
    CollegeCourseResponse, CollegeCourseCreate, CollegeCourseUpdate,
    DepartmentResponse, DepartmentCreate, DepartmentUpdate,
    ProgramResponse, ProgramCreate, ProgramUpdate,
    SemesterResponse, SemesterCreate, SemesterUpdate,
    EnrollmentResponse, EnrollmentCreate, EnrollmentUpdate
)

router = APIRouter(prefix="/courses", tags=["College Courses"], dependencies=[Depends(require_college_portal)])


# ── Course Endpoints ───────────────────────────────────────────
@router.post("/courses", response_model=CollegeCourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    data: CollegeCourseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new course (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    return await service.create_course(data)


@router.get("/courses", response_model=List[CollegeCourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 20,
    department_id: int = None,
    semester_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List courses (Protected)"""
    service = CollegeCoursesService(db)
    if department_id:
        return await service.list_courses_by_department(department_id, skip, limit)
    elif semester_id:
        return await service.list_courses_by_semester(semester_id, skip, limit)
    return await service.list_courses(skip, limit)


@router.get("/courses/{course_id}", response_model=CollegeCourseResponse)
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get course by ID (Protected)"""
    service = CollegeCoursesService(db)
    course = await service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.patch("/courses/{course_id}", response_model=CollegeCourseResponse)
async def update_course(
    course_id: int,
    data: CollegeCourseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update course (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    course = await service.update_course(course_id, data)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete course (Protected - Dean/Registrar only)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    await service.delete_course(course_id)


# ── Department Endpoints ───────────────────────────────────────
@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new department (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    return await service.create_department(data)


@router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List departments (Protected)"""
    service = CollegeCoursesService(db)
    return await service.list_departments(skip, limit)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get department by ID (Protected)"""
    service = CollegeCoursesService(db)
    dept = await service.get_department(department_id)
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return dept


@router.patch("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update department (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    dept = await service.update_department(department_id, data)
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return dept


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete department (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    await service.delete_department(department_id)


# ── Program Endpoints ───────────────────────────────────────────
@router.post("/programs", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    data: ProgramCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new program (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    return await service.create_program(data)


@router.get("/programs", response_model=List[ProgramResponse])
async def list_programs(
    skip: int = 0,
    limit: int = 20,
    department_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List programs (Protected)"""
    service = CollegeCoursesService(db)
    if department_id:
        return await service.list_programs_by_department(department_id, skip, limit)
    return await service.list_programs(skip, limit)


@router.get("/programs/{program_id}", response_model=ProgramResponse)
async def get_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get program by ID (Protected)"""
    service = CollegeCoursesService(db)
    program = await service.get_program(program_id)
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program not found")
    return program


# ── Semester Endpoints ─────────────────────────────────────────
@router.get("/semesters", response_model=List[SemesterResponse])
async def list_semesters(
    skip: int = 0,
    limit: int = 20,
    program_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List semesters (Protected)"""
    service = CollegeCoursesService(db)
    if program_id:
        return await service.list_semesters_by_program(program_id, skip, limit)
    return await service.list_semesters(skip, limit)


@router.get("/semesters/{semester_id}", response_model=SemesterResponse)
async def get_semester(
    semester_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get semester by ID (Protected)"""
    service = CollegeCoursesService(db)
    semester = await service.get_semester(semester_id)
    if not semester:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Semester not found")
    return semester


# ── Enrollment Endpoints ────────────────────────────────────────
@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_student(
    data: EnrollmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Enroll student in course (Protected - Dean/Registrar/Faculty)"""
    if current_user.role not in ["dean", "registrar", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    try:
        return await service.enroll_student(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/enrollments", response_model=List[EnrollmentResponse])
async def list_enrollments(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List enrollments (Protected)"""
    service = CollegeCoursesService(db)
    return await service.list_enrollments(skip, limit)


@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get enrollment by ID (Protected)"""
    service = CollegeCoursesService(db)
    enrollment = await service.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment


@router.patch("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update enrollment (Protected - Dean/Registrar/Faculty)"""
    if current_user.role not in ["dean", "registrar", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    enrollment = await service.update_enrollment(enrollment_id, data)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment


@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Drop course (Protected - Dean/Registrar)"""
    if current_user.role not in ["dean", "registrar", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = CollegeCoursesService(db)
    await service.delete_enrollment(enrollment_id)


__all__ = ["router"]