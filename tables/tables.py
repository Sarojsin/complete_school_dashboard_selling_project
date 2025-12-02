from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date, time
from models.models import UserRole

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Student Schemas
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

# Teacher Schemas
class TeacherBase(BaseModel):
    employee_id: str
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class TeacherCreate(UserCreate, TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class TeacherResponse(TeacherBase):
    id: int
    user_id: int
    joining_date: date
    user: UserResponse
    
    class Config:
        from_attributes = True

# Authority Schemas
class AuthorityBase(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class AuthorityCreate(UserCreate, AuthorityBase):
    secret_key: str

class AuthorityUpdate(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class AuthorityResponse(AuthorityBase):
    id: int
    user_id: int
    user: UserResponse
    
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    course_code: str
    course_name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    grade_level: Optional[str] = None
    semester: Optional[str] = None

class CourseCreate(CourseBase):
    teacher_id: Optional[int] = None

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    teacher_id: Optional[int] = None
    grade_level: Optional[str] = None
    semester: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    teacher_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assignment Schemas
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

# Assignment Submission Schemas
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

# Attendance Schemas
class AttendanceBase(BaseModel):
    date: date
    status: str  # present, absent, late
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    student_id: int
    course_id: int

class AttendanceResponse(AttendanceBase):
    id: int
    student_id: int
    course_id: int
    
    class Config:
        from_attributes = True

# Grade Schemas
class GradeBase(BaseModel):
    grade_type: Optional[str] = None
    score: float
    max_score: float
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeCreate(GradeBase):
    student_id: int
    course_id: int

class GradeUpdate(BaseModel):
    score: Optional[float] = None
    max_score: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeResponse(GradeBase):
    id: int
    student_id: int
    course_id: int
    date: date
    
    class Config:
        from_attributes = True

# Fee Schemas
class FeeRecordBase(BaseModel):
    fee_type: str
    amount: float
    due_date: date
    remarks: Optional[str] = None

class FeeRecordCreate(FeeRecordBase):
    student_id: int

class FeeRecordUpdate(BaseModel):
    paid_amount: Optional[float] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

class FeeRecordResponse(FeeRecordBase):
    id: int
    student_id: int
    paid_amount: float
    payment_date: Optional[date]
    status: str
    
    class Config:
        from_attributes = True

# Notice Schemas
class NoticeBase(BaseModel):
    title: str
    content: str
    target_role: Optional[str] = "all"
    priority: str = "normal"
    expires_at: Optional[datetime] = None

class NoticeCreate(NoticeBase):
    authority_id: int

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    target_role: Optional[str] = None
    priority: Optional[str] = None
    expires_at: Optional[datetime] = None

class NoticeResponse(NoticeBase):
    id: int
    authority_id: int
    file_path: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schedule Schemas
class ScheduleBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    room: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    course_id: int

class ScheduleResponse(ScheduleBase):
    id: int
    course_id: int
    
    class Config:
        from_attributes = True

# Note Schemas
class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None

class NoteCreate(NoteBase):
    course_id: int

class NoteResponse(NoteBase):
    id: int
    course_id: int
    teacher_id: int
    file_path: str
    file_size: Optional[int]
    file_type: Optional[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Video Schemas
class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None

class VideoCreate(VideoBase):
    course_id: int

class VideoResponse(VideoBase):
    id: int
    course_id: int
    teacher_id: int
    file_path: str
    duration: Optional[int]
    file_size: Optional[int]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str