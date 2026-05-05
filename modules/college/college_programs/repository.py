"""
College Program Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from .models import ProgramModel


class ProgramRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProgramModel]:
        result = await self.db.execute(select(ProgramModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, program_id: int) -> Optional[ProgramModel]:
        result = await self.db.execute(select(ProgramModel).where(ProgramModel.id == program_id))
        return result.scalar_one_or_none()

    async def get_by_department(self, department_id: int) -> List[ProgramModel]:
        result = await self.db.execute(
            select(ProgramModel).where(ProgramModel.department_id == department_id)
        )
        return list(result.scalars().all())


__all__ = ["ProgramRepository"]
