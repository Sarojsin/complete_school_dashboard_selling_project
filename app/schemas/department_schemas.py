from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepartmentCreate(BaseModel):
    name: str
    code: str
    hod_teacher_id: Optional[int] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    code: str
    hod_teacher_id: Optional[int]
    
    class Config:
        orm_mode = True

class HODDashboardStats(BaseModel):
    total_teachers: int
    total_students: int
    total_courses: int