# College Lab Schemas
# =================

from pydantic import BaseModel
from typing import Optional
from datetime import date


class LabBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    department_id: int
    capacity: int = 30
    location: Optional[str] = None


class LabCreate(LabBase):
    pass


class LabUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class Lab(LabBase):
    id: int
    equipment_count: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class LabEquipmentBase(BaseModel):
    lab_id: int
    name: str
    serial_number: Optional[str] = None
    quantity: int = 1
    purchase_date: Optional[date] = None
    condition: str = "good"
    notes: Optional[str] = None


class LabEquipmentCreate(LabEquipmentBase):
    pass


class LabEquipmentUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    condition: Optional[str] = None
    notes: Optional[str] = None


class LabEquipment(LabEquipmentBase):
    id: int

    class Config:
        from_attributes = True


class LabScheduleBase(BaseModel):
    lab_id: int
    course_id: Optional[int] = None
    faculty_id: Optional[int] = None
    day_of_week: str
    start_time: str
    end_time: str
    semester_id: Optional[int] = None


class LabScheduleCreate(LabScheduleBase):
    pass


class LabScheduleUpdate(BaseModel):
    course_id: Optional[int] = None
    faculty_id: Optional[int] = None
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_active: Optional[bool] = None


class LabSchedule(LabScheduleBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


__all__ = [
    "LabBase",
    "LabCreate",
    "LabUpdate",
    "Lab",
    "LabEquipmentBase",
    "LabEquipmentCreate",
    "LabEquipmentUpdate",
    "LabEquipment",
    "LabScheduleBase",
    "LabScheduleCreate",
    "LabScheduleUpdate",
    "LabSchedule",
]
