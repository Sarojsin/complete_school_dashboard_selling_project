from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessageBase(BaseModel):
    content: str


class ChatMessageCreate(ChatMessageBase):
    receiver_id: int
    file_name: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    is_read: bool
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatMessageUpdate(BaseModel):
    is_read: bool = True


class Conversation(BaseModel):
    """Conversation with another user"""
    user_id: int
    user_name: str
    last_message: str
    last_message_time: datetime
    unread_count: int = 0