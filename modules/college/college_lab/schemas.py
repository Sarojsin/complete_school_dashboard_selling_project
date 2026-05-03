"""
College Lab Schemas

Pydantic schemas for college lab API.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ── Lab Schemas ────────────────────────────────────────────────
class LabBase(BaseModel):
    name: str
    code: str
    department_id: Optional[int] = None
    location: Optional[str] = None
    capacity: Optional[int] = 30
    description: Optional[str] = None
    in_charge_id: Optional[int] = None


class LabCreate(LabBase):
    pass


class LabUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    in_charge_id: Optional[int] = None


class LabResponse(LabBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Equipment Schemas ─────────────────────────────────────────
class EquipmentBase(BaseModel):
    name: str
    serial_number: Optional[str] = None
    quantity: Optional[int] = 1
    status: Optional[str] = "working"
    description: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    lab_id: int


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None


class EquipmentResponse(EquipmentBase):
    id: int
    lab_id: int
    purchase_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Schedule Schemas ───────────────────────────────────────────
class ScheduleBase(BaseModel):
    lab_id: int
    course_id: Optional[int] = None
    day_of_week: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    semester_id: Optional[int] = None


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    day_of_week: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class ScheduleResponse(ScheduleBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)