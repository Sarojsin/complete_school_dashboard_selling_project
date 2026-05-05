"""
College Semester Service
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import SemesterRepository
from .schemas import SemesterResponse


class SemesterService:
    def __init__(self, db: AsyncSession):
        self.repository = SemesterRepository(db)

    async def get_all_semesters(self, skip: int = 0, limit: int = 100) -> List[SemesterResponse]:
        semesters = await self.repository.get_all(skip, limit)
        return [SemesterResponse.model_validate(s) for s in semesters]

    async def get_semester(self, semester_id: int) -> Optional[SemesterResponse]:
        semester = await self.repository.get_by_id(semester_id)
        if semester:
            return SemesterResponse.model_validate(semester)
        return None

    async def get_current_semester(self) -> Optional[SemesterResponse]:
        semester = await self.repository.get_current_semester()
        if semester:
            return SemesterResponse.model_validate(semester)
        return None


__all__ = ["SemesterService"]
