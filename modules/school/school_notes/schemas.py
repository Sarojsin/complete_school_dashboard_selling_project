from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    course_id: int
    is_published: bool = True


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None


class NoteResponse(NoteBase):
    id: int
    teacher_id: Optional[int] = None
    uploaded_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NoteCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class NoteCategoryCreate(NoteCategoryBase):
    pass


class NoteCategoryResponse(NoteCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True