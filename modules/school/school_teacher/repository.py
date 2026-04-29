# School Teacher Repository
# ========================
# Database operations for school teacher module

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional, List
from .models import Teacher
from .schemas import TeacherCreate, TeacherUpdate


class TeacherRepository:
    """Repository for school teacher database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create(self, data: TeacherCreate) -> Teacher:
        """Create a new teacher"""
        teacher = Teacher(**data.model_dump())
        self.db.add(teacher)
        await self.db.commit()
        await self.db.refresh(teacher)
        return teacher
        
    async def get(self, teacher_id: int) -> Optional[Teacher]:
        """Get teacher by ID"""
        result = await self.db.execute(
            select(Teacher).where(Teacher.id == teacher_id)
        )
        return result.scalar_one_or_none()
        
    async def get_by_user_id(self, user_id: int) -> Optional[Teacher]:
        """Get teacher by user ID"""
        result = await self.db.execute(
            select(Teacher).where(Teacher.user_id == user_id)
        )
        return result.scalar_one_or_none()
        
    async def get_by_employee_id(self, employee_id: str) -> Optional[Teacher]:
        """Get teacher by employee ID"""
        result = await self.db.execute(
            select(Teacher).where(Teacher.employee_id == employee_id)
        )
        return result.scalar_one_or_none()
        
    async def get_all(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Teacher]:
        """Get all teachers with optional filtering"""
        query = select(Teacher)
        
        if department is not None:
            query = query.where(Teacher.department == department)
        if status is not None:
            query = query.where(Teacher.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
        
    async def update(self, teacher_id: int, data: TeacherUpdate) -> Optional[Teacher]:
        """Update teacher"""
        await self.db.execute(
            update(Teacher).where(Teacher.id == teacher_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(teacher_id)
        
    async def delete(self, teacher_id: int) -> bool:
        """Delete teacher"""
        teacher = await self.get(teacher_id)
        if teacher:
            await self.db.delete(teacher)
            await self.db.commit()
            return True
        return False


__all__ = ["TeacherRepository"]
