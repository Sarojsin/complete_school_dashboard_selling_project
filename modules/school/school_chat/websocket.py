"""
WebSocket Chat Router

Real-time chat WebSocket endpoint.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

router = APIRouter()


# Connection manager for WebSocket
class ConnectionManager:
    def __init__(self):
        # Active connections: {user_id: websocket}
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.
    
    Expected message format:
    {
        "type": "message|typing|read",
        "sender_id": int,
        "receiver_id": int,
        "content": str (optional)
    }
    """
    user_id = None
    
    try:
        # Get user_id from query parameter or first message
        # In production, this would be extracted from JWT token
        await websocket.accept()
        
        # First message should contain user_id
        first_message = await websocket.receive_text()
        data = json.loads(first_message)
        
        if data.get("type") == "auth" and "user_id" in data:
            user_id = data["user_id"]
            await manager.connect(websocket, user_id)
            
            # Notify others that user is online
            await manager.broadcast({
                "type": "user_online",
                "user_id": user_id
            })
        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Authentication required"
            }))
            await websocket.close()
            return
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "message":
                # Send to receiver
                receiver_id = message.get("receiver_id")
                if receiver_id:
                    await manager.send_personal_message({
                        "type": "message",
                        "sender_id": user_id,
                        "content": message.get("content"),
                        "timestamp": message.get("timestamp")
                    }, receiver_id)
                
                # Also send back to sender for confirmation
                await manager.send_personal_message({
                    "type": "message_sent",
                    "receiver_id": receiver_id
                }, user_id)
                
            elif message["type"] == "typing":
                # Send typing indicator to receiver
                receiver_id = message.get("receiver_id")
                if receiver_id:
                    await manager.send_personal_message({
                        "type": "typing",
                        "sender_id": user_id
                    }, receiver_id)
                
            elif message["type"] == "read":
                # Send read receipt
                receiver_id = message.get("receiver_id")
                if receiver_id:
                    await manager.send_personal_message({
                        "type": "read",
                        "sender_id": user_id
                    }, receiver_id)
                    
    except WebSocketDisconnect:
        if user_id:
            manager.disconnect(user_id)
            # Notify others that user went offline
            await manager.broadcast({
                "type": "user_offline",
                "user_id": user_id
            })


__all__ = ["router"]