"""
College Dean Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from .models import Department, Program, Faculty, CollegeStudent


class DeanRepository:
    """Repository for dean-level aggregated queries"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_departments(self) -> int:
        result = await self.db.execute(select(func.count(Department.id)))
        return result.scalar() or 0

    async def count_programs(self) -> int:
        result = await self.db.execute(select(func.count(Program.id)))
        return result.scalar() or 0

    async def count_faculty(self) -> int:
        result = await self.db.execute(select(func.count(Faculty.id)))
        return result.scalar() or 0

    async def count_students(self) -> int:
        result = await self.db.execute(select(func.count(CollegeStudent.id)))
        return result.scalar() or 0

    async def list_departments(self, skip: int = 0, limit: int = 100) -> List[Department]:
        result = await self.db.execute(select(Department).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def list_programs(self, department_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Program]:
        query = select(Program)
        if department_id is not None:
            query = query.where(Program.department_id == department_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_faculty(self, department_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Faculty]:
        query = select(Faculty)
        if department_id is not None:
            query = query.where(Faculty.department_id == department_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_students(self, program_id: Optional[int] = None, semester: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[CollegeStudent]:
        query = select(CollegeStudent)
        if program_id is not None:
            query = query.where(CollegeStudent.program_id == program_id)
        if semester is not None:
            query = query.where(CollegeStudent.semester_id == semester)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())


__all__ = ["DeanRepository"]
