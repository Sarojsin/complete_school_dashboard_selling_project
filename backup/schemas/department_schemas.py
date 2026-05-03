from pydantic import BaseModel
from typing import Optional, List
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
        from_attributes = True

class HODDashboardStats(BaseModel):
    department_name: str = ""
    department_id: int = 0
    total_teachers: int = 0
    total_students: int = 0
    total_courses: int = 0