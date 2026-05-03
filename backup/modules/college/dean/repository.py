# College Dean Repository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class CollegeDean(Base):
    __tablename__ = "college_deans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(255))
    designation = Column(String(100), default="Dean")
    faculty = Column(String(100))
    phone = Column(String(20))
    joining_date = Column(Date, default=datetime.utcnow)


from backup.modules.college.dean.schemas import DeanCreate, DeanUpdate


class DeanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: DeanCreate) -> CollegeDean:
        dean = CollegeDean(**data.model_dump())
        self.db.add(dean)
        await self.db.commit()
        await self.db.refresh(dean)
        return dean

    async def get(self, dean_id: int) -> Optional[CollegeDean]:
        result = await self.db.execute(select(CollegeDean).where(CollegeDean.id == dean_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CollegeDean]:
        result = await self.db.execute(select(CollegeDean).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, dean_id: int, data: DeanUpdate) -> Optional[CollegeDean]:
        await self.db.execute(
            select(CollegeDean).where(CollegeDean.id == dean_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(dean_id)

    async def delete(self, dean_id: int) -> bool:
        dean = await self.get(dean_id)
        if dean:
            await self.db.delete(dean)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeDean", "DeanRepository"]
