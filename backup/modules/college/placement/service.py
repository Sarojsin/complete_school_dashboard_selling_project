# College Placement Service
# =========================
# Business logic for placement module

from typing import Optional, List
from datetime import date

from backup.modules.college.placement.repository import PlacementRepository
from backup.modules.college.placement.schemas import (
    CompanyCreate,
    CompanyUpdate,
    Company,
    JobCreate,
    JobUpdate,
    Job,
    JobWithCompany,
    ApplicationCreate,
    ApplicationUpdate,
    Application,
    ApplicationWithDetails,
    PlacementDriveCreate,
    PlacementDriveUpdate,
    PlacementDrive,
)


class PlacementService:
    """Service layer for placement operations"""

    def __init__(self, repository: PlacementRepository):
        self.repository = repository

    # Company operations
    async def create_company(self, data: CompanyCreate) -> Company:
        return await self.repository.create_company(data)

    async def get_company(self, company_id: int) -> Optional[Company]:
        return await self.repository.get_company(company_id)

    async def get_companies(self, skip: int = 0, limit: int = 100) -> List[Company]:
        return await self.repository.get_companies(skip, limit)

    async def update_company(self, company_id: int, data: CompanyUpdate) -> Optional[Company]:
        return await self.repository.update_company(company_id, data)

    async def delete_company(self, company_id: int) -> bool:
        return await self.repository.delete_company(company_id)

    # Job operations
    async def create_job(self, data: JobCreate) -> Job:
        return await self.repository.create_job(data)

    async def get_job(self, job_id: int) -> Optional[Job]:
        return await self.repository.get_job(job_id)

    async def get_jobs(
        self,
        company_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Job]:
        return await self.repository.get_jobs(company_id, is_active, skip, limit)

    async def get_active_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        return await self.repository.get_jobs(is_active=True, skip=skip, limit=limit)

    async def update_job(self, job_id: int, data: JobUpdate) -> Optional[Job]:
        return await self.repository.update_job(job_id, data)

    async def delete_job(self, job_id: int) -> bool:
        return await self.repository.delete_job(job_id)

    # Application operations
    async def create_application(self, data: ApplicationCreate) -> Application:
        # Check if already applied
        existing = await self.repository.get_applications(
            job_id=data.job_id,
            student_id=data.student_id
        )
        if existing:
            raise ValueError("Already applied to this job")
        return await self.repository.create_application(data)

    async def get_application(self, application_id: int) -> Optional[Application]:
        return await self.repository.get_application(application_id)

    async def get_applications(
        self,
        job_id: Optional[int] = None,
        student_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        return await self.repository.get_applications(job_id, student_id, status, skip, limit)

    async def get_applications_with_details(
        self,
        job_id: Optional[int] = None,
        student_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ApplicationWithDetails]:
        applications = await self.repository.get_applications_with_details(
            job_id, student_id, skip, limit
        )
        # Convert to response schema
        result = []
        for app in applications:
            result.append(ApplicationWithDetails(
                id=app.id,
                job_id=app.job_id,
                student_id=app.student_id,
                applied_date=app.applied_date,
                status=app.status,
                resume=app.resume,
                cover_letter=app.cover_letter,
                notes=app.notes,
                job=JobWithCompany(
                    id=app.job.id,
                    company_id=app.job.company_id,
                    title=app.job.title,
                    description=app.job.description,
                    requirements=app.job.requirements,
                    salary_min=app.job.salary_min,
                    salary_max=app.job.salary_max,
                    location=app.job.location,
                    job_type=app.job.job_type,
                    deadline=app.job.deadline,
                    is_active=app.job.is_active,
                    created_at=app.job.created_at,
                    company=Company(
                        id=app.job.company.id,
                        name=app.job.company.name,
                        industry=app.job.company.industry,
                        website=app.job.company.website,
                        description=app.job.company.description,
                        logo=app.job.company.logo,
                        created_at=app.job.company.created_at
                    )
                )
            ))
        return result

    async def update_application(self, application_id: int, data: ApplicationUpdate) -> Optional[Application]:
        return await self.repository.update_application(application_id, data)

    async def update_application_status(self, application_id: int, status: str) -> Optional[Application]:
        return await self.repository.update_application(
            application_id, 
            ApplicationUpdate(status=status)
        )

    async def delete_application(self, application_id: int) -> bool:
        return await self.repository.delete_application(application_id)

    # Placement Drive operations
    async def create_placement_drive(self, data: PlacementDriveCreate) -> PlacementDrive:
        return await self.repository.create_placement_drive(data)

    async def get_placement_drive(self, drive_id: int) -> Optional[PlacementDrive]:
        return await self.repository.get_placement_drive(drive_id)

    async def get_placement_drives(
        self,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[PlacementDrive]:
        return await self.repository.get_placement_drives(is_active, skip, limit)

    async def get_active_placement_drives(self, skip: int = 0, limit: int = 100) -> List[PlacementDrive]:
        return await self.repository.get_placement_drives(is_active=True, skip=skip, limit=limit)

    async def update_placement_drive(self, drive_id: int, data: PlacementDriveUpdate) -> Optional[PlacementDrive]:
        return await self.repository.update_placement_drive(drive_id, data)

    async def delete_placement_drive(self, drive_id: int) -> bool:
        return await self.repository.delete_placement_drive(drive_id)


__all__ = ["PlacementService"]
