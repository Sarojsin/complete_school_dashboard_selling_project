"""
College Exam Section Schemas

Pydantic schemas for exam result and notice validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ExamType(str, Enum):
    MIDTERM = "midterm"
    FINAL = "final"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class NoticeType(str, Enum):
    SCHEDULE = "schedule"
    HALL_TICKET = "hall_ticket"
    RESULT = "result"
    GENERAL = "general"


# ── Exam Result Schemas ───────────────────────────────────────────

class CollegeExamResultBase(BaseModel):
    student_id: int
    course_id: int
    marks: float = Field(..., ge=0)
    max_marks: float = Field(100.0, gt=0)
    exam_type: ExamType = ExamType.FINAL
    semester_id: Optional[int] = None
    remarks: Optional[str] = None


class CollegeExamResultCreate(CollegeExamResultBase):
    is_published: bool = False


class CollegeExamResultUpdate(BaseModel):
    marks: Optional[float] = Field(None, ge=0)
    is_published: Optional[bool] = None
    remarks: Optional[str] = None


class CollegeExamResultResponse(CollegeExamResultBase):
    id: int
    grade: Optional[str] = None
    is_published: bool
    published_by: Optional[int] = None
    published_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Exam Notice Schemas ────────────────────────────────────────────

class CollegeExamNoticeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    notice_type: NoticeType
    exam_date: Optional[datetime] = None
    semester_id: Optional[int] = None


class CollegeExamNoticeCreate(CollegeExamNoticeBase):
    pass


class CollegeExamNoticeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    is_active: Optional[bool] = None


class CollegeExamNoticeResponse(CollegeExamNoticeBase):
    id: int
    created_by: int
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}


# ── Dashboard / Report Schemas ────────────────────────────────────

class ExamSectionDashboard(BaseModel):
    total_results: int
    published_count: int
    unpublished_count: int
    recent_results: List[CollegeExamResultResponse] = []


__all__ = [
    "CollegeExamResultBase",
    "CollegeExamResultCreate",
    "CollegeExamResultUpdate",
    "CollegeExamResultResponse",
    "CollegeExamNoticeBase",
    "CollegeExamNoticeCreate",
    "CollegeExamNoticeUpdate",
    "CollegeExamNoticeResponse",
    "ExamSectionDashboard",
    "ExamType",
    "NoticeType",
]
