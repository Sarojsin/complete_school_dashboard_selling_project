from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade_type: Optional[str] = None
    score: float
    max_score: float
    grade: Optional[str] = None
    remarks: Optional[str] = None
    academic_year: str
    term: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    score: Optional[float] = None
    max_score: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None


class GradeBulkCreate(BaseModel):
    grades: List[GradeCreate]


class GradeResponse(GradeBase):
    id: int
    date: datetime
    
    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    name: str
    course_id: int
    academic_year: str
    term: Optional[str] = None
    max_marks: float = 100.0
    weight: float = 1.0


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentResponse(AssessmentBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class GradeReportResponse(BaseModel):
    id: int
    student_id: int
    academic_year: str
    term: Optional[str] = None
    gpa: Optional[float] = None
    total_marks: Optional[float] = None
    rank: Optional[int] = None
    generated_at: datetime
    
    class Config:
        from_attributes = True