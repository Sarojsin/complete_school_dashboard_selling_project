# College HOD Service

from typing import Optional, List

from backup.modules.college.hod.repository import HODRepository
from backup.modules.college.hod.schemas import HODCreate, HODUpdate, HOD


class HODService:
    def __init__(self, repository: HODRepository):
        self.repository = repository

    async def create(self, data: HODCreate) -> HOD:
        return await self.repository.create(data)

    async def get(self, hod_id: int) -> Optional[HOD]:
        return await self.repository.get(hod_id)

    async def get_by_department(self, department_id: int) -> Optional[HOD]:
        return await self.repository.get_by_department(department_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[HOD]:
        return await self.repository.get_all(skip, limit)

    async def update(self, hod_id: int, data: HODUpdate) -> Optional[HOD]:
        return await self.repository.update(hod_id, data)

    async def delete(self, hod_id: int) -> bool:
        return await self.repository.delete(hod_id)


__all__ = ["HODService"]
