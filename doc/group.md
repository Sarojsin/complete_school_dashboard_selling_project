# Group Management System Documentation

## Overview

The Group Management System allows educational institutions to create and manage groups for different purposes (classes, clubs, study groups, etc.). The system implements role-based access control with three distinct user levels: Authority, Teachers, and Students.

## Architecture

### Role-Based Access Control (RBAC)

| Role | Create Groups | Manage Members | Post Content | View Content | Download Notes |
|------|--------------|----------------|--------------|--------------|----------------|
| **Authority/Admin** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Teacher** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Student** | ❌ | ❌ | ❌ | ✅ | ✅ |

### Permissions Breakdown

#### Authority (Full Access)
- Create new groups
- Add/remove teachers and students to/from groups
- Edit group details (name, description)
- Post notices, notes, and links
- View all group content
- Delete groups (if implemented)

#### Teachers (Content Contributors)
- Post notices (announcements)
- Post notes (study materials with file attachments)
- Post links (external resources)
- View all group content
- Download notes and materials
- **Cannot** create groups or manage membership

#### Students (Read-Only Access)
- View all group posts
- Download study notes
- View notices and links
- **Cannot** post anything
- **Cannot** create groups or manage membership

## Directory Structure

```
templates/
├── authority/
│   └── groups.html          # Authority group management interface
├── teacher/
│   └── groups.html          # Teacher posting interface
├── student/
│   └── groups.html          # Student read-only interface
└── groups/
    ├── group_list.html      # General groups list (fallback)
    ├── create_group.html    # Group creation form (Authority only)
    ├── edit_group.html      # Group editing form (Authority only)
    ├── group_detail.html    # Individual group details page
    ├── manage_members.html  # Member management (Authority only)
    ├── group_posts.html     # List of posts in a group
    ├── new_post.html        # Create post form (Authority/Teacher)
    └── view_post.html       # Individual post view

routes/
├── groups.py               # Group CRUD operations
└── group_posts.py          # Post CRUD operations

repositories/
├── group_repository.py     # Group database operations
└── group_post_repository.py # Post database operations

services/
├── group_service.py        # Group business logic
└── group_post_service.py   # Post business logic
```

## URL Structure

### Role-Specific Endpoints

```
/authority/groups          → Authority group management page
/teacher/groups           → Teacher posting page
/student/groups           → Student view-only page
```

### Shared Endpoints

```
/groups                   → General groups list
/groups/create            → Create group (Authority only)
/groups/{id}              → Group details
/groups/{id}/edit         → Edit group (Authority only)
/groups/{id}/manage       → Manage members (Authority only)
/groups/{id}/posts        → View posts
/groups/{id}/posts/create → Create post (Authority/Teacher)
/groups/{id}/posts/{post_id} → View specific post
```

## Data Models

### Group Model
```python
- id: Integer (Primary Key)
- name: String (Group name)
- code: String (Unique 6-character code for easy sharing)
- description: Text (Optional group description)
- created_by: Integer (Foreign Key to User)
- created_at: DateTime
- updated_at: DateTime
- is_active: Boolean
```

### Group Member Model
```python
- id: Integer (Primary Key)
- group_id: Integer (Foreign Key to Group)
- user_id: Integer (Foreign Key to User)
- role: Enum (teacher/student)
- joined_at: DateTime
- is_active: Boolean
```

### Group Post Model
```python
- id: Integer (Primary Key)
- group_id: Integer (Foreign Key to Group)
- author_id: Integer (Foreign Key to User)
- post_type: Enum (notice/note/link)
- title: String
- content: Text
- file_path: String (Optional, for notes)
- link_url: String (Optional, for links)
- created_at: DateTime
- updated_at: DateTime
- is_active: Boolean
```

## Implementation Approach

### 1. Separation of Concerns

Each role has its own dedicated template with role-appropriate UI:

- **Authority Template**: Shows "Create Group" and "Manage Members" buttons
- **Teacher Template**: Shows "Create Post" button, no group management
- **Student Template**: Shows only "View Content" button, read-only mode

### 2. Permission Checks

Permission validation occurs at multiple levels:

**Route Level** (`main.py`):
```python
@app.get("/authority/groups")
async def authority_groups(...):
    # Check if user is authority
    if role.lower() not in ["authority", "admin"]:
        raise HTTPException(status_code=403)
```

**Service Level** (`group_service.py`):
```python
def create_group(...):
    # Additional business logic validation
```

**Template Level**:
```jinja2
{% if current_user.role.value in ['AUTHORITY', 'ADMIN'] %}
    <!-- Show admin controls -->
{% endif %}
```

### 3. Post Types

The system supports three types of posts:

1. **Notice**: Text-only announcements
2. **Note**: Study materials with file attachments
3. **Link**: External resource URLs

Dynamic form fields appear based on selected post type using JavaScript.

### 4. Member Management

Only Authority can:
- Add teachers to groups (who can then post content)
- Add students to groups (who can view content)
- Remove members from groups
- Change member roles (if needed)

### 5. Navigation Integration

Dashboard links are role-specific:

```html
<!-- Authority Dashboard -->
<a href="/authority/groups">Groups</a>

<!-- Teacher Dashboard -->
<a href="/teacher/groups">Groups</a>

<!-- Student Dashboard -->
<a href="/student/groups">Groups</a>
```

## Security Considerations

1. **Authorization**: Every route checks user role before allowing access
2. **Input Validation**: All forms use Pydantic schemas for validation
3. **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
4. **File Upload Security**: File paths are validated and sanitized
5. **Session Management**: Uses SessionMiddleware with secure session keys

## Database Relationships

```
User (1) ─────── (Many) GroupMember
                     │
Group (1) ─────── (Many) GroupMember
                     │
Group (1) ─────── (Many) GroupPost
                     │
User (1) ─────── (Many) GroupPost (as author)
```

## Key Features

### 1. Group Code System
- Each group gets a unique 6-character code
- Easy sharing and joining mechanism
- Automatic generation on group creation

### 2. Dynamic Forms
- JavaScript-powered dynamic form fields
- Different fields for different post types
- File upload support for notes

### 3. Role-Based UI
- Each role sees appropriate controls
- Prevents confusion and unauthorized actions
- Clean, focused interfaces

### 4. Scalability
- Repository pattern for data access
- Service layer for business logic
- Easy to extend with new features

## Future Enhancements

1. **Group Categories**: Organize groups by type (Class, Club, Study Group)
2. **Bulk Member Import**: CSV upload for adding multiple members
3. **Post Comments**: Allow discussions on posts
4. **Notifications**: Email/push notifications for new posts
5. **Analytics**: Track engagement and activity
6. **File Version Control**: Track note/file revisions
7. **Group Archives**: Soft delete with archiving capability

## Troubleshooting

### Common Issues

1. **"Not authorized" errors**: Check user role matches the endpoint
2. **Template not found**: Ensure role-specific template exists
3. **Posts not visible**: Verify user is a group member
4. **Upload fails**: Check file size limits and upload directory permissions

## Testing

### Manual Testing Checklist

- [ ] Authority can create groups
- [ ] Authority can add/remove members
- [ ] Teachers can post all content types
- [ ] Students can only view content
- [ ] File downloads work correctly
- [ ] Links open in new tabs
- [ ] Group codes are unique
- [ ] Permission checks work at all levels

## Maintenance

### Regular Tasks

1. Monitor upload directory size
2. Clean up inactive groups periodically
3. Review and update permissions as needed
4. Back up group content and files

---

**Version**: 1.0  
**Last Updated**: 2025-12-11  
**Author**: Development Team
