# School Student Repository
# ====================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional, List

from backup.modules.school.student.schemas import StudentCreate, StudentUpdate
from backup.models.school.student import SchoolStudent


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: StudentCreate) -> SchoolStudent:
        student = SchoolStudent(**data.model_dump())
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def get(self, student_id: int) -> Optional[SchoolStudent]:
        result = await self.db.execute(
            select(SchoolStudent).where(SchoolStudent.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[SchoolStudent]:
        result = await self.db.execute(
            select(SchoolStudent).where(SchoolStudent.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        grade_level: Optional[str] = None,
        section: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolStudent]:
        query = select(SchoolStudent)
        if grade_level:
            query = query.where(SchoolStudent.grade_level == grade_level)
        if section:
            query = query.where(SchoolStudent.section == section)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, student_id: int, data: StudentUpdate) -> Optional[SchoolStudent]:
        await self.db.execute(
            update(SchoolStudent).where(SchoolStudent.id == student_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(student_id)

    async def delete(self, student_id: int) -> bool:
        student = await self.get(student_id)
        if student:
            await self.db.delete(student)
            await self.db.commit()
            return True
        return False


__all__ = ["StudentRepository"]
