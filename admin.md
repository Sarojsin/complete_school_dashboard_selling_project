# Admin Panel with Feature Control System - Implementation Guide

This document contains the complete implementation plan for adding an Admin Panel to the School Management System that can control all features (enable/disable) and manage role-based access.

---

## Table of Contents

1. [Overview](#overview)
2. [Current System Analysis](#current-system-analysis)
3. [Database Schema](#database-schema)
4. [Feature Codes Reference](#feature-codes-reference)
5. [Implementation Steps](#implementation-steps)
6. [API Endpoints](#api-endpoints)
7. [Middleware Integration](#middleware-integration)
8. [Code Examples](#code-examples)
9. [Testing Checklist](#testing-checklist)

---

## Overview

**Goal:** Create a centralized admin panel that allows administrators to:
- Enable/disable individual features system-wide
- Control which roles (STUDENT, TEACHER, AUTHORITY, etc.) can access specific features
- View audit logs of all admin actions
- Monitor system statistics

**Why This Matters:**
- Flexibility to toggle features without code changes
- Security by controlling access per role
- Easy maintenance and testing

---

## Current System Analysis

### Existing User Roles

Located in [`app/models/models.py`](app/models/models.py:7):

```python
class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    AUTHORITY = "AUTHORITY"
    PARENT = "PARENT"
    HOD = "HOD"
    EXAM_SECTION = "EXAM_SECTION"
    LIBRARY_MANAGER = "LIBRARY_MANAGER"
    ACCOUNT_SECTION = "ACCOUNT_SECTION"
    GROUP_CREATOR = "GROUP_CREATOR"
```

### Existing Feature Modules

Located in [`app/api/endpoints/`](app/api/endpoints/):

| Module | File | Purpose |
|--------|------|---------|
| Authentication | `auth.py` | Login, signup, password reset |
| Authority | `authority.py` | Dashboard, manage students/teachers |
| Students | `students.py` | Student profiles, enrollments |
| Teachers | `teachers.py` | Teacher profiles, courses |
| Courses | `courses.py` | Course management |
| Assignments | `assignments.py` | Assignment CRUD |
| Attendance | `attendance.py` | Attendance tracking |
| Grades | `grades.py` | Grade management |
| Fees | `fees.py` | Fee structures, payments |
| Library | `library.py` | Book management |
| Notices | `notices.py` | Notice board |
| Groups | `groups.py` | Class groups |
| Chat | `chat.py`, `websocket_chat.py` | Messaging |
| Exams | `exam_section.py` | Exam management |
| Tests | `tests.py` | Online testing |
| Videos | `videos.py` | Educational videos |
| Notes | `notes.py` | Study materials |
| Parents | `parents.py` | Parent portal |
| Account | `account.py` | Financial transactions |
| HOD | `hod.py` | Department head |

---

## Database Schema

### 3 New Tables to Create

#### 1. System Features Table

**File:** Create `app/models/admin_models.py`

```python
class SystemFeature(Base):
    __tablename__ = "system_features"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_code = Column(String(100), unique=True, nullable=False, index=True)
    feature_name = Column(String(255), nullable=False)
    feature_category = Column(String(100))  # academic, finance, communication
    description = Column(Text)
    is_enabled = Column(Boolean, default=True)
    is_global = Column(Boolean, default=True)  # If True, applies to all roles
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    role_permissions = relationship("FeatureRolePermission", back_populates="feature", cascade="all, delete-orphan")
```

#### 2. Feature Role Permissions Table

```python
class FeatureRolePermission(Base):
    __tablename__ = "feature_role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("system_features.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    can_create = Column(Boolean, default=True)
    can_read = Column(Boolean, default=True)
    can_update = Column(Boolean, default=True)
    can_delete = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    feature = relationship("SystemFeature", back_populates="role_permissions")
```

#### 3. Admin Audit Log Table

```python
class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # enable_feature, disable_feature
    feature_code = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
```

---

## Feature Codes Reference

### Authentication & User Management

| Code | Name | Description |
|------|------|-------------|
| AUTH_STUDENT_SIGNUP | Student Signup | Allow students to register |
| AUTH_TEACHER_SIGNUP | Teacher Signup | Allow teachers to register |
| AUTH_PARENT_SIGNUP | Parent Signup | Allow parents to register |
| AUTH_PASSWORD_RESET | Password Reset | Password reset functionality |
| AUTH_SOCIAL_LOGIN | Social Login | OAuth/Google login |

### Academic Features

| Code | Name | Description |
|------|------|-------------|
| ACADEMIC_COURSES | Course Management | Create/manage courses |
| ACADEMIC_ASSIGNMENTS | Assignments | Create/submit assignments |
| ACADEMIC_ATTENDANCE | Attendance | Track attendance |
| ACADEMIC_GRADES | Grades | Manage grades |
| ACADEMIC_EXAMS | Exams | Exam management |
| ACADEMIC_TESTS | Online Tests | Testing system |
| ACADEMIC_VIDEOS | Video Lessons | Video content |
| ACADEMIC_NOTES | Study Notes | Share materials |

### Student Management

| Code | Name | Description |
|------|------|-------------|
| STUDENT_ENROLLMENT | Student Enrollment | Enroll new students |
| STUDENT_PROFILE_EDIT | Profile Editing | Students edit profile |
| STUDENT_VIEW_OTHER | View Other Students | See other students |

### Teacher Management

| Code | Name | Description |
|------|------|-------------|
| TEACHER_CREATE | Create Teachers | Create teacher accounts |
| TEACHER_ASSIGN_COURSES | Assign Courses | Assign teachers to courses |
| TEACHER_VIEW_STUDENTS | View Students | View student data |

### Finance

| Code | Name | Description |
|------|------|-------------|
| FINANCE_FEE_STRUCTURE | Fee Structure | Create fee structures |
| FINANCE_PAYMENT | Fee Payment | Online payments |
| FINANCE_REPORTS | Financial Reports | View reports |

### Communication

| Code | Name | Description |
|------|------|-------------|
| COMM_NOTICES | Notice Board | Post/view notices |
| COMM_GROUPS | Class Groups | Manage groups |
| COMM_CHAT | Chat/Messaging | Real-time chat |
| COMM_PARENT_PORTAL | Parent Portal | Parent access |

### Library

| Code | Name | Description |
|------|------|-------------|
| LIBRARY_BOOKS | Book Management | Manage books |
| LIBRARY_ISSUE_RETURN | Issue/Return | Issue books |

### Reports

| Code | Name | Description |
|------|------|-------------|
| REPORTS_STUDENT_ANALYTICS | Student Analytics | Performance data |
| REPORTS_ATTENDANCE_ANALYTICS | Attendance Reports | Attendance data |
| REPORTS_FINANCIAL | Financial Reports | Financial data |

---

## Implementation Steps

### Step 1: Create Admin Models

**File:** `app/models/admin_models.py`

Create the three models: `SystemFeature`, `FeatureRolePermission`, `AdminAuditLog`

**Imports needed:**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base
from app.models.models import UserRole
```

### Step 2: Update Models Init

**File:** `app/models/__init__.py`

Add:
```python
from app.models.admin_models import SystemFeature, FeatureRolePermission, AdminAuditLog
```

### Step 3: Create Feature Repository

**File:** `app/repositories/feature_repository.py`

Key methods to implement:
- `create_feature(feature_data)` - Create new feature
- `get_feature_by_code(code)` - Get by code
- `get_all_features(category, enabled_only)` - List all
- `update_feature(code, updates)` - Update feature
- `delete_feature(code)` - Delete feature
- `get_role_permission(feature_id, role)` - Get role permission
- `set_role_permission(feature_id, role, permissions)` - Set permission

### Step 4: Create Feature Service

**File:** `app/services/feature_service.py`

Key methods to implement:
- `check_feature_enabled(feature_code)` - Check global enable
- `check_role_permission(feature_code, role, action)` - Check role permission
- `can_access_feature(feature_code, user, action)` - Combined check
- `toggle_feature(feature_code, enabled)` - Enable/disable
- `get_features_by_category(category)` - Group by category

### Step 5: Create Admin Features API

**File:** `app/api/endpoints/admin_features.py`

Endpoints to create:

```python
# Feature CRUD
GET    /api/admin/features              # List all features
POST   /api/admin/features              # Create feature
GET    /api/admin/features/{code}       # Get feature
PUT    /api/admin/features/{code}       # Update feature
DELETE /api/admin/features/{code}       # Delete feature

# Toggle
POST   /api/admin/features/{code}/toggle  # Toggle on/off

# Categories
GET    /api/admin/features/categories   # Group by category

# Role Permissions
GET    /api/admin/features/{code}/permissions  # Get permissions
PUT    /api/admin/features/{code}/permissions  # Update permissions
POST   /api/admin/features/{code}/permissions/{role}  # Add role

# Audit
GET    /api/admin/audit-logs           # Get logs
GET    /api/admin/audit-logs/feature/{code}  # Feature logs
```

### Step 6: Create Admin Dashboard API

**File:** `app/api/endpoints/admin_dashboard.py`

```python
GET  /api/admin/dashboard              # Dashboard stats
GET  /api/admin/stats                  # System statistics
GET  /api/admin/users/count            # Users by role
GET  /api/admin/features/summary       # Feature summary
```

### Step 7: Register Routes in Main

**File:** `app/main.py`

Add imports:
```python
from app.api.endpoints import admin_features, admin_dashboard
```

Add routers:
```python
app.include_router(admin_features.router, prefix="/api/admin", tags=["Admin Features"])
app.include_router(admin_dashboard.router, prefix="/api/admin", tags=["Admin Dashboard"])
```

### Step 8: Create Feature Check Middleware

**File:** `app/middleware/feature_check.py`

```python
from fastapi import Depends, HTTPException, status
from app.services.feature_service import FeatureService

def require_feature(feature_code: str, action: str = "read"):
    """Dependency to check feature access"""
    async def check(request: Request, current_user: User = Depends(get_current_user)):
        if not await FeatureService.can_access_feature(feature_code, current_user, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_code}' is disabled or you don't have permission"
            )
        return current_user
    return check
```

### Step 9: Integrate with Existing Endpoints

Add feature checks to existing endpoints. Example for student signup:

**File:** `app/api/endpoints/auth.py`

```python
@router.post("/signup/student")
async def student_signup(
    student_data: StudentSignup,
    current_user: User = Depends(require_feature("AUTH_STUDENT_SIGNUP", "create"))
):
    # Existing code...
```

### Step 10: Create Admin Templates

**File:** `app/templates/admin/features.html`

Create HTML page with:
- List of all features with toggle switches
- Filter by category
- Search functionality
- Role permission matrix

### Step 11: Create Admin Web Routes

**File:** `app/main.py`

```python
@router.get("/admin/features")
async def admin_features_page(request: Request, current_user: User = Depends(get_current_authority)):
    features = await FeatureService.get_all_features()
    return templates.TemplateResponse("admin/features.html", {"request": request, "features": features})
```

### Step 12: Create Seed Script

**File:** `scripts/setup/seed_features.py`

Seed all default features:
```python
DEFAULT_FEATURES = [
    {"code": "AUTH_STUDENT_SIGNUP", "name": "Student Signup", "category": "auth"},
    {"code": "ACADEMIC_COURSES", "name": "Course Management", "category": "academic"},
    # ... add all features
]
```

---

## API Endpoints

### Feature Management

#### List All Features
```
GET /api/admin/features
Query params: category, enabled_only, page, per_page
Response: List of features with permissions
```

#### Create Feature
```
POST /api/admin/features
Body: {
    "feature_code": "STUDENT_ENROLLMENT",
    "feature_name": "Student Enrollment",
    "feature_category": "student_management",
    "description": "Enroll new students",
    "is_enabled": true
}
```

#### Toggle Feature
```
POST /api/admin/features/STUDENT_ENROLLMENT/toggle
Response: {"success": true, "is_enabled": false}
```

#### Set Role Permission
```
PUT /api/admin/features/STUDENT_ENROLLMENT/permissions
Body: {
    "role": "TEACHER",
    "can_create": true,
    "can_read": true,
    "can_update": false,
    "can_delete": false
}
```

### Audit Logs
```
GET /api/admin/audit-logs?page=1&per_page=20
Response: List of admin actions with timestamps
```

---

## Middleware Integration

### How to Add Feature Checks to Endpoints

#### Method 1: Using Dependency (Recommended)

```python
from app.middleware.feature_check import require_feature

@router.post("/students", dependencies=[Depends(require_feature("STUDENT_ENROLLMENT", "create"))])
async def create_student(student: StudentCreate, current_user: User = Depends(get_current_authority)):
    # Your code
```

#### Method 2: Manual Check in Endpoint

```python
@router.post("/students")
async def create_student(student: StudentCreate, current_user: User = Depends(get_current_authority)):
    # Check if feature is enabled
    if not await FeatureService.can_access_feature("STUDENT_ENROLLMENT", current_user, "create"):
        raise HTTPException(status_code=403, detail="Student enrollment is disabled")
    # Your code
```

#### Method 3: Service Layer Check

```python
@router.post("/students")
async def create_student(student: StudentCreate, current_user: User = Depends(get_current_authority)):
    await FeatureService.enforce_feature_access("STUDENT_ENROLLMENT", current_user, "create")
    # Your code
```

---

## Code Examples

### Example: Checking Feature Access

```python
from app.services.feature_service import FeatureService

async def my_endpoint(current_user: User = Depends(get_current_user)):
    # Check if feature is enabled for any access
    is_enabled = await FeatureService.check_feature_enabled("STUDENT_ENROLLMENT")
    
    # Check if user role has permission
    can_create = await FeatureService.check_role_permission(
        "STUDENT_ENROLLMENT", 
        current_user.role, 
        "create"
    )
    
    # Combined check
    can_access = await FeatureService.can_access_feature(
        "STUDENT_ENROLLMENT",
        current_user,
        "create"
    )
```

### Example: Toggle Feature

```python
from app.services.feature_service import FeatureService

async def toggle_student_enrollment():
    await FeatureService.toggle_feature("STUDENT_ENROLLMENT", False)
    # Now students cannot be enrolled until enabled again
```

### Example: Custom Response When Feature Disabled

```python
from fastapi import HTTPException

@router.get("/students")
async def get_students(
    current_user: User = Depends(get_current_user),
    feature_service: FeatureService = Depends()
):
    if not await feature_service.check_feature_enabled("STUDENT_ENROLLMENT"):
        return {"message": "Student enrollment is currently disabled", "students": []}
    
    # Return students...
```

---

## Testing Checklist

### Phase 1: Model Testing
- [ ] SystemFeature table created correctly
- [ ] FeatureRolePermission table created correctly
- [ ] AdminAuditLog table created correctly
- [ ] Relationships work properly

### Phase 2: Repository Testing
- [ ] Create feature works
- [ ] Get feature by code works
- [ ] Update feature works
- [ ] Delete feature works
- [ ] Role permissions CRUD works

### Phase 3: Service Testing
- [ ] check_feature_enabled returns correct value
- [ ] check_role_permission returns correct value
- [ ] can_access_feature combines both checks
- [ ] toggle_feature updates correctly

### Phase 4: API Testing
- [ ] GET /api/admin/features returns all features
- [ ] POST /api/admin/features creates new feature
- [ ] POST /api/admin/features/{code}/toggle works
- [ ] Role permissions API works
- [ ] Audit logs are created

### Phase 5: Integration Testing
- [ ] Student signup disabled when AUTH_STUDENT_SIGNUP disabled
- [ ] Authority always has access (bypass)
- [ ] Role permissions are enforced
- [ ] Audit log captures all actions

### Phase 6: UI Testing
- [ ] Feature list displays correctly
- [ ] Toggle switches work
- [ ] Role permission matrix editable
- [ ] Search and filter work

---

## Quick Reference

### Import Feature Service
```python
from app.services.feature_service import FeatureService
```

### Check Feature in Endpoint
```python
@router.get("/endpoint")
async def my_endpoint(current_user: User = Depends(get_current_user)):
    if not await FeatureService.check_feature_enabled("FEATURE_CODE"):
        raise HTTPException(403, "Feature disabled")
```

### Add Feature Check to Endpoint
```python
from app.middleware.feature_check import require_feature

@router.post("/students", dependencies=[Depends(require_feature("STUDENT_ENROLLMENT", "create"))])
async def create_student(...):
```

---

## File Locations

| Component | File Path |
|-----------|-----------|
| Models | `app/models/admin_models.py` |
| Repository | `app/repositories/feature_repository.py` |
| Service | `app/services/feature_service.py` |
| API Endpoints | `app/api/endpoints/admin_features.py` |
| Dashboard | `app/api/endpoints/admin_dashboard.py` |
| Middleware | `app/middleware/feature_check.py` |
| Templates | `app/templates/admin/` |
| Seed Script | `scripts/setup/seed_features.py` |

---

## Need Help?

If you get lost, refer to this checklist:

1. ✅ Created admin_models.py
2. ✅ Updated app/models/__init__.py
3. ✅ Created feature_repository.py
4. ✅ Created feature_service.py
5. ✅ Created admin_features.py endpoint
6. ✅ Created admin_dashboard.py endpoint
7. ✅ Registered routes in main.py
8. ✅ Created middleware/feature_check.py
9. ✅ Added feature checks to existing endpoints
10. ✅ Created templates
11. ✅ Created seed script
12. ✅ Tested everything

---

**Last Updated:** 2026-02-26
**Version:** 1.0
