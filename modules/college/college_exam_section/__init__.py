"""
College Exam Section Module

Handles exam results publishing, result retrieval, and exam notices for college.
"""

from .router import router as exam_section_router
from .service import ExamSectionService
from .repository import ExamSectionRepository
from .models import CollegeExamResult, CollegeExamNotice
from .schemas import (
    CollegeExamResultCreate,
    CollegeExamResultUpdate,
    CollegeExamResultResponse,
    CollegeExamNoticeCreate,
    CollegeExamNoticeResponse,
)

__all__ = [
    "router",
    "ExamSectionService",
    "ExamSectionRepository",
    "CollegeExamResult",
    "CollegeExamNotice",
    "CollegeExamResultCreate",
    "CollegeExamResultUpdate",
    "CollegeExamResultResponse",
    "CollegeExamNoticeCreate",
    "CollegeExamNoticeResponse",
]
