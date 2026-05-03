# College Registrar Repository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class CollegeRegistrar(Base):
    __tablename__ = "college_registrars"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(255))
    designation = Column(String(100), default="Registrar")
    phone = Column(String(20))
    joining_date = Column(Date, default=datetime.utcnow)


from backup.modules.college.registrar.schemas import RegistrarCreate, RegistrarUpdate


class RegistrarRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: RegistrarCreate) -> CollegeRegistrar:
        registrar = CollegeRegistrar(**data.model_dump())
        self.db.add(registrar)
        await self.db.commit()
        await self.db.refresh(registrar)
        return registrar

    async def get(self, registrar_id: int) -> Optional[CollegeRegistrar]:
        result = await self.db.execute(select(CollegeRegistrar).where(CollegeRegistrar.id == registrar_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CollegeRegistrar]:
        result = await self.db.execute(select(CollegeRegistrar).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, registrar_id: int, data: RegistrarUpdate) -> Optional[CollegeRegistrar]:
        await self.db.execute(
            select(CollegeRegistrar).where(CollegeRegistrar.id == registrar_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(registrar_id)

    async def delete(self, registrar_id: int) -> bool:
        registrar = await self.get(registrar_id)
        if registrar:
            await self.db.delete(registrar)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeRegistrar", "RegistrarRepository"]
