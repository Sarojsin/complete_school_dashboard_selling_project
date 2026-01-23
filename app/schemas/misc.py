from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

# Compatibility Imports for Legacy Routes
from app.schemas.auth import Token, TokenData, LoginRequest, UserResponse
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from app.schemas.authority import AuthorityCreate, AuthorityUpdate, AuthorityResponse
from app.schemas.parent import ParentCreate, ParentUpdate, ParentResponse
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeResponse
from app.schemas.fee import FeeRecordCreate, FeeRecordUpdate, FeeRecordResponse
FeeCreate = FeeRecordCreate
FeeUpdate = FeeRecordUpdate
FeeResponse = FeeRecordResponse
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentSubmissionCreate, AssignmentSubmissionUpdate, AssignmentSubmissionResponse
from app.legacy.tables.test_tables import TestForStudent, TestCreate, TestUpdate, TestResponse, TestSubmissionCreate, TestSubmissionResponse, TestResult
from app.schemas.group import GroupCreate, GroupUpdate, GroupInviteRequest, GroupMemberRole
from app.schemas.group_post import GroupPostCreate, GroupPostUpdate, GroupPostOut
from app.legacy.tables.chat_tables import ChatMessageResponse, OnlineUser, ChatMessageCreate, ChatMessageUpdate

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
