# 🧩 ELITE PLAN 8 — Shared Feature Modules
## Phase: CROSS-CUTTING FEATURES — chat, groups, assignments, grades, notices, videos, notifications
### Goal: Migrate all shared/cross-role feature files into dedicated feature modules

---

## 📌 Pre-Conditions (from Plan 7)
- [ ] ✅ `modules/auth/` working, all role modules protected
- [ ] ✅ `modules/super_admin/` operational
- [ ] ✅ All 20 role modules migrated and tested
- [ ] ✅ App runs cleanly with zero errors

---

## 🗂️ Features That Need Their Own Module

These features **span across roles** (school + college students, teachers, parents all use them). They live in `app/api/endpoints/` but map to no single role module:

| Feature | Source Files | New Module |
|---------|-------------|-----------|
| Chat / WebSocket | `chat.py`, `websocket_chat.py`, `chat_service.py`, `chat_repository.py`, `chat_models.py`, `websocket/` | `modules/chat/` |
| Groups | `groups.py`, `group_posts.py`, `group_service.py`, `group_post_service.py`, `group_repository.py`, `group_post_repository.py`, `group_models.py` | `modules/groups/` |
| Assignments | `assignments.py`, `assignment_repository.py`, `schemas/assignment.py` | `modules/assignments/` |
| Grades | `grades.py`, `grade_service.py`, `grade_repository.py`, `schemas/grade.py` | `modules/grades/` |
| Notices | `notices.py`, `admin_notices.py`, `admin_notice_service.py`, `admin_notice_repository.py`, `notice_repository.py`, `schemas/notice.py` | `modules/notices/` |
| Notes | `notes.py`, `notes_repository.py` | `modules/notes/` |
| Videos | `videos.py`, `videos_repository.py` | `modules/videos/` |
| Notifications | `notification_service.py` | `modules/notifications/` |
| Courses (school) | `courses.py`, `course_repository.py`, `schemas/course.py` | `modules/courses/` |

---

## 📋 MODULE: `modules/chat/`

### Source Files
```
app/models/chat_models.py              → modules/chat/models.py
app/schemas/  (chat-related)           → modules/chat/schemas.py
app/repositories/chat_repository.py   → modules/chat/repository.py
app/services/chat_service.py          → modules/chat/service.py
app/services/chat_cleanup_service.py  → modules/chat/cleanup.py
app/api/endpoints/chat.py             → modules/chat/api.py
app/api/endpoints/websocket_chat.py   → modules/chat/websocket.py
app/websocket/                        → modules/chat/websocket_manager.py
```

### Structure
```
modules/chat/
├── __init__.py
├── models.py            ← ChatRoom, ChatMessage, ChatParticipant
├── schemas.py           ← MessageCreate, MessageResponse, RoomCreate
├── repository.py        ← ChatRepository (get messages, create room, etc.)
├── service.py           ← ChatService
├── cleanup.py           ← ChatCleanupService (move from chat_cleanup_service.py)
├── api.py               ← REST endpoints for chat history, rooms
└── websocket.py         ← WebSocket endpoint (/ws/chat/{room_id})
```

### Key models.py
```python
# modules/chat/models.py
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    is_group = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    sender_id = Column(Integer)             # FK by name to avoid circular
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

### websocket.py
```python
# modules/chat/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from modules.shared.database import get_db
from modules.chat.service import ChatService

ws_router = APIRouter()

# Connection manager (from app/websocket/)
class ConnectionManager:
    def __init__(self): self.active_connections: dict = {}
    async def connect(self, room_id: int, ws: WebSocket):
        await ws.accept()
        self.active_connections.setdefault(room_id, []).append(ws)
    async def disconnect(self, room_id: int, ws: WebSocket):
        self.active_connections[room_id].remove(ws)
    async def broadcast(self, room_id: int, message: str):
        for conn in self.active_connections.get(room_id, []):
            await conn.send_text(message)

manager = ConnectionManager()

