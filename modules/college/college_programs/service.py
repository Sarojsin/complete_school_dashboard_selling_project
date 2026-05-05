"""
College Program Service
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import ProgramRepository
from .schemas import ProgramResponse


class ProgramService:
    def __init__(self, db: AsyncSession):
        self.repository = ProgramRepository(db)

    async def get_all_programs(self, skip: int = 0, limit: int = 100) -> List[ProgramResponse]:
        programs = await self.repository.get_all(skip, limit)
        return [ProgramResponse.model_validate(p) for p in programs]

    async def get_program(self, program_id: int) -> Optional[ProgramResponse]:
        program = await self.repository.get_by_id(program_id)
        if program:
            return ProgramResponse.model_validate(program)
        return None

    async def get_programs_by_department(self, department_id: int) -> List[ProgramResponse]:
        programs = await self.repository.get_by_department(department_id)
        return [ProgramResponse.model_validate(p) for p in programs]


__all__ = ["ProgramService"]
