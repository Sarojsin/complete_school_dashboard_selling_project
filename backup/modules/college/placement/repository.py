# College Placement Repository
# ============================
# Database operations for placement module

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import date

from backup.modules.college.placement.schemas import (
    CompanyCreate,
    CompanyUpdate,
    JobCreate,
    JobUpdate,
    ApplicationCreate,
    ApplicationUpdate,
    PlacementDriveCreate,
    PlacementDriveUpdate,
)
from backup.models.college.placement import Company, Job, Application, PlacementDrive


class PlacementRepository:
    """Repository for placement-related database operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # Company operations
    async def create_company(self, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def get_company(self, company_id: int) -> Optional[Company]:
        result = await self.db.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def get_companies(self, skip: int = 0, limit: int = 100) -> List[Company]:
        result = await self.db.execute(
            select(Company).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_company(self, company_id: int, data: CompanyUpdate) -> Optional[Company]:
        await self.db.execute(
            update(Company).where(Company.id == company_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_company(company_id)

    async def delete_company(self, company_id: int) -> bool:
        company = await self.get_company(company_id)
        if company:
            await self.db.delete(company)
            await self.db.commit()
            return True
        return False

    # Job operations
    async def create_job(self, data: JobCreate) -> Job:
        job = Job(**data.model_dump())
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def get_job(self, job_id: int) -> Optional[Job]:
        result = await self.db.execute(
            select(Job).options(selectinload(Job.company)).where(Job.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_jobs(
        self,
        company_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Job]:
        query = select(Job).options(selectinload(Job.company))
        
        if company_id is not None:
            query = query.where(Job.company_id == company_id)
        if is_active is not None:
            query = query.where(Job.is_active == is_active)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_job(self, job_id: int, data: JobUpdate) -> Optional[Job]:
        await self.db.execute(
            update(Job).where(Job.id == job_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_job(job_id)

    async def delete_job(self, job_id: int) -> bool:
        job = await self.get_job(job_id)
        if job:
            await self.db.delete(job)
            await self.db.commit()
            return True
        return False

    # Application operations
    async def create_application(self, data: ApplicationCreate) -> Application:
        application = Application(**data.model_dump())
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def get_application(self, application_id: int) -> Optional[Application]:
        result = await self.db.execute(
            select(Application).where(Application.id == application_id)
        )
        return result.scalar_one_or_none()

    async def get_applications(
        self,
        job_id: Optional[int] = None,
        student_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        query = select(Application)
        
        if job_id is not None:
            query = query.where(Application.job_id == job_id)
        if student_id is not None:
            query = query.where(Application.student_id == student_id)
        if status is not None:
            query = query.where(Application.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_applications_with_details(
        self,
        job_id: Optional[int] = None,
        student_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        query = select(Application).options(
            selectinload(Application.job).selectinload(Job.company)
        )
        
        if job_id is not None:
            query = query.where(Application.job_id == job_id)
        if student_id is not None:
            query = query.where(Application.student_id == student_id)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_application(self, application_id: int, data: ApplicationUpdate) -> Optional[Application]:
        await self.db.execute(
            update(Application).where(Application.id == application_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_application(application_id)

    async def delete_application(self, application_id: int) -> bool:
        application = await self.get_application(application_id)
        if application:
            await self.db.delete(application)
            await self.db.commit()
            return True
        return False

    # Placement Drive operations
    async def create_placement_drive(self, data: PlacementDriveCreate) -> PlacementDrive:
        drive = PlacementDrive(**data.model_dump())
        self.db.add(drive)
        await self.db.commit()
        await self.db.refresh(drive)
        return drive

    async def get_placement_drive(self, drive_id: int) -> Optional[PlacementDrive]:
        result = await self.db.execute(
            select(PlacementDrive).where(PlacementDrive.id == drive_id)
        )
        return result.scalar_one_or_none()

    async def get_placement_drives(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[PlacementDrive]:
        query = select(PlacementDrive)
        
        if is_active is not None:
            query = query.where(PlacementDrive.is_active == is_active)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_placement_drive(self, drive_id: int, data: PlacementDriveUpdate) -> Optional[PlacementDrive]:
        await self.db.execute(
            update(PlacementDrive).where(PlacementDrive.id == drive_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_placement_drive(drive_id)

    async def delete_placement_drive(self, drive_id: int) -> bool:
        drive = await self.get_placement_drive(drive_id)
        if drive:
            await self.db.delete(drive)
            await self.db.commit()
            return True
        return False


__all__ = ["PlacementRepository"]
