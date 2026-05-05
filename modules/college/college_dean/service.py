"""
College Dean Service

Business logic for dean oversight and analytics.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import DeanRepository
from .schemas import (
    DeanDashboardResponse,
    DepartmentListSchema,
    ProgramListSchema,
    FacultySummarySchema,
    StudentSummarySchema
)
from modules.shared.exceptions import ForbiddenError


class DeanService:
    """Service for dean operations"""

    def __init__(self, db: AsyncSession):
        self.repository = DeanRepository(db)

    async def get_dashboard(self) -> DeanDashboardResponse:
        """Get dean dashboard aggregate stats"""
        return DeanDashboardResponse(
            departments=await self.repository.count_departments(),
            programs=await self.repository.count_programs(),
            faculty=await self.repository.count_faculty(),
            students=await self.repository.count_students()
        )

    async def get_departments(self, skip: int = 0, limit: int = 100) -> List[DepartmentListSchema]:
        depts = await self.repository.list_departments(skip, limit)
        return [DepartmentListSchema.model_validate(d) for d in depts]

    async def get_department_detail(self, dept_id: int) -> DepartmentListSchema:
        dept = await self.repository.list_departments(limit=1)
        # Simplified
        return DepartmentListSchema.model_validate(dept)

    async def get_programs(self, department_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[ProgramListSchema]:
        programs = await self.repository.list_programs(department_id, skip, limit)
        return [ProgramListSchema.model_validate(p) for p in programs]

    async def get_faculty(self, department_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[FacultySummarySchema]:
        faculty = await self.repository.list_faculty(department_id, skip, limit)
        return [FacultySummarySchema.model_validate(f) for f in faculty]

    async def get_students(self, program_id: Optional[int] = None, semester: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[StudentSummarySchema]:
        students = await self.repository.list_students(program_id, semester, skip, limit)
        return [StudentSummarySchema.model_validate(s) for s in students]


__all__ = ["DeanService"]
