# Plan: Migrate school_notes Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_notes/)
Check if this module exists in modules/school/ - likely doesn't exist yet.

| File | Current State | Issues |
|------|---------------|--------|
| `models.py` | ❌ Missing | Need to create from backup |
| `schemas.py` | ❌ Missing | Need to create from backup |
| `repository.py` | ❌ Missing | Need to create from backup |
| `api.py` | ❌ Missing | Need to create from backup |
| `router.py` | ❌ Missing | Need to create from backup |

### Source from Backup
| File | Contents |
|------|----------|
| `backup/models/models.py` | Note class (lines ~360-377) with title, description, file_path, course_id, teacher_id |
| `backup/repositories/notes_repository.py` | NotesRepository with create, get, get_by_course, get_by_teacher |
| `backup/web/routers/teacher.py` | /teacher/notes/upload endpoints |
| `backup/web/routers/student.py` | /student/notes endpoints |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/models.py` (Note class)
**Target:** `modules/school/school_notes/models.py`

```python
# Expected structure:
class Note(Base):
    __tablename__ = "school_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=True)  # pdf, doc, ppt, etc.
    file_size = Column(Integer, nullable=True)  # in bytes
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("school_teachers.id", ondelete="SET NULL"), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("SchoolCourse", back_populates="notes")
    teacher = relationship("Teacher", back_populates="notes")
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_notes/schemas.py`

```python
# Expected schemas:
class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    course_id: int

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None

class NoteResponse(NoteBase):
    id: int
    teacher_id: Optional[int] = None
    uploaded_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/notes_repository.py`
**Target:** `modules/school/school_notes/repository.py`

Methods needed:
- `create(note_data)` - Create new note
- `get(note_id)` - Get note by ID
- `get_by_course(course_id)` - Get notes by course
- `get_by_teacher(teacher_id)` - Get notes by teacher
- `get_all(filters)` - Get all notes
- `update(note_id, data)` - Update note
- `delete(note_id)` - Delete note

### Step 4: Create `api.py`
**Source:** `backup/web/routers/teacher.py`, `backup/web/routers/student.py`
**Target:** `modules/school/school_notes/api.py`

Endpoints needed:
- `POST /` - Upload note
- `GET /{id}` - Get note
- `GET /` - List notes (with filters: course_id, teacher_id)
- `PUT /{id}` - Update note
- `DELETE /{id}` - Delete note
- `GET /course/{course_id}` - Get notes by course
- `GET /teacher/{teacher_id}` - Get notes by teacher

### Step 5: Create `router.py`
**Target:** `modules/school/school_notes/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| Note class | Create with table name "school_notes" |
| Fields | title, description, file_path, file_type, file_size, course_id, teacher_id |
| Relationships | Add course and teacher relationships |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| NoteBase | title, description, file_path, file_type, file_size, course_id |
| NoteCreate | All required fields |
| NoteUpdate | Optional fields for partial update |
| NoteResponse | All fields including id, teacher_id, timestamps |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create | Insert new note |
| get | Fetch note by ID |
| get_by_course | Fetch notes for a course |
| get_by_teacher | Fetch notes by a teacher |
| get_all | List with pagination and filters |
| update | Modify existing note |
| delete | Remove note |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST / | Upload new note |
| GET /{id} | Get note details |
| GET / | List notes |
| PUT /{id} | Update note |
| DELETE /{id} | Delete note |
| GET /course/{course_id} | Get by course |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.repositories.notes_repository import ...` | Create new repository |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules