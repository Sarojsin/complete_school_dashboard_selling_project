# Migration Phase 4: Restructure API Endpoints

**Duration:** 2-3 days  
**Goal:** Organize API endpoints into v1 structure with school/college separation

---

## Overview

Phase 4 reorganizes the API endpoints to follow the new versioned structure with clear separation between school and college endpoints.

---

## Current State

```
app/api/
└── endpoints/
    ├── auth.py           # Auth endpoints
    ├── students.py       # Student endpoints
    ├── teachers.py      # Teacher endpoints
    ├── authority.py     # Authority endpoints
    ├── parents.py       # Parent endpoints
    ├── courses.py       # Mixed course endpoints
    ├── exams.py        # Exam endpoints
    ├── fees.py         # Fee endpoints
    ├── library.py      # Library endpoints
    ├── hod.py          # HOD endpoints
    ├── groups.py       # Group endpoints
    ├── admin_*.py      # Admin endpoints
    └── ...
```

---

## Target State After Phase 4

```
app/api/
└── v1/                    # ← NEW: Versioned API
    ├── __init__.py
    ├── auth.py            # Shared auth
    ├── school/           # ← NEW: School endpoints
    │   ├── __init__.py
    │   ├── students.py
    │   ├── teachers.py
    │   ├── authorities.py
    │   ├── parents.py
    │   ├── courses.py
    │   ├── exams.py
    │   ├── fees.py
    │   ├── library.py
    │   ├── attendance.py
    │   └── groups.py
    │
    └── college/          # ← NEW: College endpoints
        ├── __init__.py
        ├── students.py
        ├── faculty.py
        ├── deans.py
        ├── hod.py
        ├── registrars.py
        ├── courses.py
        ├── semesters.py
        ├── programs.py
        ├── enrollments.py
        ├── exams.py
        ├── fees.py
        ├── library.py
        ├── placements.py
        ├── research.py
        ├── hostels.py
        ├── labs.py
        ├── attendance.py
        └── groups.py
```

---

## Step-by-Step Tasks

### Step 1: Create v1 Directory Structure

Create folders:
```
app/api/v1/
app/api/v1/school/
app/api/v1/college/
```

### Step 2: Create __init__.py Files

**Create: `app/api/v1/__init__.py`**
```python
from fastapi import APIRouter

api_router = APIRouter()

# Import and include sub-routers
from app.api.v1 import auth, school, college

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(school.router, prefix="/school", tags=["School"])
api_router.include_router(college.router, prefix="/college", tags=["College"])

__all__ = ["api_router"]
```

### Step 3: Create School API Router

**Create: `app/api/v1/school/__init__.py`**
```python
from fastapi import APIRouter

router = APIRouter()

# Import school endpoints
from app.api.v1.school import students, teachers, authorities, parents

router.include_router(students.router, tags=["Students"])
router.include_router(teachers.router, tags=["Teachers"])
router.include_router(authorities.router, tags=["Authorities"])
router.include_router(parents.router, tags=["Parents"])

__all__ = ["router"]
```

### Step 4: Move/Copy School Endpoints

#### 4.1 Students → School Students

**Copy from: `app/api/endpoints/students.py`**  
**To: `app/api/v1/school/students.py`**

Modify imports:
```python
# Old
from app.models.models import Student

# New
from app.models.school import Student
```

Add prefix in router:
```python
router = APIRouter(prefix="/students")
```

#### 4.2 Teachers → School Teachers

**Copy from: `app/api/endpoints/teachers.py`**  
**To: `app/api/v1/school/teachers.py`**

#### 4.3 Authority → School Authority

**Copy from: `app/api/endpoints/authority.py`**  
**To: `app/api/v1/school/authorities.py`**

#### 4.4 Parents → School Parents

**Copy from: `app/api/endpoints/parents.py`**  
**To: `app/api/v1/school/parents.py`**

#### 4.5 Courses → School Courses

**Copy from: `app/api/endpoints/courses.py`**  
**To: `app/api/v1/school/courses.py`**

#### 4.6 Fees → School Fees

**Copy from: `app/api/endpoints/fees.py`**  
**To: `app/api/v1/school/fees.py`**

#### 4.7 Library → School Library

**Copy from: `app/api/endpoints/library.py`**  
**To: `app/api/v1/school/library.py`**

### Step 5: Create College API Router

**Create: `app/api/v1/college/__init__.py`**
```python
from fastapi import APIRouter

router = APIRouter()

# Import college endpoints
from app.api.v1.college import (
    students, faculty, deans, hod, registrars,
    courses, programs, semesters, enrollments
)

router.include_router(students.router, tags=["College Students"])
router.include_router(faculty.router, tags=["Faculty"])
router.include_router(deans.router, tags=["Deans"])
router.include_router(hod.router, tags=["HOD"])
router.include_router(registrars.router, tags=["Registrars"])

__all__ = ["router"]
```

