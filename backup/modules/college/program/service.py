"""
Program Service

Business logic layer for program.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backup.modules.college.program.repository import ProgramRepository
from backup.modules.college.program.schemas import ProgramCreate, ProgramUpdate


class ProgramService:
    def __init__(self):
        self.repo = ProgramRepository()
    
    async def get_program(self, db: AsyncSession, program_id: int):
        return await self.repo.get_by_id(db, program_id)
    
    async def list_programs(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        programs = await self.repo.get_all(db, skip, limit)
        total = await self.repo.get_count(db)
        return {"programs": programs, "total": total}
    
    async def list_programs_by_department(self, db: AsyncSession, department_id: int, skip: int = 0, limit: int = 100):
        return await self.repo.get_by_department(db, department_id, skip, limit)
    
    async def create_program(self, db: AsyncSession, program_data: ProgramCreate):
        existing = await self.repo.get_by_code(db, program_data.code)
        if existing:
            raise ValueError("Program code already exists")
        return await self.repo.create(db, program_data.model_dump())
    
    async def update_program(self, db: AsyncSession, program_id: int, program_data: ProgramUpdate):
        update_data = program_data.model_dump(exclude_unset=True)
        return await self.repo.update(db, program_id, update_data)
    
    async def delete_program(self, db: AsyncSession, program_id: int):
        return await self.repo.delete(db, program_id)
