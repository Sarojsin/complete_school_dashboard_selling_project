# College HOD Schemas

from pydantic import BaseModel
from typing import Optional
from datetime import date


class HODBase(BaseModel):
    user_id: int
    department_id: int
    full_name: Optional[str] = None
    designation: str = "HOD"
    qualification: Optional[str] = None
    phone: Optional[str] = None


class HODCreate(HODBase):
    pass


class HODUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    phone: Optional[str] = None


class HOD(HODBase):
    id: int
    joining_date: date

    class Config:
        from_attributes = True


__all__ = ["HODBase", "HODCreate", "HODUpdate", "HOD"]
