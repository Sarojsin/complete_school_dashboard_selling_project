"""
College Faculty Router

FastAPI endpoints for college faculty operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import FacultyService
from .schemas import FacultyResponse, FacultyUpdate, FacultyCreate

router = APIRouter(prefix="/faculty", tags=["College Faculty"], dependencies=[Depends(require_college_portal)])


@router.post("/", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    data: FacultyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new faculty member (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create faculty"
        )
    service = FacultyService(db)
    return await service.create(data)


@router.get("/", response_model=List[FacultyResponse])
async def list_faculty(
    skip: int = 0,
    limit: int = 20,
    department_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all faculty members (Protected)"""
    service = FacultyService(db)
    
    if department_id:
        return await service.list_by_department(department_id, skip, limit)
    return await service.list_faculty(skip, limit)


@router.get("/me", response_model=FacultyResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current faculty profile (Protected)"""
    service = FacultyService(db)
    faculty = await service.get_my_profile(current_user.id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found for current user"
        )
    return faculty


@router.patch("/me", response_model=FacultyResponse)
async def update_my_profile(
    faculty_data: FacultyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current faculty profile (Protected)"""
    service = FacultyService(db)
    faculty = await service.update_profile(current_user.id, faculty_data)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found"
        )
    return faculty


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get faculty by ID (Protected)"""
    service = FacultyService(db)
    faculty = await service.get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    return faculty


@router.put("/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: int,
    data: FacultyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update faculty by ID (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update faculty"
        )
    service = FacultyService(db)
    faculty = await service.update(faculty_id, data)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete faculty by ID (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete faculty"
        )
    service = FacultyService(db)
    success = await service.delete(faculty_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )


# ── Faculty Dashboard ──────────────────────────────────────────
@router.get("/dashboard")
async def get_faculty_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get faculty dashboard (Protected)"""
    service = FacultyService(db)
    faculty = await service.get_my_profile(current_user.id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found"
        )
    
    return {
        "faculty_id": faculty.id,
        "employee_id": faculty.employee_id,
        "designation": faculty.designation,
        "department_id": faculty.department_id,
        "message": "College faculty dashboard - extend with courses, students, etc."
    }


# ── Faculty Courses ─────────────────────────────────────────────
@router.get("/my-courses", response_model=List[dict])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get courses taught by current faculty (Protected)"""
    service = FacultyService(db)
    return await service.get_my_courses(current_user.id)


# ── Faculty Students ────────────────────────────────────────────
@router.get("/my-students", response_model=List[dict])
async def get_my_students(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get students in faculty's courses (Protected)"""
    service = FacultyService(db)
    return await service.get_my_students(current_user.id)


__all__ = ["router"]