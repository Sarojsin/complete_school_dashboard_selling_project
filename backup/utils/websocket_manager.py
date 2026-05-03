
from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                print(f"Error sending message to user {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict, exclude_user: int = None):
        for user_id, connection in list(self.active_connections.items()):
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to user {user_id}: {e}")
                self.disconnect(user_id)
    
    def get_online_users(self) -> List[int]:
        return list(self.active_connections.keys())
    
    def is_user_online(self, user_id: int) -> bool:
        return user_id in self.active_connections

manager = ConnectionManager()