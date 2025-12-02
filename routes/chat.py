from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from dependencies import get_current_user
from models.models import User
from repositories.chat_repository import ChatRepository
from repositories.user_repository import UserRepository
from tables.chat_tables import ChatMessageResponse, OnlineUser
from utils.websocket_manager import manager

router = APIRouter()

@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of users current user has conversations with"""
    conversations = ChatRepository.get_conversations_list(db, current_user.id)
    
    # Add online status
    for conv in conversations:
        conv['is_online'] = manager.is_user_online(conv['user'].id)
    
    return conversations

@router.get("/messages/{other_user_id}")
async def get_conversation_messages(
    other_user_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages between current user and another user"""
    # Verify other user exists
    other_user = UserRepository.get_by_id(db, other_user_id)
    if not other_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = ChatRepository.get_conversation(db, current_user.id, other_user_id, limit)
    
    # Mark messages as read
    ChatRepository.mark_as_read(db, current_user.id, other_user_id)
    
    return {
        "other_user": other_user,
        "messages": messages,
        "is_online": manager.is_user_online(other_user_id)
    }

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread messages"""
    count = ChatRepository.get_unread_count(db, current_user.id)
    return {"unread_count": count}

@router.post("/mark-read/{other_user_id}")
async def mark_conversation_read(
    other_user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all messages from a user as read"""
    ChatRepository.mark_as_read(db, current_user.id, other_user_id)
    return {"message": "Messages marked as read"}

@router.get("/online-users")
async def get_online_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of currently online users"""
    online_user_ids = manager.get_online_users()
    
    online_users = []
    for user_id in online_user_ids:
        if user_id != current_user.id:  # Exclude current user
            user = UserRepository.get_by_id(db, user_id)
            if user:
                online_users.append(OnlineUser(
                    user_id=user.id,
                    username=user.username,
                    full_name=user.full_name,
                    role=user.role.value,
                    is_online=True
                ))
    
    return online_users

@router.get("/search-users/{query}")
async def search_users_to_chat(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search users to start a conversation"""
    from models.models import User
    
    search_pattern = f"%{query}%"
    users = db.query(User).filter(
        (User.full_name.ilike(search_pattern)) | (User.username.ilike(search_pattern)),
        User.id != current_user.id,
        User.is_active == True
    ).limit(20).all()
    
    # Add online status
    user_list = []
    for user in users:
        user_list.append({
            "user": user,
            "is_online": manager.is_user_online(user.id)
        })
    
    return user_list

@router.get("/search-messages/{query}")
async def search_messages(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search in message history"""
    messages = ChatRepository.search_messages(db, current_user.id, query)
    return messages