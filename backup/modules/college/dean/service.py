# College Dean Service

from typing import Optional, List

from backup.modules.college.dean.repository import DeanRepository
from backup.modules.college.dean.schemas import DeanCreate, DeanUpdate, Dean


class DeanService:
    def __init__(self, repository: DeanRepository):
        self.repository = repository

    async def create(self, data: DeanCreate) -> Dean:
        return await self.repository.create(data)

    async def get(self, dean_id: int) -> Optional[Dean]:
        return await self.repository.get(dean_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dean]:
        return await self.repository.get_all(skip, limit)

    async def update(self, dean_id: int, data: DeanUpdate) -> Optional[Dean]:
        return await self.repository.update(dean_id, data)

    async def delete(self, dean_id: int) -> bool:
        return await self.repository.delete(dean_id)


__all__ = ["DeanService"]
