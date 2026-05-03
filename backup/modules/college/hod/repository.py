# College HOD Repository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class CollegeHOD(Base):
    __tablename__ = "college_hods"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    full_name = Column(String(255))
    designation = Column(String(100), default="HOD")
    qualification = Column(String(255))
    phone = Column(String(20))
    joining_date = Column(Date, default=datetime.utcnow)


from backup.modules.college.hod.schemas import HODCreate, HODUpdate


class HODRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: HODCreate) -> CollegeHOD:
        hod = CollegeHOD(**data.model_dump())
        self.db.add(hod)
        await self.db.commit()
        await self.db.refresh(hod)
        return hod

    async def get(self, hod_id: int) -> Optional[CollegeHOD]:
        result = await self.db.execute(select(CollegeHOD).where(CollegeHOD.id == hod_id))
        return result.scalar_one_or_none()

    async def get_by_department(self, department_id: int) -> Optional[CollegeHOD]:
        result = await self.db.execute(select(CollegeHOD).where(CollegeHOD.department_id == department_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CollegeHOD]:
        result = await self.db.execute(select(CollegeHOD).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, hod_id: int, data: HODUpdate) -> Optional[CollegeHOD]:
        await self.db.execute(
            select(CollegeHOD).where(CollegeHOD.id == hod_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(hod_id)

    async def delete(self, hod_id: int) -> bool:
        hod = await self.get(hod_id)
        if hod:
            await self.db.delete(hod)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeHOD", "HODRepository"]
