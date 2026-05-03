# College Lab Repository
# ==================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean

# Import models from app.models
from backup.models.college.lab import Lab, LabEquipment, LabSchedule


from backup.modules.college.lab.schemas import (
    LabCreate,
    LabUpdate,
    LabEquipmentCreate,
    LabEquipmentUpdate,
    LabScheduleCreate,
    LabScheduleUpdate,
)


class LabRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Lab methods
    async def create_lab(self, data: LabCreate) -> Lab:
        lab = Lab(**data.model_dump())
        self.db.add(lab)
        await self.db.commit()
        await self.db.refresh(lab)
        return lab

    async def get_lab(self, lab_id: int) -> Optional[Lab]:
        result = await self.db.execute(select(Lab).where(Lab.id == lab_id))
        return result.scalar_one_or_none()

    async def get_labs_by_department(self, department_id: int) -> List[Lab]:
        result = await self.db.execute(select(Lab).where(Lab.department_id == department_id))
        return list(result.scalars().all())

    async def get_all_labs(self, skip: int = 0, limit: int = 100) -> List[Lab]:
        result = await self.db.execute(select(Lab).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_lab(self, lab_id: int, data: LabUpdate) -> Optional[Lab]:
        await self.db.execute(
            select(Lab).where(Lab.id == lab_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_lab(lab_id)

    async def delete_lab(self, lab_id: int) -> bool:
        lab = await self.get_lab(lab_id)
        if lab:
            await self.db.delete(lab)
            await self.db.commit()
            return True
        return False

    # Equipment methods
    async def create_equipment(self, data: LabEquipmentCreate) -> LabEquipment:
        equipment = LabEquipment(**data.model_dump())
        self.db.add(equipment)
        await self.db.commit()
        await self.db.refresh(equipment)
        return equipment

    async def get_equipment(self, equipment_id: int) -> Optional[LabEquipment]:
        result = await self.db.execute(select(LabEquipment).where(LabEquipment.id == equipment_id))
        return result.scalar_one_or_none()

    async def get_equipment_by_lab(self, lab_id: int) -> List[LabEquipment]:
        result = await self.db.execute(select(LabEquipment).where(LabEquipment.lab_id == lab_id))
        return list(result.scalars().all())

    async def get_all_equipment(self, skip: int = 0, limit: int = 100) -> List[LabEquipment]:
        result = await self.db.execute(select(LabEquipment).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_equipment(self, equipment_id: int, data: LabEquipmentUpdate) -> Optional[LabEquipment]:
        await self.db.execute(
            select(LabEquipment).where(LabEquipment.id == equipment_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_equipment(equipment_id)

    async def delete_equipment(self, equipment_id: int) -> bool:
        equipment = await self.get_equipment(equipment_id)
        if equipment:
            await self.db.delete(equipment)
            await self.db.commit()
            return True
        return False

    # Schedule methods
    async def create_schedule(self, data: LabScheduleCreate) -> LabSchedule:
        schedule = LabSchedule(**data.model_dump())
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def get_schedule(self, schedule_id: int) -> Optional[LabSchedule]:
        result = await self.db.execute(select(LabSchedule).where(LabSchedule.id == schedule_id))
        return result.scalar_one_or_none()

    async def get_schedules_by_lab(self, lab_id: int) -> List[LabSchedule]:
        result = await self.db.execute(select(LabSchedule).where(LabSchedule.lab_id == lab_id))
        return list(result.scalars().all())

    async def get_all_schedules(self, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        result = await self.db.execute(select(LabSchedule).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_schedule(self, schedule_id: int, data: LabScheduleUpdate) -> Optional[LabSchedule]:
        await self.db.execute(
            select(LabSchedule).where(LabSchedule.id == schedule_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_schedule(schedule_id)

    async def delete_schedule(self, schedule_id: int) -> bool:
        schedule = await self.get_schedule(schedule_id)
        if schedule:
            await self.db.delete(schedule)
            await self.db.commit()
            return True
        return False


__all__ = ["LabRepository"]
