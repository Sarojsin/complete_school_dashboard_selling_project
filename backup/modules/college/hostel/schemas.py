"""
Hostel Schemas

Pydantic schemas for hostel and room management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HostelBase(BaseModel):
    name: str
    address: str
    contact_number: str
    email: str
    warden_name: str
    total_rooms: int


class HostelResponse(HostelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HostelListResponse(BaseModel):
    hostels: list[HostelResponse]
    total: int


class RoomBase(BaseModel):
    room_number: str
    floor: int
    capacity: int
    occupied: int = 0
    hostel_id: int
    room_type: str = "standard"  # standard, deluxe, ac


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoomListResponse(BaseModel):
    rooms: list[RoomResponse]
    total: int
