"""
College Semester Schemas
"""

from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class SemesterBase(BaseModel):
    name: str
    program_id: Optional[int] = None
    number: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = False


class SemesterResponse(SemesterBase):
    id: int

    model_config = {"from_attributes": True}


__all__ = ["SemesterBase", "SemesterResponse"]
