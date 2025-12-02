from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database.database import get_db
from models.models import User
from models.chat_models import ChatMessage
from utils.websocket_manager import manager
from config.config import settings
from datetime import datetime
import json

router = APIRouter()

async def get_user_from_token(token: str, db: Session) -> User:
    """Authenticate user from WebSocket token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        return None

@router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
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
                # Save message to database
                chat_message = ChatMessage(
                    sender_id=user.id,
                    receiver_id=message_data["receiver_id"],
                    content=message_data["content"]
                )
                db.add(chat_message)
                db.commit()
                db.refresh(chat_message)
                
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
                # Mark messages as read
                message_ids = message_data.get("message_ids", [])
                db.query(ChatMessage).filter(
                    ChatMessage.id.in_(message_ids),
                    ChatMessage.receiver_id == user.id
                ).update({"is_read": True}, synchronize_session=False)
                db.commit()
                
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        # Notify others that user is offline
        await manager.broadcast({
            "type": "user_status",
            "user_id": user.id,
            "status": "offline"
        })
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(user.id)
        await manager.broadcast({
            "type": "user_status",
            "user_id": user.id,
            "status": "offline"
        })