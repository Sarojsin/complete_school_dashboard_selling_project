# College Registrar Schemas

from pydantic import BaseModel
from typing import Optional
from datetime import date


class RegistrarBase(BaseModel):
    user_id: int
    full_name: Optional[str] = None
    designation: str = "Registrar"
    phone: Optional[str] = None


class RegistrarCreate(RegistrarBase):
    pass


class RegistrarUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None


class Registrar(RegistrarBase):
    id: int
    joining_date: date

    class Config:
        from_attributes = True


__all__ = ["RegistrarBase", "RegistrarCreate", "RegistrarUpdate", "Registrar"]
