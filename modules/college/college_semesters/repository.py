"""
College Semester Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from .models import SemesterModel


class SemesterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SemesterModel]:
        result = await self.db.execute(select(SemesterModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, semester_id: int) -> Optional[SemesterModel]:
        result = await self.db.execute(select(SemesterModel).where(SemesterModel.id == semester_id))
        return result.scalar_one_or_none()

    async def get_current_semester(self) -> Optional[SemesterModel]:
        result = await self.db.execute(
            select(SemesterModel).where(SemesterModel.is_current == True)
        )
        return result.scalar_one_or_none()


__all__ = ["SemesterRepository"]
