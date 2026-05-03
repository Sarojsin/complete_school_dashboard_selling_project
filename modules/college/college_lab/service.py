"""
College Lab Service

Business logic for college lab operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import LabRepository, EquipmentRepository, ScheduleRepository
from .models import Lab, LabEquipment, LabSchedule
from .schemas import LabCreate, LabUpdate, EquipmentCreate, EquipmentUpdate, ScheduleCreate, ScheduleUpdate


class LabService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lab_repo = LabRepository(db)
        self.equip_repo = EquipmentRepository(db)
        self.schedule_repo = ScheduleRepository(db)
    
    # ── Lab Methods ─────────────────────────────────────────────
    async def create_lab(self, data: LabCreate) -> Lab:
        lab = Lab(**data.model_dump())
        return await self.lab_repo.create(lab)
    
    async def get_lab(self, lab_id: int) -> Optional[Lab]:
        return await self.lab_repo.get_by_id(lab_id)
    
    async def list_labs(self, skip: int = 0, limit: int = 100) -> List[Lab]:
        return await self.lab_repo.list(skip, limit)
    
    async def list_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Lab]:
        return await self.lab_repo.list_by_department(department_id, skip, limit)
    
    async def update_lab(self, lab_id: int, data: LabUpdate) -> Optional[Lab]:
        lab = await self.lab_repo.get_by_id(lab_id)
        if not lab:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(lab, key, value)
        return await self.lab_repo.update(lab)
    
    async def delete_lab(self, lab_id: int) -> bool:
        return await self.lab_repo.delete(lab_id)
    
    # ── Equipment Methods ──────────────────────────────────────
    async def add_equipment(self, data: EquipmentCreate) -> LabEquipment:
        equipment = LabEquipment(**data.model_dump())
        return await self.equip_repo.create(equipment)
    
    async def get_equipment(self, equipment_id: int) -> Optional[LabEquipment]:
        return await self.equip_repo.get_by_id(equipment_id)
    
    async def list_equipment(self, lab_id: int, skip: int = 0, limit: int = 100) -> List[LabEquipment]:
        return await self.equip_repo.list_by_lab(lab_id, skip, limit)
    
    async def update_equipment(self, equipment_id: int, data: EquipmentUpdate) -> Optional[LabEquipment]:
        equipment = await self.equip_repo.get_by_id(equipment_id)
        if not equipment:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(equipment, key, value)
        return await self.equip_repo.update(equipment)
    
    # ── Schedule Methods ───────────────────────────────────────
    async def create_schedule(self, data: ScheduleCreate) -> LabSchedule:
        schedule = LabSchedule(**data.model_dump())
        return await self.schedule_repo.create(schedule)
    
    async def get_schedule(self, schedule_id: int) -> Optional[LabSchedule]:
        return await self.schedule_repo.get_by_id(schedule_id)
    
    async def list_schedules(self, lab_id: int, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        return await self.schedule_repo.list_by_lab(lab_id, skip, limit)
    
    async def list_schedules_by_course(self, course_id: int, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        return await self.schedule_repo.list_by_course(course_id, skip, limit)
    
    async def update_schedule(self, schedule_id: int, data: ScheduleUpdate) -> Optional[LabSchedule]:
        schedule = await self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(schedule, key, value)
        return await self.schedule_repo.update(schedule)