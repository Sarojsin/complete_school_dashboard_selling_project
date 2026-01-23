from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.models import Parent, Student
from app.repositories.student_repository import StudentRepository

class ParentRepository:
    @staticmethod
    async def create(db: AsyncSession, parent_data: dict) -> Parent:
        parent = Parent(**parent_data)
        db.add(parent)
        await db.commit()
        await db.refresh(parent)
        return parent
    
    @staticmethod
    async def get_by_id(db: AsyncSession, parent_id: int) -> Optional[Parent]:
        result = await db.execute(select(Parent).filter(Parent.id == parent_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> Optional[Parent]:
        result = await db.execute(select(Parent).filter(Parent.user_id == user_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_children(db: AsyncSession, parent_id: int) -> List[Student]:
        """Get all children of a parent"""
        result = await db.execute(select(Student).filter(Student.parent_id == parent_id))
        return result.scalars().all()
    
    @staticmethod
    async def link_child(db: AsyncSession, parent_id: int, student_id: int):
        """Link a child to a parent"""
        student = await StudentRepository.get_by_id(db, student_id)
        if student:
            student.parent_id = parent_id
            await db.commit()
            await db.refresh(student)
        return student
    
    @staticmethod
    async def update(db: AsyncSession, parent: Parent, **kwargs) -> Parent:
        for key, value in kwargs.items():
            if value is not None and hasattr(parent, key):
                setattr(parent, key, value)
        await db.commit()
        await db.refresh(parent)
        return parent
    
    @staticmethod
    async def delete(db: AsyncSession, parent: Parent):
        await db.delete(parent)
        await db.commit()