### Step 6: Create College Endpoints

#### 6.1 College Students
**Create: `app/api/v1/college/students.py`**
```python
from fastapi import APIRouter, Depends
from app.models.college import CollegeStudent
from app.schemas import StudentResponse

router = APIRouter(prefix="/students")

@router.get("/")
async def list_students():
    # College-specific implementation
    pass

@router.get("/{id}")
async def get_student(id: int):
    # College-specific implementation
    pass

@router.post("/")
async def create_student():
    # College-specific implementation
    pass
```

#### 6.2 Faculty
**Create: `app/api/v1/college/faculty.py`**
```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/faculty")

@router.get("/")
async def list_faculty():
    pass

@router.post("/")
async def create_faculty():
    pass
```

#### 6.3 Programs
**Create: `app/api/v1/college/programs.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/programs")

@router.get("/")
async def list_programs():
    pass

@router.post("/")
async def create_program():
    pass
```

#### 6.4 Semesters
**Create: `app/api/v1/college/semesters.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/semesters")

@router.get("/")
async def list_semesters():
    pass

@router.post("/")
async def create_semester():
    pass
```

#### 6.5 Enrollments
**Create: `app/api/v1/college/enrollments.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/enrollments")

@router.get("/")
async def list_enrollments():
    pass

@router.post("/")
async def create_enrollment():
    pass
```

#### 6.6 Placement (NEW)
**Create: `app/api/v1/college/placements.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/placements")

@router.get("/companies")
async def list_companies():
    pass

@router.get("/jobs")
async def list_jobs():
    pass

@router.post("/apply")
async def apply_job():
    pass
```

#### 6.7 Research (NEW)
**Create: `app/api/v1/college/research.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/research")

@router.get("/projects")
async def list_projects():
    pass

@router.get("/publications")
async def list_publications():
    pass
```

#### 6.8 Hostel (NEW)
**Create: `app/api/v1/college/hostels.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/hostels")

@router.get("/rooms")
async def list_rooms():
    pass

@router.post("/allocate")
async def allocate_room():
    pass
```

#### 6.9 Labs (NEW)
**Create: `app/api/v1/college/labs.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/labs")

@router.get("/")
async def list_labs():
    pass

@router.get("/bookings")
async def list_bookings():
    pass
```

### Step 7: Update main.py

**Modify: `app/main.py`**

Replace old endpoint registration:
```python
# OLD WAY
from app.api.endpoints import students, teachers, authority
app.include_router(students.router, prefix="/api/students")
app.include_router(teachers.router, prefix="/api/teachers")
```

With new:
```python
# NEW WAY
from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")
```

---

## Endpoint Mapping

| Old Endpoint | New Endpoint |
|--------------|--------------|
| `/api/students` | `/api/v1/school/students` |
| `/api/teachers` | `/api/v1/school/teachers` |
| `/api/authority` | `/api/v1/school/authorities` |
| `/api/parents` | `/api/v1/school/parents` |
| `/api/courses` | `/api/v1/school/courses` |
| `/api/fees` | `/api/v1/school/fees` |
| `/api/hod` | `/api/v1/college/hod` |
| (new) | `/api/v1/college/faculty` |
| (new) | `/api/v1/college/programs` |
| (new) | `/api/v1/college/placements` |

---

## Files to Create

| File | Purpose |
|------|---------|
| `app/api/v1/__init__.py` | Main v1 router |
| `app/api/v1/school/__init__.py` | School router |
| `app/api/v1/college/__init__.py` | College router |
| `app/api/v1/school/students.py` | School students |
| `app/api/v1/school/teachers.py` | School teachers |
| `app/api/v1/school/authorities.py` | School authorities |
| `app/api/v1/school/parents.py` | School parents |
| `app/api/v1/college/students.py` | College students |
| `app/api/v1/college/faculty.py` | Faculty |
| `app/api/v1/college/programs.py` | Programs |
| `app/api/v1/college/semesters.py` | Semesters |
| `app/api/v1/college/enrollments.py` | Enrollments |
| `app/api/v1/college/placements.py` | Placements |
| `app/api/v1/college/research.py` | Research |
| `app/api/v1/college/hostels.py` | Hostels |
| `app/api/v1/college/labs.py` | Labs |

---

## Verification Checklist

- [ ] v1 directory created
- [ ] School router working
- [ ] College router working
- [ ] All old endpoints still work (or redirect)
- [ ] New endpoints responding
- [ ] Authentication working
- [ ] main.py updated

---

## Backward Compatibility

Keep old endpoints working during transition:
```python
# In main.py - add redirect
@app.get("/api/students")
async def redirect_students():
    return RedirectResponse("/api/v1/school/students")
```

---

## Next Phase

After Phase 4 → Go to [Phase 5: Restructure Templates](migration_phase5.md)

---

*End of Phase 4*
