# School Parent Service

from typing import Optional, List, Union

from .repository import ParentRepository
from .schemas import ParentCreate, ParentUpdate, ParentResponse
from .models import SchoolParent


class ParentService:
    def __init__(self, db):
        self.repository = ParentRepository(db)

    async def create(self, data: ParentCreate) -> ParentResponse:
        parent = await self.repository.create(data)
        return parent

    async def get(self, parent_id: int) -> Optional[ParentResponse]:
        return await self.repository.get(parent_id)

    async def get_by_user_id(self, user_id: any) -> Optional[ParentResponse]:
        return await self.repository.get_by_user_id(user_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ParentResponse]:
        return await self.repository.get_all(skip, limit)

    async def update(self, parent_id: int, data: ParentUpdate) -> Optional[ParentResponse]:
        return await self.repository.update(parent_id, data)

    async def delete(self, parent_id: int) -> bool:
        return await self.repository.delete(parent_id)


__all__ = ["ParentService"]