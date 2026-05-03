# School Parent Repository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from backup.modules.school.parent.schemas import ParentCreate, ParentUpdate
from backup.models.school.parent import SchoolParent


class ParentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ParentCreate) -> SchoolParent:
        parent = SchoolParent(**data.model_dump())
        self.db.add(parent)
        await self.db.commit()
        await self.db.refresh(parent)
        return parent

    async def get(self, parent_id: int) -> Optional[SchoolParent]:
        result = await self.db.execute(select(SchoolParent).where(SchoolParent.id == parent_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[SchoolParent]:
        result = await self.db.execute(select(SchoolParent).where(SchoolParent.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SchoolParent]:
        result = await self.db.execute(select(SchoolParent).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, parent_id: int, data: ParentUpdate) -> Optional[SchoolParent]:
        await self.db.execute(
            select(SchoolParent).where(SchoolParent.id == parent_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(parent_id)

    async def delete(self, parent_id: int) -> bool:
        parent = await self.get(parent_id)
        if parent:
            await self.db.delete(parent)
            await self.db.commit()
            return True
        return False


__all__ = ["ParentRepository"]