@ws_router.websocket("/ws/chat/{room_id}")
async def chat_websocket(room_id: int, websocket: WebSocket):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)
```

### Wire into main.py
```python
from modules.chat.api import router as chat_router
from modules.chat.websocket import ws_router as chat_ws_router
app.include_router(chat_router,    prefix="/api/v1/chat", tags=["💬 Chat"])
app.include_router(chat_ws_router, tags=["💬 Chat WebSocket"])
```

---

## 📋 MODULE: `modules/groups/`

### Source Files
```
app/models/group_models.py              → modules/groups/models.py
app/schemas/group.py + group_post.py    → modules/groups/schemas.py
app/repositories/group_repository.py   → modules/groups/repository.py
app/repositories/group_post_repository.py → modules/groups/repository.py (merge)
app/services/group_service.py          → modules/groups/service.py
app/services/group_post_service.py     → modules/groups/service.py (merge)
app/api/endpoints/groups.py            → modules/groups/api.py
app/api/endpoints/group_posts.py       → modules/groups/api.py (merge)
```

### Key api.py routes
```python
# modules/groups/api.py
router = APIRouter()

# Group CRUD
GET    /groups/          → list all groups
POST   /groups/          → create group
GET    /groups/{id}      → get group detail
PUT    /groups/{id}      → update group
DELETE /groups/{id}      → delete group

# Group Posts
GET    /groups/{id}/posts     → list posts in group
POST   /groups/{id}/posts     → create post
DELETE /groups/{id}/posts/{post_id} → delete post
POST   /groups/{id}/join      → join group
POST   /groups/{id}/leave     → leave group
```

### Wire into main.py
```python
from modules.groups.api import router as groups_router
app.include_router(groups_router, prefix="/api/v1", tags=["👥 Groups"])
```

---

## 📋 MODULE: `modules/assignments/`

### Source Files
```
app/schemas/assignment.py                → modules/assignments/schemas.py
app/repositories/assignment_repository.py → modules/assignments/repository.py
app/api/endpoints/assignments.py        → modules/assignments/api.py
```

> ℹ️ No dedicated service file for assignments in old code — use a thin service wrapper.

### Key routes
```python
GET  /assignments/          → list (filtered by student/teacher)
POST /assignments/          → create (teacher)
GET  /assignments/{id}      → get detail
PUT  /assignments/{id}      → update (teacher)
POST /assignments/{id}/submit → student submit
GET  /assignments/{id}/submissions → list submissions (teacher)
```

---

## 📋 MODULE: `modules/grades/`

### Source Files
```
app/schemas/grade.py               → modules/grades/schemas.py
app/repositories/grade_repository.py → modules/grades/repository.py
app/services/grade_service.py      → modules/grades/service.py
app/api/endpoints/grades.py        → modules/grades/api.py
```

### Key routes
```python
GET  /grades/              → get my grades (student) | all grades (teacher)
POST /grades/              → assign grade (teacher)
PUT  /grades/{id}          → update grade
GET  /grades/report/{student_id} → grade report for student
```

---

## 📋 MODULE: `modules/notices/`

### Source Files (merge school + admin notices)
```
app/schemas/notice.py              → modules/notices/schemas.py
app/repositories/notice_repository.py → modules/notices/repository.py
app/services/admin_notice_service.py → modules/notices/service.py
app/api/endpoints/notices.py       → modules/notices/api.py
app/api/endpoints/admin_notices.py → modules/notices/api.py (merge admin routes)
```

### Access control logic
```python
# modules/notices/api.py
@router.get("/notices/")
def list_notices(db=Depends(get_db), user=Depends(get_current_user)):
    # All users can READ notices
    ...

@router.post("/notices/")
def create_notice(db=Depends(get_db), user=Depends(require_school_staff)):
    # Only staff/admin can CREATE
    ...
```

---

## 📋 MODULE: `modules/notes/`

### Source Files
```
app/repositories/notes_repository.py → modules/notes/repository.py
app/api/endpoints/notes.py           → modules/notes/api.py
```

### Key routes
```python
GET    /notes/           → get my notes
POST   /notes/           → create note
PUT    /notes/{id}       → update note
DELETE /notes/{id}       → delete note
```

---

## 📋 MODULE: `modules/videos/`

### Source Files
```
app/repositories/videos_repository.py → modules/videos/repository.py
app/api/endpoints/videos.py           → modules/videos/api.py
```

### Key routes
```python
GET    /videos/              → list videos (public or course-specific)
POST   /videos/              → upload video (teacher)
GET    /videos/{id}          → stream/view video
DELETE /videos/{id}          → delete video (teacher/admin)
```

---

## 📋 MODULE: `modules/notifications/`

### Source Files
```
app/services/notification_service.py → modules/notifications/service.py
```

> ℹ️ No dedicated endpoint file — notifications are sent from other services.

### Usage pattern (called by other modules)
```python
# In modules/assignments/service.py
from modules.notifications.service import NotificationService

