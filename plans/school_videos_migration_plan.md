# Plan: Migrate school_videos Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_videos/)
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
| `backup/models/models.py` | Video class (lines ~379-397), VideoProgress class (lines ~399-411) |
| `backup/repositories/videos_repository.py` | VideosRepository with create, get, get_by_course, get_by_teacher, mark_as_watched |
| `backup/web/routers/teacher.py` | /teacher/videos/upload endpoints |
| `backup/web/routers/student.py` | /student/videos endpoints |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/models.py` (Video, VideoProgress classes)
**Target:** `modules/school/school_videos/models.py`

```python
# Expected structure:
class Video(Base):
    __tablename__ = "school_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)
    thumbnail = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("school_teachers.id", ondelete="SET NULL"), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    
    # Relationships
    course = relationship("SchoolCourse", back_populates="videos")
    teacher = relationship("Teacher", back_populates="videos")
    watch_history = relationship("VideoProgress", back_populates="video", cascade="all, delete-orphan")


class VideoProgress(Base):
    __tablename__ = "school_video_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("school_videos.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    watched_seconds = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="watch_history")
    student = relationship("SchoolStudent", back_populates="video_watch_history")
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_videos/schemas.py`

```python
# Expected schemas:
class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    course_id: int
    is_published: bool = False

class VideoCreate(VideoBase):
    pass

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None

class VideoResponse(VideoBase):
    id: int
    teacher_id: Optional[int] = None
    uploaded_at: datetime
    updated_at: datetime
    view_count: int
    class Config:
        from_attributes = True


class VideoProgressBase(BaseModel):
    video_id: int
    student_id: int
    watched_seconds: int = 0
    completed: bool = False

class VideoProgressCreate(VideoProgressBase):
    pass

class VideoProgressResponse(VideoProgressBase):
    id: int
    viewed_at: datetime
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/videos_repository.py`
**Target:** `modules/school/school_videos/repository.py`

Methods needed:
- `create(video_data)` - Create new video
- `get(video_id)` - Get video by ID
- `get_by_course(course_id)` - Get videos by course
- `get_by_teacher(teacher_id)` - Get videos by teacher
- `get_all(filters)` - Get all videos
- `update(video_id, data)` - Update video
- `delete(video_id)` - Delete video
- `increment_view_count(video_id)` - Increment view count
- `mark_as_watched(video_id, student_id)` - Mark video as watched

### Step 4: Create `api.py`
**Source:** `backup/web/routers/teacher.py`, `backup/web/routers/student.py`
**Target:** `modules/school/school_videos/api.py`

Endpoints needed:
- `POST /` - Upload video
- `GET /{id}` - Get video
- `GET /` - List videos (with filters: course_id, teacher_id, is_published)
- `PUT /{id}` - Update video
- `DELETE /{id}` - Delete video
- `GET /course/{course_id}` - Get videos by course
- `POST /{id}/watch` - Mark as watched
- `GET /{id}/progress/{student_id}` - Get student progress

### Step 5: Create `router.py`
**Target:** `modules/school/school_videos/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| Video class | Create with table name "school_videos" |
| VideoProgress class | Create with table name "school_video_progress" |
| Fields (Video) | title, description, file_path, thumbnail, duration, course_id, teacher_id, view_count, is_published |
| Fields (Progress) | video_id, student_id, watched_seconds, completed |
| Relationships | Add course, teacher, watch_history |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| VideoBase | title, description, file_path, thumbnail, duration, course_id, is_published |
| VideoCreate | All required fields |
| VideoUpdate | Optional fields for partial update |
| VideoResponse | All fields with timestamps and view_count |
| VideoProgressBase | video_id, student_id, watched_seconds, completed |
| VideoProgressResponse | All fields with id and viewed_at |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create | Insert new video |
| get | Fetch video by ID |
| get_by_course | Fetch videos for a course |
| get_by_teacher | Fetch videos by a teacher |
| get_all | List with pagination and filters |
| update | Modify existing video |
| delete | Remove video |
| increment_view_count | Update view count |
| mark_as_watched | Create/update progress record |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST / | Upload new video |
| GET /{id} | Get video details |
| GET / | List videos |
| PUT /{id} | Update video |
| DELETE /{id} | Delete video |
| POST /{id}/watch | Mark as watched |
| GET /{id}/progress/{student_id} | Get progress |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.repositories.videos_repository import ...` | Create new repository |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules