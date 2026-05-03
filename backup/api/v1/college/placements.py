"""
College Placements API
=====================
API endpoints for campus placement system.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.college import Company, Job, Application

router = APIRouter(prefix="/placements", tags=["Placements"])


# Company Endpoints
@router.get("/companies")
async def list_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all companies"""
    res = await db.execute(select(Company).offset(skip).limit(limit))
    companies = res.scalars().all()
    return companies


@router.get("/companies/{company_id}")
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get company details"""
    res = await db.execute(select(Company).filter(Company.id == company_id))
    company = res.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/companies")
async def create_company(
    name: str,
    industry: str = None,
    website: str = None,
    description: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new company"""
    company = Company(
        name=name,
        industry=industry,
        website=website,
        description=description
    )
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


# Job Endpoints
@router.get("/jobs")
async def list_jobs(
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List job postings"""
    query = select(Job)
    if active_only:
        query = query.filter(Job.is_active == True)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    jobs = res.scalars().all()
    return jobs


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get job details"""
    res = await db.execute(select(Job).filter(Job.id == job_id))
    job = res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs")
async def create_job(
    company_id: int,
    title: str,
    description: str = None,
    requirements: str = None,
    salary_min: int = None,
    salary_max: int = None,
    location: str = None,
    job_type: str = "full-time",
    deadline: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new job posting"""
    from datetime import datetime
    
    # Check company exists
    res = await db.execute(select(Company).filter(Company.id == company_id))
    company = res.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    job = Job(
        company_id=company_id,
        title=title,
        description=description,
        requirements=requirements,
        salary_min=salary_min,
        salary_max=salary_max,
        location=location,
        job_type=job_type,
        deadline=datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


# Application Endpoints
@router.post("/apply")
async def apply_for_job(
    job_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Apply for a job"""
    # Check job exists and is active
    res = await db.execute(select(Job).filter(Job.id == job_id, Job.is_active == True))
    job = res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or closed")
    
    # Check not already applied
    res = await db.execute(
        select(Application).filter(
            Application.job_id == job_id,
            Application.student_id == student_id
        )
    )
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied for this job")
    
    application = Application(
        job_id=job_id,
        student_id=student_id,
        status="applied"
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


@router.get("/applications/student/{student_id}")
async def get_student_applications(
    student_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get student's applications"""
    res = await db.execute(
        select(Application).filter(Application.student_id == student_id)
    )
    applications = res.scalars().all()
    return applications


@router.get("/applications/job/{job_id}")
async def get_job_applications(
    job_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get applications for a job"""
    res = await db.execute(
        select(Application).filter(Application.job_id == job_id)
    )
    applications = res.scalars().all()
    return applications


@router.put("/applications/{application_id}/status")
async def update_application_status(
    application_id: int,
    status: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update application status"""
    res = await db.execute(
        select(Application).filter(Application.id == application_id)
    )
    application = res.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = status
    await db.commit()
    await db.refresh(application)
    return application


__all__ = ["router"]
