from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User
from .repository import ChatRepository
from .schemas import ChatMessageCreate, ChatMessageResponse, ChatMessageUpdate, Conversation

router = APIRouter(dependencies=[Depends(require_school_portal)])


@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of conversations with last message info"""
    conversations = await ChatRepository.get_conversations(db, current_user.id)
    return conversations


@router.get("/messages/{user_id}", response_model=List[ChatMessageResponse])
async def get_conversation_messages(
    user_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get messages between current user and another user"""
    messages = await ChatRepository.get_conversation(db, current_user.id, user_id, limit)
    return messages


@router.post("/messages", response_model=ChatMessageResponse)
async def send_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message to another user"""
    # Can't send message to yourself
    if message_data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")
    
    message = await ChatRepository.create(db, {
        "sender_id": current_user.id,
        "receiver_id": message_data.receiver_id,
        "content": message_data.content,
        "file_name": message_data.file_name
    })
    return message


@router.put("/messages/{message_id}/read", response_model=ChatMessageResponse)
async def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a message as read"""
    message = await ChatRepository.get_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Only receiver can mark as read
    if message.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    message.is_read = True
    await db.commit()
    await db.refresh(message)
    return message


@router.put("/messages/read/{user_id}")
async def mark_conversation_read(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark all messages from a user as read"""
    await ChatRepository.mark_as_read(db, current_user.id, user_id)
    return {"message": "Messages marked as read"}


@router.get("/unread/count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get count of unread messages"""
    count = await ChatRepository.get_unread_count(db, current_user.id)
    return {"unread_count": count}


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a message (only sender can delete)"""
    message = await ChatRepository.get_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.delete(message)
    await db.commit()
    return {"message": "Message deleted"}


@router.get("/search")
async def search_messages(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search messages"""
    messages = await ChatRepository.search_messages(db, current_user.id, query)
    return messages


# Additional endpoints from backup

@router.get("/online-users")
async def get_online_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of online users"""
    from sqlalchemy import or_
    from modules.shared.models import User
    
    result = await db.execute(
        select(User).filter(User.is_active == True).limit(50)
    )
    users = result.scalars().all()
    
    # Filter out current user
    online_users = [u for u in users if u.id != current_user.id]
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "role": u.role.value if hasattr(u.role, 'value') else str(u.role)} for u in online_users]


@router.get("/search/users")
async def search_users(
    query: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search users to chat with"""
    from sqlalchemy import or_
    from modules.shared.models import User
    
    result = await db.execute(
        select(User).filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.full_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            ),
            User.is_active == True
        ).limit(20)
    )
    users = result.scalars().all()
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "role": u.role.value if hasattr(u.role, 'value') else str(u.role)} for u in users]


@router.get("/contacts/teacher")
async def get_teacher_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of teachers for contact"""
    from modules.shared.models import UserRole
    from sqlalchemy import select
    
    result = await db.execute(
        select(User).filter(User.role == UserRole.TEACHER, User.is_active == True)
    )
    teachers = result.scalars().all()
    return [{"id": t.id, "username": t.username, "full_name": t.full_name, "role": t.role.value if hasattr(t.role, 'value') else str(t.role)} for t in teachers]


@router.get("/contacts/parent")
async def get_parent_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of parents for contact"""
    from modules.shared.models import UserRole
    from sqlalchemy import select
    
    result = await db.execute(
        select(User).filter(User.role == UserRole.PARENT, User.is_active == True)
    )
    parents = result.scalars().all()
    return [{"id": p.id, "username": p.username, "full_name": p.full_name, "role": p.role.value if hasattr(p.role, 'value') else str(p.role)} for p in parents]


__all__ = ["router"]