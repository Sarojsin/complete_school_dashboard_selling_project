from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    content: str
    receiver_id: int

class ChatMessageCreate(ChatMessageBase):
    file_name: Optional[str] = None
    file_type: Optional[str] = None

class ChatMessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    file_path: Optional[str]
    file_name: Optional[str]
    file_type: Optional[str]
    is_read: bool
    created_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageUpdate(BaseModel):
    is_read: bool = True

class OnlineUser(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: str
    is_online: bool
    