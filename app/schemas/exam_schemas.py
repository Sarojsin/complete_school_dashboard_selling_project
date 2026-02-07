from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExamResultCreate(BaseModel):
    student_id: int
    course_id: int
    marks: float
    semester: str = "Spring 2024"

class ExamResultResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    course_id: int
    course_name: str
    marks: float
    grade: str
    published_at: datetime
    semester: str
    
    class Config:
        orm_mode = True

class StudentExamSummary(BaseModel):
    total_subjects: int
    total_marks: float
    average_marks: float
    semester: str