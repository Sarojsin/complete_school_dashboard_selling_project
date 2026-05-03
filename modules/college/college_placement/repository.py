"""
College Placement Repository

Async CRUD operations for college placement management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import PlacementCompany, PlacementJob, PlacementApplication


# ── Company Repository ─────────────────────────────────────────
class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, company_id: int) -> Optional[PlacementCompany]:
        result = await self.db.execute(select(PlacementCompany).filter(PlacementCompany.id == company_id))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[PlacementCompany]:
        result = await self.db.execute(select(PlacementCompany).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def create(self, company: PlacementCompany) -> PlacementCompany:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company
    
    async def update(self, company: PlacementCompany) -> PlacementCompany:
        await self.db.commit()
        await self.db.refresh(company)
        return company
    
    async def delete(self, company_id: int) -> bool:
        company = await self.get_by_id(company_id)
        if company:
            await self.db.delete(company)
            await self.db.commit()
            return True
        return False


# ── Job Repository ─────────────────────────────────────────────
class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, job_id: int) -> Optional[PlacementJob]:
        result = await self.db.execute(select(PlacementJob).filter(PlacementJob.id == job_id))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        result = await self.db.execute(select(PlacementJob).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def list_by_company(self, company_id: int, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        result = await self.db.execute(
            select(PlacementJob).filter(PlacementJob.company_id == company_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_active(self, skip: int = 0, limit: int = 100) -> List[PlacementJob]:
        result = await self.db.execute(
            select(PlacementJob).filter(PlacementJob.is_active == True).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, job: PlacementJob) -> PlacementJob:
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job
    
    async def update(self, job: PlacementJob) -> PlacementJob:
        await self.db.commit()
        await self.db.refresh(job)
        return job
    
    async def delete(self, job_id: int) -> bool:
        job = await self.get_by_id(job_id)
        if job:
            await self.db.delete(job)
            await self.db.commit()
            return True
        return False


# ── Application Repository ──────────────────────────────────────
class ApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, application_id: int) -> Optional[PlacementApplication]:
        result = await self.db.execute(select(PlacementApplication).filter(PlacementApplication.id == application_id))
        return result.scalars().first()
    
    async def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[PlacementApplication]:
        result = await self.db.execute(
            select(PlacementApplication).filter(PlacementApplication.student_id == student_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_job(self, job_id: int, skip: int = 0, limit: int = 100) -> List[PlacementApplication]:
        result = await self.db.execute(
            select(PlacementApplication).filter(PlacementApplication.job_id == job_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_student_and_job(self, student_id: int, job_id: int) -> Optional[PlacementApplication]:
        result = await self.db.execute(
            select(PlacementApplication)
            .filter(PlacementApplication.student_id == student_id)
            .filter(PlacementApplication.job_id == job_id)
        )
        return result.scalars().first()
    
    async def create(self, application: PlacementApplication) -> PlacementApplication:
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def update(self, application: PlacementApplication) -> PlacementApplication:
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def delete(self, application_id: int) -> bool:
        application = await self.get_by_id(application_id)
        if application:
            await self.db.delete(application)
            await self.db.commit()
            return True
        return False