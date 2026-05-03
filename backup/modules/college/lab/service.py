# College Lab Service
# ================

from typing import Dict, Any, List, Optional

from backup.modules.college.lab.repository import LabRepository
from backup.modules.college.lab.schemas import (
    LabCreate,
    LabUpdate,
    LabEquipmentCreate,
    LabEquipmentUpdate,
    LabScheduleCreate,
    LabScheduleUpdate,
)


class LabService:
    def __init__(self, repository: LabRepository):
        self.repository = repository

    # Lab operations
    async def create_lab(self, data: LabCreate) -> Dict[str, Any]:
        lab = await self.repository.create_lab(data)
        return {"lab": lab}

    async def get_lab(self, lab_id: int) -> Optional[Dict[str, Any]]:
        lab = await self.repository.get_lab(lab_id)
        return {"lab": lab} if lab else None

    async def get_labs_by_department(self, department_id: int) -> List[Dict[str, Any]]:
        labs = await self.repository.get_labs_by_department(department_id)
        return [{"lab": lab} for lab in labs]

    async def get_all_labs(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        labs = await self.repository.get_all_labs(skip, limit)
        return [{"lab": lab} for lab in labs]

    async def update_lab(self, lab_id: int, data: LabUpdate) -> Optional[Dict[str, Any]]:
        lab = await self.repository.update_lab(lab_id, data)
        return {"lab": lab} if lab else None

    async def delete_lab(self, lab_id: int) -> bool:
        return await self.repository.delete_lab(lab_id)

    # Equipment operations
    async def create_equipment(self, data: LabEquipmentCreate) -> Dict[str, Any]:
        equipment = await self.repository.create_equipment(data)
        return {"equipment": equipment}

    async def get_equipment(self, equipment_id: int) -> Optional[Dict[str, Any]]:
        equipment = await self.repository.get_equipment(equipment_id)
        return {"equipment": equipment} if equipment else None

    async def get_equipment_by_lab(self, lab_id: int) -> List[Dict[str, Any]]:
        equipment = await self.repository.get_equipment_by_lab(lab_id)
        return [{"equipment": e} for e in equipment]

    async def get_all_equipment(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        equipment = await self.repository.get_all_equipment(skip, limit)
        return [{"equipment": e} for e in equipment]

    async def update_equipment(self, equipment_id: int, data: LabEquipmentUpdate) -> Optional[Dict[str, Any]]:
        equipment = await self.repository.update_equipment(equipment_id, data)
        return {"equipment": equipment} if equipment else None

    async def delete_equipment(self, equipment_id: int) -> bool:
        return await self.repository.delete_equipment(equipment_id)

    # Schedule operations
    async def create_schedule(self, data: LabScheduleCreate) -> Dict[str, Any]:
        schedule = await self.repository.create_schedule(data)
        return {"schedule": schedule}

    async def get_schedule(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        schedule = await self.repository.get_schedule(schedule_id)
        return {"schedule": schedule} if schedule else None

    async def get_schedules_by_lab(self, lab_id: int) -> List[Dict[str, Any]]:
        schedules = await self.repository.get_schedules_by_lab(lab_id)
        return [{"schedule": s} for s in schedules]

    async def get_all_schedules(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        schedules = await self.repository.get_all_schedules(skip, limit)
        return [{"schedule": s} for s in schedules]

    async def update_schedule(self, schedule_id: int, data: LabScheduleUpdate) -> Optional[Dict[str, Any]]:
        schedule = await self.repository.update_schedule(schedule_id, data)
        return {"schedule": schedule} if schedule else None

    async def delete_schedule(self, schedule_id: int) -> bool:
        return await self.repository.delete_schedule(schedule_id)


__all__ = ["LabService"]
