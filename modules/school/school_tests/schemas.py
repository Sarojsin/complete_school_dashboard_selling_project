from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import QuestionType


class QuestionBase(BaseModel):
    question_text: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    points: float = 1.0
    order: int = 0


class QuestionCreate(QuestionBase):
    correct_answer: Optional[str] = None


class QuestionResponse(QuestionBase):
    id: int
    test_id: int
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None

    class Config:
        from_attributes = True


class TestBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    subject_name: Optional[str] = None
    grade_level: Optional[str] = None
    target_section: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration: int

    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class TestCreate(TestBase):
    questions: List[QuestionCreate]


class TestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None


class TestResponse(TestBase):
    id: int
    teacher_id: int
    total_points: float
    is_active: bool
    created_at: datetime
    questions: List[QuestionResponse] = []

    class Config:
        from_attributes = True


class TestForStudent(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructions: Optional[str]
    subject_name: Optional[str] = None
    grade_level: Optional[str] = None
    target_section: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration: int
    total_points: float
    questions: List[QuestionBase]  # No correct answers

    class Config:
        from_attributes = True


class TestSubmissionCreate(BaseModel):
    answers: Dict[str, Any]


class TestSubmissionUpdate(BaseModel):
    answers: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    percentage: Optional[float] = None
    is_graded: Optional[bool] = None
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = None
    time_taken: Optional[int] = None


class TestSubmissionResponse(BaseModel):
    id: int
    test_id: int
    student_id: int
    answers: Optional[Dict[str, Any]]
    score: Optional[float]
    max_score: Optional[float]
    percentage: Optional[float]
    started_at: datetime
    submitted_at: Optional[datetime]
    time_taken: Optional[int]
    is_graded: bool
    feedback: Optional[str]

    class Config:
        from_attributes = True


class TestResult(BaseModel):
    test_id: int
    test_title: str
    score: float
    max_score: float
    percentage: float
    time_taken: int
    submitted_at: datetime
    feedback: Optional[str]
    questions_correct: int
    total_questions: int