# Separate Database Architecture: School & College Systems

## Overview
Completely separate PostgreSQL databases with independent deployments:
- **school_db** - PostgreSQL database for school system
- **college_db** - PostgreSQL database for college system
- Each runs as independent deployment with its own backend

---
## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Landing Page                             │
│                   (Institution Selector)                    │
│            [School]              [College]                  │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│   School System       │           │   College System      │
│   ─────────────       │           │   ─────────────       │
│   Domain:             │           │   Domain:             │
│   school.example.com  │           │   college.example.com │
│                       │           │                       │
│   PostgreSQL:         │           │   PostgreSQL:          │
│   school_db           │           │   college_db          │
│                       │           │                       │
│   Same codebase       │           │   Same codebase       │
│   Different config    │           │   Different config    │
└───────────────────────┘           └───────────────────────┘
```
---

## Implementation Plan

### Task 1: Configuration Changes

**File: `app/core/config.py`** - Add:
```python
# Environment-based database configuration
SCHOOL_DATABASE_URL = os.getenv("SCHOOL_DATABASE_URL")
COLLEGE_DATABASE_URL = os.getenv("COLLEGE_DATABASE_URL")

# Current instance type
INSTITUTION_TYPE = os.getenv("INSTITUTION_TYPE", "school")  # "school" or "college"
```

**File: `app/core/database.py`** - Modify:
```python
def get_database_url():
    """Get database URL based on institution type"""
    institution_type = os.getenv("INSTITUTION_TYPE", "school")
    
    if institution_type == "college":
        return os.getenv("COLLEGE_DATABASE_URL")
    return os.getenv("SCHOOL_DATABASE_URL")
```
### Task 2: Environment Configuration

**For School Deployment:**
```bash
# .env.school
INSTITUTION_TYPE=school
DATABASE_URL=postgresql://user:pass@localhost:5432/school_db
SCHOOL_DATABASE_URL=postgresql://user:pass@localhost:5432/school_db
```

**For College Deployment:**
```bash
# .env.college
INSTITUTION_TYPE=college
DATABASE_URL=postgresql://user:pass@localhost:5432/college_db
COLLEGE_DATABASE_URL=postgresql://user:pass@localhost:5432/college_db
```
### Task 3: Landing Page with Institution Selector

**File: `app/templates/index.html`** - Create:
```html
<!-- Institution Selection Page -->
<div class="institution-selector">
    <h1>Welcome to Education Portal</h1>
    <p>Select your institution type:</p>
    
    <div class="institution-cards">
        <a href="/school" class="card school">
            <h2>School</h2>
            <p>Primary & Secondary Education</p>
        </a>
        
        <a href="/college" class="card college">
            <h2>College</h2>
            <p>Higher Education & University</p>
        </a>
    </div>
</div>
```
### Task 4: Separate Routes

**Modify: `app/main.py`** - Add institution-based routing:
```python
# Redirect based on path
@app.get("/school")
async def school_redirect():
    # Set school session and redirect to login
    response = RedirectResponse(url="/school/login")
    response.set_cookie("institution", "school", domain=request.url.hostname)
    return response

@app.get("/college")
async def college_redirect():
    response = RedirectResponse(url="/college/login")
    response.set_cookie("institution", "college", domain=request.url.hostname)
    return response

# Separate login routes
app.include_router(school_auth.router, prefix="/school/auth", tags=["School Auth"])
app.include_router(college_auth.router, prefix="/college/auth", tags=["College Auth"])
```

### Task 5: Separate Auth Endpoints

**New file: `app/api/endpoints/school_auth.py`** - Copy from auth.py:
```python
# School-specific authentication
router = APIRouter()
@router.post("/login")
async def school_login(...):
    # Use school_db
    ...
@router.post("/signup")
async def school_signup(...):
    # School-specific signup with school fields
    ...
```
**New file: `app/api/endpoints/college_auth.py`** - Modified:
```python
# College-specific authentication
router = APIRouter()

@router.post("/login")
async def college_login(...):
    # Use college_db
    ...

