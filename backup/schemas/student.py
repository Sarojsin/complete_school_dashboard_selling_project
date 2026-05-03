from pydantic import BaseModel
from typing import Optional
from datetime import date
from .user import UserCreate, UserResponse

class StudentBase(BaseModel):
    student_id: str
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None

class StudentCreate(UserCreate, StudentBase):
    pass

class StudentUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    user_id: int
    enrollment_date: date
    user: UserResponse
    
    class Config:
        from_attributes = True
