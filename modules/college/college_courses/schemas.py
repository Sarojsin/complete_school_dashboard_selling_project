"""
College Course Schemas

Pydantic schemas for college courses, departments, programs, semesters.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# ── Course Schemas ─────────────────────────────────────────────
class CollegeCourseBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    credits: Optional[int] = 3
    department_id: Optional[int] = None
    semester_id: Optional[int] = None
    instructor_id: Optional[int] = None
    is_elective: Optional[bool] = False
    max_students: Optional[int] = 60


class CollegeCourseCreate(CollegeCourseBase):
    pass


class CollegeCourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    semester_id: Optional[int] = None
    instructor_id: Optional[int] = None
    is_elective: Optional[bool] = None
    max_students: Optional[int] = None


class CollegeCourseResponse(CollegeCourseBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Department Schemas ─────────────────────────────────────────
class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hod_teacher_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    id: int
    hod_teacher_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Program Schemas ────────────────────────────────────────────
class ProgramBase(BaseModel):
    name: str
    code: str
    level: str
    duration_years: Optional[int] = None
    total_credits: Optional[int] = None


class ProgramCreate(ProgramBase):
    department_id: Optional[int] = None


class ProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    duration_years: Optional[int] = None
    total_credits: Optional[int] = None


class ProgramResponse(ProgramBase):
    id: int
    department_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Semester Schemas ───────────────────────────────────────────
class SemesterBase(BaseModel):
    name: str
    number: int
    is_current: Optional[bool] = False


class SemesterCreate(SemesterBase):
    program_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SemesterUpdate(BaseModel):
    name: Optional[str] = None
    is_current: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SemesterResponse(SemesterBase):
    id: int
    program_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ── Enrollment Schemas ──────────────────────────────────────────
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    semester_id: Optional[int] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    grade: Optional[str] = None
    grade_points: Optional[float] = None


class EnrollmentResponse(EnrollmentBase):
    id: int
    enrollment_date: Optional[datetime] = None
    status: Optional[str] = None
    grade: Optional[str] = None
    grade_points: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)