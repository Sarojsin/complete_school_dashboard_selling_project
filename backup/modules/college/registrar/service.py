# College Registrar Service

from typing import Optional, List

from backup.modules.college.registrar.repository import RegistrarRepository
from backup.modules.college.registrar.schemas import RegistrarCreate, RegistrarUpdate, Registrar


class RegistrarService:
    def __init__(self, repository: RegistrarRepository):
        self.repository = repository

    async def create(self, data: RegistrarCreate) -> Registrar:
        return await self.repository.create(data)

    async def get(self, registrar_id: int) -> Optional[Registrar]:
        return await self.repository.get(registrar_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Registrar]:
        return await self.repository.get_all(skip, limit)

    async def update(self, registrar_id: int, data: RegistrarUpdate) -> Optional[Registrar]:
        return await self.repository.update(registrar_id, data)

    async def delete(self, registrar_id: int) -> bool:
        return await self.repository.delete(registrar_id)


__all__ = ["RegistrarService"]
