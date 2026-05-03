# School Parent Service

from typing import Optional, List

from backup.modules.school.parent.repository import ParentRepository
from backup.modules.school.parent.schemas import ParentCreate, ParentUpdate, Parent


class ParentService:
    def __init__(self, repository: ParentRepository):
        self.repository = repository

    async def create(self, data: ParentCreate) -> Parent:
        return await self.repository.create(data)

    async def get(self, parent_id: int) -> Optional[Parent]:
        return await self.repository.get(parent_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Parent]:
        return await self.repository.get_all(skip, limit)

    async def update(self, parent_id: int, data: ParentUpdate) -> Optional[Parent]:
        return await self.repository.update(parent_id, data)

    async def delete(self, parent_id: int) -> bool:
        return await self.repository.delete(parent_id)


__all__ = ["ParentService"]
