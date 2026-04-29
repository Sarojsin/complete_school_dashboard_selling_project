from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class TimetableEntryBase(BaseModel):
    course_id: int
    teacher_id: Optional[int] = None
    class_id: Optional[int] = None
    day_of_week: str
    start_time: str
    end_time: str
    room: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    is_active: Optional[int] = 1


class TimetableEntryCreate(TimetableEntryBase):
    pass


class TimetableEntryUpdate(BaseModel):
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    class_id: Optional[int] = None
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    is_active: Optional[int] = None


class TimetableEntryResponse(TimetableEntryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PeriodBase(BaseModel):
    period_number: int
    start_time: str
    end_time: str
    name: Optional[str] = None
    is_break: Optional[int] = 0
    academic_year: Optional[str] = None
    class_id: Optional[int] = None


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(BaseModel):
    period_number: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    name: Optional[str] = None
    is_break: Optional[int] = None
    academic_year: Optional[str] = None
    class_id: Optional[int] = None


class PeriodResponse(PeriodBase):
    id: int

    class Config:
        from_attributes = True


class TimetableConflictCheck(BaseModel):
    course_id: int
    day_of_week: str
    start_time: str
    end_time: str
    exclude_entry_id: Optional[int] = None


class TimetableResponse(BaseModel):
    entries: list
    total: int