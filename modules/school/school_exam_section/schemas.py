# School Exam Section Schemas
# ========================

from pydantic import BaseModel
from typing import Optional
from datetime import date


class ExamScheduleBase(BaseModel):
    class_id: int
    subject: str
    exam_date: date
    start_time: str
    end_time: str
    total_marks: int = 100
    passing_marks: int = 35


class ExamScheduleCreate(ExamScheduleBase):
    pass


class ExamScheduleUpdate(BaseModel):
    subject: Optional[str] = None
    exam_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_marks: Optional[int] = None
    passing_marks: Optional[int] = None


class ExamSchedule(ExamScheduleBase):
    id: int

    class Config:
        from_attributes = True


class GradeBase(BaseModel):
    student_id: int
    exam_id: int
    marks: float
    grade: str
    remarks: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    marks: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None


class Grade(GradeBase):
    id: int

    class Config:
        from_attributes = True


__all__ = [
    "ExamScheduleBase",
    "ExamScheduleCreate",
    "ExamScheduleUpdate",
    "ExamSchedule",
    "GradeBase",
    "GradeCreate",
    "GradeUpdate",
    "Grade",
]