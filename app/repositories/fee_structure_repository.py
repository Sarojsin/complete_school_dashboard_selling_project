from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from app.models.models import FeeStructure

class FeeStructureRepository:
    @staticmethod
    async def get_all(db: AsyncSession) -> List[FeeStructure]:
        result = await db.execute(select(FeeStructure).order_by(FeeStructure.grade_level))
        return result.scalars().all()
    
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[FeeStructure]:
        result = await db.execute(
            select(FeeStructure).filter(
                or_(
                    FeeStructure.grade_level.ilike(f"%{query}%"),
                    FeeStructure.academic_year.ilike(f"%{query}%")
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(db: AsyncSession, structure_id: int) -> Optional[FeeStructure]:
        result = await db.execute(select(FeeStructure).filter(FeeStructure.id == structure_id))
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, data: dict) -> FeeStructure:
        structure = FeeStructure(**data)
        db.add(structure)
        await db.commit()
        await db.refresh(structure)
        return structure
    
    @staticmethod
    async def update(db: AsyncSession, structure: FeeStructure, **kwargs) -> FeeStructure:
        for key, value in kwargs.items():
            if value is not None and hasattr(structure, key):
                setattr(structure, key, value)
        await db.commit()
        await db.refresh(structure)
        return structure
    
    @staticmethod
    async def delete(db: AsyncSession, structure: FeeStructure):
        await db.delete(structure)
        await db.commit()
