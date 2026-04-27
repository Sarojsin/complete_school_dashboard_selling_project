# Migration Phase 3: Create Module Structure

**Duration:** 3-5 days  
**Goal:** Create modular structure for each role (authority, teacher, student, etc.)

---

## Overview

Phase 3 creates the modular folder structure where each role (authority, teacher, student, etc.) becomes a complete module with its own models, repositories, services, APIs, and templates.

---

## Target Module Structure

Each module follows this pattern:
```
module_name/
├── __init__.py
├── models.py          # Module-specific models (if any beyond base)
├── schemas.py         # Pydantic validation schemas
├── repository.py     # Data access layer
├── service.py        # Business logic
├── api.py            # API routes
├── constants.py      # Module constants
├── exceptions.py     # Custom exceptions
├── templates/        # HTML templates
│   ├── dashboard.html
│   ├── list.html
│   └── detail.html
└── tests/            # Unit tests
```

---

## School Modules to Create

```
app/modules/school/
├── authority/        # ← Create
├── teacher/          # ← Create
├── student/         # ← Create
├── parent/          # ← Create
├── exam_section/     # ← Move from existing
├── account_section/  # ← Move from existing
└── library/         # ← Move from existing
```

---

## College Modules to Create

```
app/modules/college/
├── dean/            # ← Create
├── hod/             # ← Move from existing
├── faculty/         # ← Create (similar to teacher)
├── student/         # ← Create (different from school)
├── registrar/       # ← Create
├── exam_section/     # ← Create (college version)
├── account_section/  # ← Create (college version)
├── library/         # ← Create (enhanced)
├── placement/       # ← Create (new)
├── research/        # ← Create (new)
├── hostel/          # ← Create (new)
└── lab/             # ← Create (new)
```

---

## Step-by-Step Tasks

### Step 1: Create School Authority Module

**Create folder: `app/modules/school/authority/`**

#### 1.1 Create __init__.py
```python
__all__ = ["router"]
```

#### 1.2 Create constants.py
```python
from enum import Enum

class AuthorityRole(str, Enum):
    PRINCIPAL = "PRINCIPAL"
    VICE_PRINCIPAL = "VICE_PRINCIPAL"
    ADMIN = "ADMIN"

SCOPE_ALL = "all"
SCOPE_DEPARTMENT = "department"
SCOPE_CLASS = "class"
```

#### 1.3 Create exceptions.py
```python
from fastapi import HTTPException

class AuthorityException(Exception):
    pass

class UnauthorizedAction(AuthorityException):
    pass

class PermissionDenied(AuthorityException):
    pass
```

#### 1.4 Create schemas.py
```python
from pydantic import BaseModel
from typing import Optional

class AuthorityBase(BaseModel):
    user_id: int
    position: str
    department: Optional[str] = None

class AuthorityCreate(AuthorityBase):
    pass

class AuthorityResponse(AuthorityBase):
    id: int
    
    class Config:
        from_attributes = True
```

#### 1.5 Create repository.py
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.school.authority import Authority

class AuthorityRepository:
    async def get_by_id(self, db: AsyncSession, id: int):
        result = await db.execute(select(Authority).where(Authority.id == id))
        return result.scalars().first()
    
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Authority))
        return result.scalars().all()
    
    # ... other methods
```

#### 1.6 Create service.py
```python
from app.modules.school.authority.repository import AuthorityRepository

class AuthorityService:
    def __init__(self):
        self.repo = AuthorityRepository()
    
    async def get_authority(self, db, id):
        return await self.repo.get_by_id(db, id)
    
    # ... business logic
```

#### 1.7 Create api.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/authorities", tags=["Authority"])

@router.get("/")
async def list_authorities(db: AsyncSession = Depends(get_db)):
    # Implementation
    pass

@router.post("/")
async def create_authority(...):
    # Implementation
    pass
```

#### 1.8 Create templates
Create basic template files:
- `templates/dashboard.html`
- `templates/list.html`

---

### Step 2: Create School Teacher Module

**Create folder: `app/modules/school/teacher/`**

Same structure as authority, with:
- Teacher-specific models
- Teacher-specific schemas
- Teacher-specific API endpoints

#### Key Components:
- `get_assigned_classes()` - Get classes teacher teaches
- `get_attendance_stats()` - Get attendance for classes
- `get_students()` - Get students in teacher's classes
- `mark_attendance()` - Mark attendance
- `submit_grades()` - Submit student grades

---

### Step 3: Create School Student Module

**Create folder: `app/modules/school/student/`**

