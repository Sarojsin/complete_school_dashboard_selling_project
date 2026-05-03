from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from backup.core.database import get_async_db
from backup.models.models import User
from backup.utils.websocket_manager import manager
from backup.core.config import settings
from backup.services.chat_service import ChatService
import json
from typing import Optional

router = APIRouter()

async def get_user_from_token(token: Optional[str], db: AsyncSession) -> User:
    """Authenticate user from WebSocket token"""
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        res = await db.execute(select(User).filter(User.id == int(user_id)))
        user = res.scalars().first()
        return user
    except (JWTError, ValueError):
        return None

@router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db)
):
    if not token:
        cookie_authorization = websocket.cookies.get("access_token")
        if cookie_authorization:
            scheme, _, param = cookie_authorization.partition(" ")
            if scheme.lower() == "bearer" and param:
                token = param

    user = await get_user_from_token(token, db)
    
    if not user:
        await websocket.close(code=1008)  # Policy violation
        return
    
    await manager.connect(user.id, websocket)
    
    # Notify others that user is online
    await manager.broadcast({
        "type": "user_status",
        "user_id": user.id,
        "status": "online"
    }, exclude_user=user.id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                # Save message to database using Service
                chat_message = await ChatService.save_message(
                    db=db,
                    sender_id=user.id,
                    receiver_id=message_data["receiver_id"],
                    content=message_data["content"]
                )
                
                # Send to receiver if online
                await manager.send_personal_message({
                    "type": "message",
                    "id": chat_message.id,
                    "sender_id": user.id,
                    "sender_name": user.full_name,
                    "content": chat_message.content,
                    "created_at": chat_message.created_at.isoformat()
                }, message_data["receiver_id"])
                
                # Confirm to sender
                await manager.send_personal_message({
                    "type": "message_sent",
                    "id": chat_message.id,
                    "created_at": chat_message.created_at.isoformat()
                }, user.id)
            
            elif message_data.get("type") == "typing":
                # Forward typing indicator
                await manager.send_personal_message({
                    "type": "typing",
                    "user_id": user.id,
                    "user_name": user.full_name
                }, message_data["receiver_id"])
            
            elif message_data.get("type") == "mark_read":
                # Mark messages as read using Service
                message_ids = message_data.get("message_ids", [])
                await ChatService.mark_messages_as_read(db, message_ids, user.id)
                
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        # Notify others that user is offline
        await manager.broadcast({
            "type": "user_status",
            "user_id": user.id,
            "status": "offline"
        })
    except Exception as e:
        import logging
        logging.error(f"WebSocket error: {e}")
        manager.disconnect(user.id)
        await manager.broadcast({
            "type": "user_status",
            "user_id": user.id,
            "status": "offline"
        })
