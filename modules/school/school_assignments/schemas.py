from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: float = 100.0


class AssignmentCreate(AssignmentBase):
    course_id: int
    teacher_id: int


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = None


class AssignmentResponse(AssignmentBase):
    id: int
    course_id: int
    teacher_id: int
    file_path: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    submission_text: Optional[str] = None


class AssignmentSubmissionUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None


class AssignmentSubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submission_text: Optional[str]
    file_path: Optional[str]
    submitted_at: datetime
    score: Optional[float]
    feedback: Optional[str]
    graded_at: Optional[datetime]
    
    class Config:
        from_attributes = True