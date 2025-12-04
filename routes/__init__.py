# Import all routers for easy registration in main.py
from routes import (
    auth,
    students,
    teachers,
    tests,
    assignments,
    attendance,
    websocket_chat,
    parents
)

# You can add more imports as you create additional route files:
# from app.routes import courses, grades, fees, notices, notes, videos, chat, authority

__all__ = [
    'auth',
    'students', 
    'teachers',
    'tests',
    'assignments',
    'attendance',
    'websocket_chat',
    'parents'
]