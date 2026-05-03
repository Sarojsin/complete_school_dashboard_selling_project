"""
Program Repository

Data access layer for program.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.models.college import Program


class ProgramRepository:
    """Repository for program data access"""
    
    async def get_by_id(self, db: AsyncSession, program_id: int):
        result = await db.execute(select(Program).where(Program.id == program_id))
        return result.scalars().first()
    
    async def get_by_code(self, db: AsyncSession, code: str):
        result = await db.execute(select(Program).where(Program.code == code))
        return result.scalars().first()
    
    async def get_by_department(self, db: AsyncSession, department_id: int, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Program).where(Program.department_id == department_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Program).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def get_count(self, db: AsyncSession):
        result = await db.execute(select(Program))
        return len(result.scalars().all())
    
    async def create(self, db: AsyncSession, program_data: dict):
        program = Program(**program_data)
        db.add(program)
        await db.commit()
        await db.refresh(program)
        return program
    
    async def update(self, db: AsyncSession, program_id: int, program_data: dict):
        program = await self.get_by_id(db, program_id)
        if program:
            for key, value in program_data.items():
                if value is not None:
                    setattr(program, key, value)
            await db.commit()
            await db.refresh(program)
        return program
    
    async def delete(self, db: AsyncSession, program_id: int):
        program = await self.get_by_id(db, program_id)
        if program:
            await db.delete(program)
            await db.commit()
        return program
