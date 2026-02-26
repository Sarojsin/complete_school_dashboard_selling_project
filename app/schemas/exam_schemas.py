from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ExamResultCreate(BaseModel):
    student_id: int
    course_id: int
    marks: float
    max_marks: float = 100.0
    exam_type: str = "final"
    semester: str = "Spring 2024"

class ExamResultResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    marks: float
    max_marks: float = 100.0
    grade: str
    exam_type: str = "final"
    is_published: bool = True
    published_at: datetime
    semester: str
    # Populated by router, not ORM
    student_name: Optional[str] = None
    course_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class ExamNoticeCreate(BaseModel):
    title: str
    content: str
    notice_type: str = "schedule"  # schedule, hall_ticket, result
    exam_date: Optional[date] = None

class ExamNoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    notice_type: str
    exam_date: Optional[date]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExamDashboardStats(BaseModel):
    results_published: int = 0
    pending_results: int = 0
    exams_scheduled: int = 0
    total_students: int = 0

class StudentExamSummary(BaseModel):
    total_subjects: int
    total_marks: float
    average_marks: float
    semester: str