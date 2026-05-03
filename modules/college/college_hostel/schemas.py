"""
College Hostel Schemas

Pydantic schemas for college hostel API.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ── Hostel Schemas ─────────────────────────────────────────────
class HostelBase(BaseModel):
    name: str
    capacity: Optional[int] = 0
    warden_id: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None


class HostelCreate(HostelBase):
    pass


class HostelUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    warden_id: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None


class HostelResponse(HostelBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Room Schemas ────────────────────────────────────────────────
class RoomBase(BaseModel):
    hostel_id: int
    room_number: str
    floor: Optional[int] = 1
    capacity: Optional[int] = 2
    room_type: Optional[str] = None
    amenities: Optional[str] = None
    is_available: Optional[bool] = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    floor: Optional[int] = None
    capacity: Optional[int] = None
    room_type: Optional[str] = None
    amenities: Optional[str] = None
    is_available: Optional[bool] = None


class RoomResponse(RoomBase):
    id: int
    occupied: Optional[int] = 0
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Allocation Schemas ─────────────────────────────────────────
class AllocationBase(BaseModel):
    student_id: int
    room_id: int


class AllocationCreate(AllocationBase):
    pass


class AllocationResponse(AllocationBase):
    id: int
    allocation_date: Optional[datetime] = None
    vacate_date: Optional[datetime] = None
    status: Optional[str] = "active"
    
    model_config = ConfigDict(from_attributes=True)


# ── Complaint Schemas ───────────────────────────────────────────
class ComplaintBase(BaseModel):
    subject: str
    description: str
    category: Optional[str] = None
    hostel_id: Optional[int] = None
    room_id: Optional[int] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolved_by: Optional[int] = None


class ComplaintResponse(ComplaintBase):
    id: int
    student_id: int
    status: Optional[str] = "pending"
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)