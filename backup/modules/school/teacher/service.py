# School Teacher Service
# ====================
# Business logic for school teacher module

from typing import Optional, List

from backup.modules.school.teacher.repository import TeacherRepository
from backup.modules.school.teacher.schemas import TeacherCreate, TeacherUpdate, Teacher


class TeacherService:
    """Service layer for school teacher operations"""

    def __init__(self, repository: TeacherRepository):
        self.repository = repository

    async def create(self, data: TeacherCreate) -> Teacher:
        # Check if employee_id already exists
        existing = await self.repository.get_by_employee_id(data.employee_id)
        if existing:
            raise ValueError("Employee ID already exists")
        
        # Check if user already has teacher profile
        existing_user = await self.repository.get_by_user_id(data.user_id)
        if existing_user:
            raise ValueError("User already has teacher profile")
        
        return await self.repository.create(data)

    async def get(self, teacher_id: int) -> Optional[Teacher]:
        return await self.repository.get(teacher_id)

    async def get_by_user_id(self, user_id: int) -> Optional[Teacher]:
        return await self.repository.get_by_user_id(user_id)

    async def get_all(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Teacher]:
        return await self.repository.get_all(department, status, skip, limit)

    async def get_active_teachers(
        self,
        department: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Teacher]:
        return await self.repository.get_all(department, status="active", skip=skip, limit=limit)

    async def update(self, teacher_id: int, data: TeacherUpdate) -> Optional[Teacher]:
        return await self.repository.update(teacher_id, data)

    async def delete(self, teacher_id: int) -> bool:
        return await self.repository.delete(teacher_id)

    async def deactivate(self, teacher_id: int) -> Optional[Teacher]:
        return await self.repository.update(teacher_id, TeacherUpdate(status="inactive"))


__all__ = ["TeacherService"]
