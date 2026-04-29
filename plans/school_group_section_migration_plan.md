# Plan: Migrate school_group_section Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_group_section/)
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
| `backup/models/group_models.py` | Group, GroupMember, GroupPost models |
| `backup/web/routers/group_posts.py` | Group posts endpoints |
| `backup/api/endpoints/groups.py` | Groups API endpoints |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/group_models.py`
**Target:** `modules/school/school_group_section/models.py`

```python
# Expected structure:
class GroupSection(Base):
    __tablename__ = "school_group_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    group_type = Column(String(50), nullable=False)  # study, project, discussion, committee
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    subject_id = Column(Integer, ForeignKey("school_subjects.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    max_members = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("GroupSectionMember", back_populates="group", cascade="all, delete-orphan")
    posts = relationship("GroupSectionPost", back_populates="group", cascade="all, delete-orphan")


class GroupSectionMember(Base):
    __tablename__ = "school_group_section_members"
    
    id = Column(Integer, primary_key=True, index=True)
    group_section_id = Column(Integer, ForeignKey("school_group_sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="member")  # owner, admin, member
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    group = relationship("GroupSection", back_populates="members")


class GroupSectionPost(Base):
    __tablename__ = "school_group_section_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    group_section_id = Column(Integer, ForeignKey("school_group_sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    post_type = Column(String(50), default="discussion")  # announcement, discussion, question, resource
    file_url = Column(String(500), nullable=True)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    group = relationship("GroupSection", back_populates="posts")
    comments = relationship("GroupSectionComment", back_populates="post", cascade="all, delete-orphan")


class GroupSectionComment(Base):
    __tablename__ = "school_group_section_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    group_section_id = Column(Integer, ForeignKey("school_group_sections.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("school_group_section_posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = relationship("GroupSectionPost", back_populates="comments")
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_group_section/schemas.py`

```python
# Expected schemas:
class GroupSectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    group_type: str
    class_id: Optional[int] = None
    subject_id: Optional[int] = None
    academic_year: str
    max_members: Optional[int] = None
    is_public: bool = True

class GroupSectionCreate(GroupSectionBase):
    pass

class GroupSectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class GroupSectionResponse(GroupSectionBase):
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class GroupSectionPostBase(BaseModel):
    title: Optional[str] = None
    content: str
    post_type: str = "discussion"
    file_url: Optional[str] = None

class GroupSectionPostCreate(GroupSectionPostBase):
    group_section_id: int


class GroupSectionCommentBase(BaseModel):
    content: str

class GroupSectionCommentCreate(GroupSectionCommentBase):
    post_id: int
```

### Step 3: Create `repository.py`
**Target:** `modules/school/school_group_section/repository.py`

Methods needed:
- `create_group(group_data)` - Create new group
- `get_group(group_id)` - Get group by ID
- `get_all(filters)` - Get all groups
- `update_group(group_id, data)` - Update group
- `delete_group(group_id)` - Delete group
- `add_member(group_id, user_id, role)` - Add member
- `remove_member(group_id, user_id)` - Remove member
- `get_members(group_id)` - Get group members
- `create_post(post_data)` - Create post
- `get_posts(group_id)` - Get group posts
- `update_post(post_id, data)` - Update post
- `delete_post(post_id)` - Delete post
- `pin_post(post_id)` - Pin post
- `create_comment(comment_data)` - Create comment
- `get_comments(post_id)` - Get post comments
- `delete_comment(comment_id)` - Delete comment

### Step 4: Create `api.py`
**Source:** `backup/api/endpoints/groups.py`, `backup/web/routers/group_posts.py`
**Target:** `modules/school/school_group_section/api.py`

Endpoints needed:
- `POST /groups` - Create group
- `GET /groups` - List groups
- `GET /groups/{id}` - Get group
- `PUT /groups/{id}` - Update group
- `DELETE /groups/{id}` - Delete group
- `POST /groups/{id}/members` - Add member
- `GET /groups/{id}/members` - Get members
- `DELETE /groups/{id}/members/{user_id}` - Remove member
- `POST /groups/{id}/posts` - Create post
- `GET /groups/{id}/posts` - Get posts
- `PUT /groups/{id}/posts/{post_id}` - Update post
- `DELETE /groups/{id}/posts/{post_id}` - Delete post
- `POST /groups/{id}/posts/{post_id}/pin` - Pin post
- `POST /groups/{id}/posts/{post_id}/comments` - Add comment

### Step 5: Create `router.py`
**Target:** `modules/school/school_group_section/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| GroupSection class | Create with table name "school_group_sections" |
| GroupSectionMember class | Create with table name "school_group_section_members" |
| GroupSectionPost class | Create with table name "school_group_section_posts" |
| GroupSectionComment class | Create with table name "school_group_section_comments" |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| GroupSectionBase | name, description, group_type, class_id, subject_id, academic_year |
| GroupSectionCreate | All required fields |
| GroupSectionPostBase | title, content, post_type, file_url |
| GroupSectionCommentBase | content |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create_group | Create new group |
| get_group | Fetch group by ID |
| get_all | List groups |
| update_group | Modify group |
| delete_group | Remove group |
| add_member | Add user to group |
| remove_member | Remove user from group |
| create_post | Create post |
| get_posts | List group posts |
| create_comment | Add comment |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST /groups | Create group |
| GET /groups | List groups |
| GET /groups/{id} | Get group |
| PUT /groups/{id} | Update group |
| DELETE /groups/{id} | Delete group |
| POST /groups/{id}/posts | Create post |
| GET /groups/{id}/posts | Get posts |
| POST /groups/{id}/posts/{post_id}/comments | Add comment |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules