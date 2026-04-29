# Plan: Migrate school_chat_section Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_chat_section/)
Check if this module exists in modules/school/ - likely doesn't exist yet.

Note: The main school_chat module exists. This is a separate module for chat sections/rooms.

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
| `backup/models/group_models.py` | Group model (similar concepts for sections) |
| `backup/api/endpoints/chat.py` | Chat endpoints |
| `backup/repositories/chat_repository.py` | ChatRepository |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** Reference `backup/models/group_models.py` for structure
**Target:** `modules/school/school_chat_section/models.py`

```python
# Expected structure:
class ChatSection(Base):
    __tablename__ = "school_chat_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    section_type = Column(String(50), nullable=False)  # class, subject, group, general
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    subject_id = Column(Integer, ForeignKey("school_subjects.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("ChatSectionMember", back_populates="section", cascade="all, delete-orphan")
    messages = relationship("ChatSectionMessage", back_populates="section", cascade="all, delete-orphan")


class ChatSectionMember(Base):
    __tablename__ = "school_chat_section_members"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_section_id = Column(Integer, ForeignKey("school_chat_sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="member")  # admin, member
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    section = relationship("ChatSection", back_populates="members")


class ChatSectionMessage(Base):
    __tablename__ = "school_chat_section_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_section_id = Column(Integer, ForeignKey("school_chat_sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, file, image
    file_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    section = relationship("ChatSection", back_populates="messages")
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_chat_section/schemas.py`

```python
# Expected schemas:
class ChatSectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    section_type: str
    class_id: Optional[int] = None
    subject_id: Optional[int] = None
    academic_year: str

class ChatSectionCreate(ChatSectionBase):
    pass

class ChatSectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ChatSectionResponse(ChatSectionBase):
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class ChatSectionMemberBase(BaseModel):
    user_id: int
    role: str = "member"

class ChatSectionMemberCreate(ChatSectionMemberBase):
    pass


class ChatSectionMessageBase(BaseModel):
    message: str
    message_type: str = "text"
    file_url: Optional[str] = None

class ChatSectionMessageCreate(ChatSectionMessageBase):
    chat_section_id: int

class ChatSectionMessageResponse(ChatSectionMessageBase):
    id: int
    user_id: int
    chat_section_id: int
    created_at: datetime
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/chat_repository.py`
**Target:** `modules/school/school_chat_section/repository.py`

Methods needed:
- `create_section(section_data)` - Create new section
- `get_section(section_id)` - Get section by ID
- `get_all(filters)` - Get all sections
- `update_section(section_id, data)` - Update section
- `delete_section(section_id)` - Delete section
- `add_member(section_id, user_id, role)` - Add member
- `remove_member(section_id, user_id)` - Remove member
- `get_members(section_id)` - Get section members
- `create_message(message_data)` - Create message
- `get_messages(section_id)` - Get section messages

### Step 4: Create `api.py`
**Source:** `backup/api/endpoints/chat.py`
**Target:** `modules/school/school_chat_section/api.py`

Endpoints needed:
- `POST /sections` - Create section
- `GET /sections` - List sections
- `GET /sections/{id}` - Get section
- `PUT /sections/{id}` - Update section
- `DELETE /sections/{id}` - Delete section
- `POST /sections/{id}/members` - Add member
- `GET /sections/{id}/members` - Get members
- `DELETE /sections/{id}/members/{user_id}` - Remove member
- `POST /sections/{id}/messages` - Send message
- `GET /sections/{id}/messages` - Get messages

### Step 5: Create `router.py`
**Target:** `modules/school/school_chat_section/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| ChatSection class | Create with table name "school_chat_sections" |
| ChatSectionMember class | Create with table name "school_chat_section_members" |
| ChatSectionMessage class | Create with table name "school_chat_section_messages" |
| Fields | name, description, section_type, class_id, subject_id, academic_year, is_active |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| ChatSectionBase | name, description, section_type, class_id, subject_id, academic_year |
| ChatSectionCreate | All required fields |
| ChatSectionUpdate | Optional fields |
| ChatSectionMessageBase | message, message_type, file_url |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create_section | Create new chat section |
| get_section | Fetch section by ID |
| get_all | List sections |
| update_section | Modify section |
| delete_section | Remove section |
| add_member | Add user to section |
| remove_member | Remove user from section |
| get_members | List section members |
| create_message | Add message to section |
| get_messages | List section messages |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST /sections | Create section |
| GET /sections | List sections |
| GET /sections/{id} | Get section |
| PUT /sections/{id} | Update section |
| DELETE /sections/{id} | Delete section |
| POST /sections/{id}/members | Add member |
| DELETE /sections/{id}/members/{user_id} | Remove member |
| POST /sections/{id}/messages | Send message |
| GET /sections/{id}/messages | Get messages |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.repositories.chat_repository import ...` | Create new repository |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules