# College Exam Section Schemas

from pydantic import BaseModel
from typing import Optional
from datetime import date


class ExamScheduleBase(BaseModel):
    course_id: int
    semester_id: int
    exam_type: str
    exam_date: date
    start_time: str
    end_time: str
    room: Optional[str] = None


class ExamScheduleCreate(ExamScheduleBase):
    pass


class ExamScheduleUpdate(BaseModel):
    exam_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room: Optional[str] = None


class ExamSchedule(ExamScheduleBase):
    id: int

    class Config:
        from_attributes = True


__all__ = ["ExamScheduleBase", "ExamScheduleCreate", "ExamScheduleUpdate", "ExamSchedule"]
