from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int
    is_published: Optional[bool] = True

class VideoCreate(VideoBase):
    pass

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None

class VideoResponse(VideoBase):
    id: int
    teacher_id: Optional[int] = None
    file_path: str
    thumbnail_path: Optional[str] = None
    duration: Optional[int] = None
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VideoProgressBase(BaseModel):
    video_id: int
    watched_seconds: int = 0
    completed: bool = False

class VideoProgressCreate(VideoProgressBase):
    student_id: int

class VideoProgressResponse(VideoProgressBase):
    id: int
    student_id: int
    last_viewed_at: datetime

    class Config:
        from_attributes = True
