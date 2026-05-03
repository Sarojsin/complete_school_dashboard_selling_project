# School Parent Schemas

from pydantic import BaseModel, Field
from typing import Optional


class ParentBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None


class ParentCreate(ParentBase):
    user_id: int


class ParentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None


class Parent(ParentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


__all__ = ["ParentBase", "ParentCreate", "ParentUpdate", "Parent"]
