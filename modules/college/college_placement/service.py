"""
College Placement Service

Business logic for college placement operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import CompanyRepository, JobRepository, ApplicationRepository
from .models import PlacementCompany, PlacementJob, PlacementApplication
from .schemas import CompanyCreate, CompanyUpdate, JobCreate, JobUpdate, ApplicationCreate, ApplicationUpdate


class PlacementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.company_repo = CompanyRepository(db)
        self.job_repo = JobRepository(db)
        self.app_repo = ApplicationRepository(db)
    
    # ── Company Methods ─────────────────────────────────────────
    async def create_company(self, data: CompanyCreate) -> PlacementCompany:
        company = PlacementCompany(**data.model_dump())
        return await self.company_repo.create(company)
    
    async def get_company(self, company_id: int) -> Optional[PlacementCompany]:
        return await self.company_repo.get_by_id(company_id)
    
    async def list_companies(self, skip: int = 0, limit: int = 100) -> List[PlacementCompany]:
        return await self.company_repo.list(skip, limit)
    
    async def update_company(self, company_id: int, data: CompanyUpdate) -> Optional[PlacementCompany]:
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        return await self.company_repo.update(company)
    
    async def delete_company(self, company_id: int) -> bool:
        return await self.company_repo.delete(company_id)
    
    # ── Job Methods ─────────────────────────────────────────────
    async def create_job(self, data: JobCreate) -> PlacementJob:
        job = PlacementJob(**data.model_dump())
        return await self.job_repo.create(job)
    
    async def get_job(self, job_id: int) -> Optional[PlacementJob]:
        return await self.job_repo.get_by_id(job_id)
    
    async def list_jobs(self, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        return await self.job_repo.list(skip, limit)
    
    async def list_active_jobs(self, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        return await self.job_repo.list_active(skip, limit)
    
    async def list_jobs_by_company(self, company_id: int, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        return await self.job_repo.list_by_company(company_id, skip, limit)
    
    async def update_job(self, job_id: int, data: JobUpdate) -> Optional[PlacementJob]:
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(job, key, value)
        return await self.job_repo.update(job)
    
    async def delete_job(self, job_id: int) -> bool:
        return await self.job_repo.delete(job_id)
    
    # ── Application Methods ─────────────────────────────────────
    async def apply_for_job(self, student_id: int, job_id: int) -> PlacementApplication:
        # Check if already applied
        existing = await self.app_repo.get_by_student_and_job(student_id, job_id)
        if existing:
            raise ValueError("Already applied for this job")
        
        application = PlacementApplication(student_id=student_id, job_id=job_id)
        return await self.app_repo.create(application)
    
    async def get_application(self, application_id: int) -> Optional[PlacementApplication]:
        return await self.app_repo.get_by_id(application_id)
    
    async def get_student_applications(self, student_id: int, skip: int = 0, limit: int = 100) -> List[PlacementApplication]:
        return await self.app_repo.get_by_student(student_id, skip, limit)
    
    async def get_job_applications(self, job_id: int, skip: int = 0, limit: int = 100) -> List[PlacementApplication]:
        return await self.app_repo.get_by_job(job_id, skip, limit)
    
    async def update_application_status(self, application_id: int, status: str, notes: str = None) -> Optional[PlacementApplication]:
        application = await self.app_repo.get_by_id(application_id)
        if not application:
            return None
        application.status = status
        if notes:
            application.notes = notes
        return await self.app_repo.update(application)