class AssignmentService:
    def submit_assignment(self, student_id, assignment_id, db):
        # ... do submission
        NotificationService(db).notify_teacher(
            teacher_id=assignment.teacher_id,
            message=f"Student {student_id} submitted assignment {assignment_id}"
        )
```

### modules/notifications/service.py
```python
# modules/notifications/service.py
from sqlalchemy.orm import Session

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def notify_user(self, user_id: int, title: str, message: str):
        # Store in DB and/or send via WebSocket
        pass

    def notify_teacher(self, teacher_id: int, message: str):
        self.notify_user(teacher_id, "New Notification", message)

    def notify_students_in_class(self, class_id: int, message: str):
        # Get all students in class and notify each
        pass
```

---

## 📋 MODULE: `modules/courses/` (School-side)

### Source Files
```
app/schemas/course.py              → modules/courses/schemas.py
app/repositories/course_repository.py → modules/courses/repository.py
app/api/endpoints/courses.py       → modules/courses/api.py
```

> ℹ️ College courses are already in `modules/college_registrar/`. This module handles school-level subject/course assignment.

---

## 🔧 Batch Folder Creation Script

```python
# scripts/create_feature_modules.py
from pathlib import Path

ROOT = Path(__file__).parent.parent
FEATURES = [
    "chat", "groups", "assignments", "grades",
    "notices", "notes", "videos", "notifications", "courses"
]

for feat in FEATURES:
    d = ROOT / "modules" / feat
    d.mkdir(parents=True, exist_ok=True)
    init = d / "__init__.py"
    if not init.exists():
        init.write_text(f'"""Feature module: {feat}"""\n')
        print(f"✅ Created modules/{feat}/")
    else:
        print(f"⏭️ Exists  modules/{feat}/")
```

```powershell
python scripts/create_feature_modules.py
```

---

## 📊 Phase 8 Completion Checklist

| Module | models | schemas | repo | service | api | Wired |
|--------|--------|---------|------|---------|-----|-------|
| chat | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| groups | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| assignments | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| grades | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| notices | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| notes | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| videos | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| notifications | — | — | — | [ ] | — | — |
| courses | [ ] | [ ] | [ ] | — | [ ] | [ ] |

### Additional checks
- [ ] WebSocket `/ws/chat/{room_id}` connects and broadcasts messages
- [ ] Groups maintain membership correctly
- [ ] Assignments submission triggers notification to teacher
- [ ] Grades are visible to students (role-filtered)
- [ ] Notices visible to all, writable only by staff
- [ ] `verify_module.py` runs clean on all 9 feature modules

---

## 🎉 Full Migration Complete!

Once Plan 8 is done, the complete modular architecture is:

```
modules/
├── shared/              ← DB, Base, config, utils
├── auth/                ← JWT, dependencies, roles (Plan 6)
├── super_admin/         ← System control (Plan 7)
│
├── school_authority/    ← (Plan 2)
├── school_teacher/      ← (Plan 2)
├── school_student/      ← (Plan 2)
├── school_parent/       ← (Plan 2)
├── school_library/      ← (Plan 2)
├── school_attendance/   ← (Plan 2)
├── school_exam_section/ ← (Plan 3)
├── school_account_section/ ← (Plan 3)
│
├── college_faculty/     ← (Plan 4)
├── college_student/     ← (Plan 4)
├── college_hod/         ← (Plan 4)
├── college_dean/        ← (Plan 4)
├── college_registrar/   ← (Plan 4)
├── college_exam_section/ ← (Plan 4)
├── college_account_section/ ← (Plan 4)
├── college_library/     ← (Plan 4)
├── college_placement/   ← (Plan 4)
├── college_research/    ← (Plan 4)
├── college_hostel/      ← (Plan 4)
├── college_lab/         ← (Plan 4)
│
├── chat/                ← (Plan 8) 💬
├── groups/              ← (Plan 8) 👥
├── assignments/         ← (Plan 8) 📝
├── grades/              ← (Plan 8) 📊
├── notices/             ← (Plan 8) 📢
├── notes/               ← (Plan 8) 📓
├── videos/              ← (Plan 8) 🎥
├── notifications/       ← (Plan 8) 🔔
└── courses/             ← (Plan 8) 📚
```

**Total: 32 modules — 100% of codebase covered.**
