# College Dean Schemas

from pydantic import BaseModel
from typing import Optional
from datetime import date


class DeanBase(BaseModel):
    user_id: int
    full_name: Optional[str] = None
    designation: str = "Dean"
    faculty: Optional[str] = None
    phone: Optional[str] = None


class DeanCreate(DeanBase):
    pass


class DeanUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    faculty: Optional[str] = None
    phone: Optional[str] = None


class Dean(DeanBase):
    id: int
    joining_date: date

    class Config:
        from_attributes = True


__all__ = ["DeanBase", "DeanCreate", "DeanUpdate", "Dean"]