@router.post("/signup")
async def college_signup(...):
    # College-specific signup with college fields
    # (Program, Semester, Department instead of Grade/Class)
    ...
```
### Task 6: Separate Templates

**School Templates:** `app/templates/school/`
```
app/templates/school/
├── login.html
├── signup.html
├── base.html
├── student/
├── teacher/
├── parent/
├── authority/
└── admin/
```
**College Templates:** `app/templates/college/`
```
app/templates/college/
├── login.html
├── signup.html
├── base.html
├── student/
├── faculty/
├── hod/
├── dean/
├── registrar/
├── admin/
└── ...
```
### Task 7: Separate Web Routers

**New: `app/web/routers/school/`**
```
app/web/routers/school/
├── __init__.py
├── student.py
├── teacher.py
├── parent.py
├── authority.py
└── groups.py
```
**New: `app/web/routers/college/`**
```
app/web/routers/college/
├── __init__.py
├── student.py    # Different from school
├── faculty.py   # Different from teacher
├── hod.py
├── dean.py
├── registrar.py
└── groups.py    # Different - department groups
```

---
## Database Schema Differences

### School Database Tables
```sql
-- Students have grade_level, section
students (
    id, user_id, grade_level VARCHAR(20),  -- "Class 1", "Class 10A"
    section VARCHAR(10),
    ...
)
-- Courses are "Subjects"
courses (
    id, grade_level VARCHAR(20),  -- tied to class
    ...
)
```
### College Database Tables
```sql
-- Students have program_id, semester
students (
    id, user_id, program_id INT,
    semester VARCHAR(20),  -- "Fall 2024"
    ...
)

-- Courses have credits
courses (
    id, credits INT,
    program_id INT,
    ...
)
-- Additional college tables
programs (id, name, department_id, ...)
semesters (id, name, program_id, ...)
departments (id, name, hod_id, ...)
```
---
## Deployment Strategy

### Option 1: Single Server, Multiple Instances

```
# Docker Compose for School
school-app:
  image: education-system
  environment:
    - INSTITUTION_TYPE=school
    - DATABASE_URL=postgresql://school_db
  ports:
    - "8000:8000"
# Docker Compose for College  
college-app:
  image: education-system
  environment:
    - INSTITUTION_TYPE=college
    - DATABASE_URL=postgresql://college_db
  ports:
    - "8001:8000"
```
### Option 2: Separate Servers

```
Server 1: school.example.com
- school-app container
- school_db PostgreSQL
Server 2: college.example.com
- college-app container
- college_db PostgreSQL
```
### Option 3: Single App with Database Routing
```
# Single codebase, chooses DB based on domain
school.example.com → uses school_db
college.example.com → uses college_db

# Middleware detects subdomain and sets DB
```
---
## Recommended Approach
Given your requirements, I recommend **Option 1 or 2**:
- Same codebase (Django/FastAPI app)
- Environment variable controls database
- Separate deployments with separate PostgreSQL databases
### Benefits:
1. Complete isolation - no data mixing
2. Independent scaling
3. Different feature sets possible
4. Easier maintenance
5. Clear separation of concerns

---
## Files to Modify

| Category | Files |
|----------|-------|
| Config | `app/core/config.py`, `app/core/database.py` |
| Landing | `app/templates/index.html` |
| Routes | `app/main.py` |
| Auth | Create `app/api/endpoints/school_auth.py`, `app/api/endpoints/college_auth.py` |
| Templates | Create `app/templates/school/`, `app/templates/college/` |
| Web Routes | Create `app/web/routers/school/`, `app/web/routers/college/` |
---
## Migration Steps
1. **Current state**: Your existing SQLite database becomes school_db
2. **Create college_db**: New empty PostgreSQL database
3. **Update config**: Add database URL configuration
4. **Create landing page**: Institution selector
5. **Create separate routes**: /school/* and /college/*
6. **Deploy twice**: Once with INSTITUTION_TYPE=school, once with INSTITUTION_TYPE=college