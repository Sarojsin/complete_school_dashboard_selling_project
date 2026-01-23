from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
