from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.core.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.models import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.schemas.misc import ChatMessageResponse, OnlineUser
from app.utils.websocket_manager import manager
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get list of users current user has conversations with"""
    conversations = await ChatRepository.get_conversations_list(db, current_user.id)
    
    # Add online status
    for conv in conversations:
        conv['is_online'] = manager.is_user_online(conv['user'].id)
    
    return conversations

@router.get("/messages/{other_user_id}")
async def get_messages(
    other_user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get messages with specific user"""
    messages = await ChatRepository.get_conversation(db, current_user.id, other_user_id)
    other_user = await UserRepository.get_by_id(db, other_user_id)
    
    return {
        "messages": messages,
        "other_user": other_user
    }

@router.post("/messages/{receiver_id}")
async def send_message(
    receiver_id: int,
    content: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Send a message to another user"""
    message_data = {
        "sender_id": current_user.id,
        "receiver_id": receiver_id,
        "content": content.get("content"),
        "expires_at": datetime.utcnow() + timedelta(days=1)
    }
    
    message = await ChatRepository.create(db, message_data)
    
    # Notify via WebSocket if receiver is online
    if manager.is_user_online(receiver_id):
        await manager.send_personal_message(
            {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
                "is_read": message.is_read
            },
            receiver_id
        )
    
    return message

@router.post("/mark-read/{sender_id}")
async def mark_messages_read(
    sender_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Mark all messages from sender as read"""
    await ChatRepository.mark_as_read(db, current_user.id, sender_id)
    return {"status": "success"}

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get total unread message count"""
    count = await ChatRepository.get_unread_count(db, current_user.id)
    return {"count": count}

@router.get("/online-users")
async def get_online_users(
    current_user: User = Depends(get_current_user)
):
    """Get list of currently online users"""
    online_ids = manager.get_online_users()
    return {"online_user_ids": online_ids}

@router.get("/search/{query}")
async def search_users(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Search for users to chat with"""
    search_pattern = f"%{query}%"
    res = await db.execute(select(User).filter(
        or_(User.full_name.ilike(search_pattern), User.username.ilike(search_pattern)),
        User.id != current_user.id,
        User.is_active == True
    ).limit(20))
    users = res.scalars().all()
    
    # Add online status
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "role": user.role,
            "is_online": manager.is_user_online(user.id)
        })
    
    return user_list

@router.get("/contacts/parent")
async def get_parent_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get contacts for a parent (all teachers)"""
    from app.repositories.parent_repository import ParentRepository
    
    parent = await ParentRepository.get_by_user_id(db, current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
        
    contacts = await ChatRepository.get_all_teachers(db, parent.id)
    
    # Add online status
    for contact in contacts:
        contact['is_online'] = manager.is_user_online(contact['user'].id)
        
    return contacts

@router.get("/contacts/teacher")
async def get_teacher_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get contacts for a teacher (parents of their students)"""
    from app.repositories.teacher_repository import TeacherRepository
    
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
        
    contacts = await ChatRepository.get_teacher_parents(db, teacher.id)
    
    # Add online status
    for contact in contacts:
        contact['is_online'] = manager.is_user_online(contact['user'].id)
        
    return contacts

@router.get("/search-messages/{query}")
async def search_messages(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Search in message history"""
    messages = await ChatRepository.search_messages(db, current_user.id, query)
    return messages