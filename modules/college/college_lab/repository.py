"""
College Lab Repository

Async CRUD operations for college lab management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import Lab, LabEquipment, LabSchedule


# ── Lab Repository ─────────────────────────────────────────────
class LabRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, lab_id: int) -> Optional[Lab]:
        result = await self.db.execute(select(Lab).filter(Lab.id == lab_id))
        return result.scalars().first()
    
    async def get_by_code(self, code: str) -> Optional[Lab]:
        result = await self.db.execute(select(Lab).filter(Lab.code == code))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Lab]:
        result = await self.db.execute(select(Lab).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def list_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Lab]:
        result = await self.db.execute(
            select(Lab).filter(Lab.department_id == department_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, lab: Lab) -> Lab:
        self.db.add(lab)
        await self.db.commit()
        await self.db.refresh(lab)
        return lab
    
    async def update(self, lab: Lab) -> Lab:
        await self.db.commit()
        await self.db.refresh(lab)
        return lab
    
    async def delete(self, lab_id: int) -> bool:
        lab = await self.get_by_id(lab_id)
        if lab:
            await self.db.delete(lab)
            await self.db.commit()
            return True
        return False


# ── Equipment Repository ──────────────────────────────────────
class EquipmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, equipment_id: int) -> Optional[LabEquipment]:
        result = await self.db.execute(select(LabEquipment).filter(LabEquipment.id == equipment_id))
        return result.scalars().first()
    
    async def list_by_lab(self, lab_id: int, skip: int = 0, limit: int = 100) -> List[LabEquipment]:
        result = await self.db.execute(
            select(LabEquipment).filter(LabEquipment.lab_id == lab_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, equipment: LabEquipment) -> LabEquipment:
        self.db.add(equipment)
        await self.db.commit()
        await self.db.refresh(equipment)
        return equipment
    
    async def update(self, equipment: LabEquipment) -> LabEquipment:
        await self.db.commit()
        await self.db.refresh(equipment)
        return equipment
    
    async def delete(self, equipment_id: int) -> bool:
        equipment = await self.get_by_id(equipment_id)
        if equipment:
            await self.db.delete(equipment)
            await self.db.commit()
            return True
        return False


# ── Schedule Repository ────────────────────────────────────────
class ScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, schedule_id: int) -> Optional[LabSchedule]:
        result = await self.db.execute(select(LabSchedule).filter(LabSchedule.id == schedule_id))
        return result.scalars().first()
    
    async def list_by_lab(self, lab_id: int, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        result = await self.db.execute(
            select(LabSchedule).filter(LabSchedule.lab_id == lab_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_course(self, course_id: int, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        result = await self.db.execute(
            select(LabSchedule).filter(LabSchedule.course_id == course_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, schedule: LabSchedule) -> LabSchedule:
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule
    
    async def update(self, schedule: LabSchedule) -> LabSchedule:
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule
    
    async def delete(self, schedule_id: int) -> bool:
        schedule = await self.get_by_id(schedule_id)
        if schedule:
            await self.db.delete(schedule)
            await self.db.commit()
            return True
        return False