"""
College Placement Router

FastAPI endpoints for college placement operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from .service import PlacementService
from .schemas import (
    CompanyResponse, CompanyCreate, CompanyUpdate,
    JobResponse, JobCreate, JobUpdate,
    ApplicationResponse, ApplicationCreate, ApplicationUpdate
)

router = APIRouter(prefix="/placements", tags=["College Placement"], dependencies=[Depends(require_college_portal)])


# ── Company Endpoints ──────────────────────────────────────────
@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new company (Protected - Dean/TPO only)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = PlacementService(db)
    return await service.create_company(data)


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List companies (Protected)"""
    service = PlacementService(db)
    return await service.list_companies(skip, limit)


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get company by ID (Protected)"""
    service = PlacementService(db)
    company = await service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


# ── Job Endpoints ───────────────────────────────────────────────
@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new job (Protected - Dean/TPO only)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = PlacementService(db)
    return await service.create_job(data)


@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 20,
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List jobs (Protected)"""
    service = PlacementService(db)
    if active_only:
        return await service.list_active_jobs(skip, limit)
    return await service.list_jobs(skip, limit)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get job by ID (Protected)"""
    service = PlacementService(db)
    job = await service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


# ── Application Endpoints ───────────────────────────────────────
@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Apply for a job (Protected - Student)"""
    if current_user.role not in ["student", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Get student profile
    from modules.college.college_student.repository import CollegeStudentRepository
    student_repo = CollegeStudentRepository(db)
    student = await student_repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    service = PlacementService(db)
    try:
        return await service.apply_for_job(student.id, job_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/applications/student/{student_id}", response_model=List[ApplicationResponse])
async def get_student_applications(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get student's applications (Protected)"""
    service = PlacementService(db)
    return await service.get_student_applications(student_id)


@router.get("/applications/job/{job_id}", response_model=List[ApplicationResponse])
async def get_job_applications(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get job applications (Protected - Dean/TPO only)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = PlacementService(db)
    return await service.get_job_applications(job_id)


@router.patch("/applications/{application_id}/status")
async def update_application_status(
    application_id: int,
    status: str,
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update application status (Protected - Dean/TPO only)"""
    if current_user.role not in ["dean", "faculty", "super_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    service = PlacementService(db)
    application = await service.update_application_status(application_id, status, notes)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return {"message": "Status updated"}


__all__ = ["router"]