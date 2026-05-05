"""
College Program Schemas
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProgramBase(BaseModel):
    name: str
    code: str
    department_id: Optional[int] = None
    level: Optional[str] = None
    duration_years: Optional[int] = None
    total_credits: Optional[int] = None


class ProgramResponse(ProgramBase):
    id: int

    model_config = {"from_attributes": True}


__all__ = ["ProgramBase", "ProgramResponse"]
