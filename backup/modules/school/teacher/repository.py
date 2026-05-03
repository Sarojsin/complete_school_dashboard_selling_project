# School Teacher Repository
# ========================
# Database operations for school teacher module

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List

from backup.modules.school.teacher.schemas import TeacherCreate, TeacherUpdate
from backup.models.school.teacher import SchoolTeacher


class TeacherRepository:
    """Repository for school teacher database operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: TeacherCreate) -> SchoolTeacher:
        teacher = SchoolTeacher(**data.model_dump())
        self.db.add(teacher)
        await self.db.commit()
        await self.db.refresh(teacher)
        return teacher

    async def get(self, teacher_id: int) -> Optional[SchoolTeacher]:
        result = await self.db.execute(
            select(SchoolTeacher).where(SchoolTeacher.id == teacher_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[SchoolTeacher]:
        result = await self.db.execute(
            select(SchoolTeacher).where(SchoolTeacher.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_employee_id(self, employee_id: str) -> Optional[SchoolTeacher]:
        result = await self.db.execute(
            select(SchoolTeacher).where(SchoolTeacher.employee_id == employee_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolTeacher]:
        query = select(SchoolTeacher)
        
        if department is not None:
            query = query.where(SchoolTeacher.department == department)
        if status is not None:
            query = query.where(SchoolTeacher.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, teacher_id: int, data: TeacherUpdate) -> Optional[SchoolTeacher]:
        await self.db.execute(
            update(SchoolTeacher).where(SchoolTeacher.id == teacher_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(teacher_id)

    async def delete(self, teacher_id: int) -> bool:
        teacher = await self.get(teacher_id)
        if teacher:
            await self.db.delete(teacher)
            await self.db.commit()
            return True
        return False


__all__ = ["TeacherRepository"]
