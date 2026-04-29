# School Teacher Service
# ====================
# Business logic for school teacher module

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import TeacherRepository
from .schemas import TeacherCreate, TeacherUpdate
from .models import Teacher


class TeacherService:
    """Service layer for school teacher operations"""
    
    def __init__(self, db: AsyncSession):
        self.repository = TeacherRepository(db)
        
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
        return await self.repository.update(teacher_id, TeacherUpdate(status="inactive", employee_id=None))
    
    # Keep legacy methods for backward compatibility
    async def get_teacher(self, teacher_id: int) -> Optional[Teacher]:
        return await self.get(teacher_id)
    
    async def get_my_profile(self, user_id: int) -> Optional[Teacher]:
        return await self.get_by_user_id(user_id)
    
    async def list_teachers(self, skip: int = 0, limit: int = 100) -> List[Teacher]:
        return await self.get_all(skip=skip, limit=limit)


__all__ = ["TeacherService"]