#### Key Components:
- `get_profile()` - Get student profile
- `get_timetable()` - Get class schedule
- `get_assignments()` - Get homework
- `submit_assignment()` - Submit homework
- `get_grades()` - Get marks/grades
- `view_fees()` - View fee details
- `pay_fees()` - Make payment

---

### Step 4: Create School Parent Module

**Create folder: `app/modules/school/parent/`**

#### Key Components:
- `get_children()` - Get linked children
- `view_child_progress()` - View child's academic progress
- `view_child_attendance()` - View child's attendance
- `communicate_teacher()` - Message teachers

---

### Step 5: Move Existing Exam Section to School

**Create folder: `app/modules/school/exam_section/`**

Move and adapt existing exam functionality:
- Create exam
- Schedule exam
- Distribute papers
- Enter marks
- Publish results

---

### Step 6: Move Existing Account Section to School

**Create folder: `app/modules/school/account_section/`**

Move and adapt existing fee functionality:
- Create fee structure
- Generate bills
- Record payments
- Generate reports

---

### Step 7: Create College Modules

Now create college-specific modules:

#### 7.1 Dean Module
```
app/modules/college/dean/
```
- Department oversight
- Policy management
- Faculty evaluation
- Curriculum approval

#### 7.2 HOD Module
```
app/modules/college/hod/
```
- Department management
- Faculty assignment
- Course allocation
- Budget planning

#### 7.3 Faculty Module
```
app/modules/college/faculty/
```
- Course teaching
- Research
- Student mentorship
- Publications

#### 7.4 College Student Module
```
app/modules/college/student/
```
- Course registration
- GPA tracking
- Research projects
- Placements

#### 7.5 Registrar Module
```
app/modules/college/registrar/
```
- Enrollment management
- Transcripts
- Certificates
- Student records

#### 7.6 Exam Section (College)
```
app/modules/college/exam_section/
```
- Semester exams
- Grade calculation
- GPA/CGPA
- Transcripts

#### 7.7 Account Section (College)
```
app/modules/college/account_section/
```
- Per-credit fees
- Faculty salaries
- Research grants

#### 7.8 Library (Enhanced)
```
app/modules/college/library/
```
- Journals
- Digital resources
- Research papers

#### 7.9 Placement Cell (NEW)
```
app/modules/college/placement/
```
- Company management
- Job postings
- Applications
- Campus drives

#### 7.10 Research (NEW)
```
app/modules/college/research/
```
- Project management
- Publications
- Grants

#### 7.11 Hostel (NEW)
```
app/modules/college/hostel/
```
- Room allocation
- Mess management
- Complaints

#### 7.12 Lab (NEW)
```
app/modules/college/lab/
```
- Equipment management
- Lab bookings
- Inventory

---

## Files to Create Summary

### School Modules (7):
| Module | Files to Create |
|--------|---------------|
| authority | 8 files (init, constants, exceptions, schemas, repo, service, api, templates) |
| teacher | 8 files |
| student | 8 files |
| parent | 8 files |
| exam_section | 8 files |
| account_section | 8 files |
| library | 8 files |

### College Modules (12):
| Module | Files to Create |
|--------|---------------|
| dean | 8 files |
| hod | 8 files |
| faculty | 8 files |
| student | 8 files |
| registrar | 8 files |
| exam_section | 8 files |
| account_section | 8 files |
| library | 8 files |
| placement | 8 files |
| research | 8 files |
| hostel | 8 files |
| lab | 8 files |

---

## Key Implementation Details

### Repository Pattern
Each module has its own repository:
```python
class AuthorityRepository:
    async def get_by_id(self, db, id): ...
    async def get_all(self, db): ...
    async def create(self, db, data): ...
    async def update(self, db, id, data): ...
    async def delete(self, db, id): ...
```

### Service Layer
Business logic in service:
```python
class AuthorityService:
    def __init__(self):
        self.repo = AuthorityRepository()
    
    async def get_with_user(self, db, id):
        authority = await self.repo.get_by_id(db, id)
        # Add business logic
        return authority
```

### API Routes
Each module exports router:
```python
# authority/api.py
router = APIRouter()

@router.get("/")
async def list_authorities(...):
    ...

@router.post("/")
async def create_authority(...):
    ...
```

---

## Verification Checklist

- [ ] All school modules created
- [ ] All college modules created
- [ ] Each module has repository
- [ ] Each module has service
- [ ] Each module has API
- [ ] All imports working
- [ ] Application runs

---

## Next Phase

After Phase 3 → Go to [Phase 4: Restructure API Endpoints](migration_phase4.md)

---

*End of Phase 3*
