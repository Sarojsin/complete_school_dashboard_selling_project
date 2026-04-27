# Phase 1 Implementation Plan: Infrastructure & Core Setup

**Based on: Separate Database Architecture 2 (Comprehensive)**

---

## Phase 1 Focus: Infrastructure Foundation

This phase sets up the foundational infrastructure for the complete system.

---

## Task 1: PostgreSQL Database Setup

### 1.1 Create Databases
```bash
# Create both databases in PostgreSQL
psql -U postgres -c "CREATE DATABASE school_db;"
psql -U postgres -c "CREATE DATABASE college_db;"
psql -U postgres -c "CREATE DATABASE auth_db;"  # For shared authentication
```

### 1.2 Database Configuration
**File: `app/core/config.py`**
```python
class Settings(BaseSettings):
    # PostgreSQL Database URLs
    SCHOOL_DATABASE_URL: str = "postgresql://user:pass@localhost:5432/school_db"
    COLLEGE_DATABASE_URL: str = "postgresql://user:pass@localhost:5432/college_db"
    AUTH_DATABASE_URL: str = "postgresql://user:pass@localhost:5432/auth_db"
    
    # Current instance type
    INSTITUTION_TYPE: str = "school"  # "school" or "college"
    
    @property
    def DATABASE_URL(self) -> str:
        if self.INSTITUTION_TYPE == "college":
            return self.COLLEGE_DATABASE_URL
        return self.SCHOOL_DATABASE_URL
```

---

## Task 2: Shared Authentication Service

### 2.1 Auth Database Models
**File: `app/models/auth_models.py`**
```python
class AuthUser(Base):
    __tablename__ = "auth_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superadmin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Institution access - which systems user can access
    can_access_school = Column(Boolean, default=False)
    can_access_college = Column(Boolean, default=False)

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_users.id"))
    session_token = Column(String(500), unique=True)
    institution_type = Column(String(20))  # school, college, or None
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2.2 JWT Token with Institution Claim
**File: `app/core/auth.py`**
```python
def create_access_token(data: dict) -> str:
    """Create JWT with institution claim"""
    to_encode = data.copy()
    to_encode.update({
        "institution": data.get("institution", "school"),
        "type": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token payload:
# {
#     "sub": user_id,
#     "email": user@example.com,
#     "institution": "school",  # or "college" or "both"
#     "role": "student",
#     "exp": timestamp
# }
```

---

## Task 3: Landing Page & Institution Selector

### 3.1 Create Landing Page
**File: `app/templates/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Education Portal</title>
    <link rel="stylesheet" href="{{ static_url }}/css/base.css">
    <style>
        .hero { text-align: center; padding: 80px 20px; }
        .institution-selector { display: flex; justify-content: center; gap: 40px; margin-top: 60px; }
        .card { 
            padding: 60px 40px; border-radius: 16px; text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
        .school { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .college { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 80px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>Welcome to Education Portal</h1>
            <p class="lead">Select your institution to continue</p>
            
            <div class="institution-selector">
                <a href="/school/login" class="card school">
                    <h2>🏫 School</h2>
                    <p>Primary & Secondary Education</p>
                    <small>Classes 1-12</small>
                </a>
                
                <a href="/college/login" class="card college">
                    <h2>🎓 College</h2>
                    <p>Higher Education</p>
                    <small>Universities & Institutes</small>
                </a>
            </div>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>📚 Academic Management</h3>
                <p>Complete student information system</p>
            </div>
            <div class="feature">
                <h3>📊 Analytics</h3>
                <p>Performance tracking & reports</p>
            </div>
            <div class="feature">
                <h3>🔒 Secure</h3>
                <p>Role-based access control</p>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## Task 4: Separate Routes & Authentication

### 4.1 School Auth
**File: `app/api/endpoints/school_auth.py`**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.core.auth import verify_password, create_access_token

router = APIRouter(prefix="/school/api/auth", tags=["School Auth"])

@router.post("/login")
async def school_login(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_async_db)
):
    # 1. Verify against auth_db
    # 2. Check can_access_school permission
    # 3. Create token with institution="school"
    token = create_access_token({
        "sub": user.id,
        "email": user.email,
        "institution": "school",
        "role": user.school_role
    })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup")
async def school_signup(
    email: str,
    password: str,
    full_name: str,
    role: str,  # student, teacher, parent, authority
    grade_level: str,  # Class 1-12
    section: str,
    db: AsyncSession = Depends(get_async_db)
):
    # 1. Create in auth_db with can_access_school=True
    # 2. Create school-specific record in school_db
    ...
```

### 4.2 College Auth
**File: `app/api/endpoints/college_auth.py`**
```python
router = APIRouter(prefix="/college/api/auth", tags=["College Auth"])

@router.post("/login")
async def college_login(...):
    # Similar but with institution="college"
    ...

@router.post("/signup")
async def college_signup(
    email: str,
    password: str,
    full_name: str,
    role: str,  # student, faculty, hod, dean
    program_id: int,
    semester: str,
    db: AsyncSession = Depends(get_async_db)
):
    # 1. Create in auth_db with can_access_college=True
    # 2. Create college-specific record in college_db
    ...
```

---

## Task 5: Template Structure

### 5.1 School Templates
```
app/templates/school/
├── base.html
├── login.html
├── signup.html
├── student/
│   ├── dashboard.html
│   ├── timetable.html
│   ├── assignments.html
│   └── grades.html
├── teacher/
│   ├── dashboard.html
│   ├── attendance.html
│   └── assignments.html
├── parent/
│   └── dashboard.html
├── authority/
│   └── dashboard.html
└── admin/
    └── dashboard.html
```

### 5.2 College Templates
```
app/templates/college/
├── base.html
├── login.html
├── signup.html
├── student/
│   ├── dashboard.html
│   ├── courses.html
│   ├── grades.html
│   └── timetable.html
├── faculty/
│   ├── dashboard.html
│   └── courses.html
├── hod/
│   └── dashboard.html
├── dean/
│   └── dashboard.html
├── registrar/
│   └── dashboard.html
├── exam_section/
│   └── dashboard.html
├── library/
│   └── dashboard.html
└── account/
    └── dashboard.html
```

---

## Task 6: Environment Configuration

### 6.1 School Deployment
```bash
# .env.school
INSTITUTION_TYPE=school
DATABASE_URL=postgresql://user:pass@localhost:5432/school_db
AUTH_DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db
SECRET_KEY=your-secret-key
```

### 6.2 College Deployment
```bash
# .env.college
INSTITUTION_TYPE=college
DATABASE_URL=postgresql://user:pass@localhost:5432/college_db
AUTH_DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db
SECRET_KEY=your-secret-key
```

---

## Task 7: Migration Script

### 7.1 Migrate Existing Data to PostgreSQL
**File: `scripts/migrate_to_postgres.py`**
```python
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

async def migrate_school_data():
    # 1. Export from SQLite
    sqlite_conn = sqlite3.connect('school_db.sqlite')
    
    # 2. Import to PostgreSQL school_db
    pg_conn = psycopg2.connect("postgresql://user:pass@localhost:5432/school_db")
    
    # Migrate tables one by one
    tables = ['users', 'students', 'teachers', 'parents', 'courses', 'grades']
    for table in tables:
        # Export from SQLite
        df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
        
        # Import to PostgreSQL
        cols = df.columns.tolist()
        execute_values(
            cur,
            f"INSERT INTO {table} ({','.join(cols)}) VALUES %s",
            df.values
        )
```

---

## Implementation Order

1. ✅ PostgreSQL setup & database creation
2. ✅ Auth models & shared authentication
3. ✅ Landing page with institution selector
4. ✅ Separate auth endpoints (school/college)
5. ✅ Template structure
6. ✅ Environment configuration
7. ✅ Migration script

---

## Files to Create/Modify

| Category | Files |
|----------|-------|
| Models | `app/models/auth_models.py` |
| Config | `app/core/config.py` |
| Auth | `app/api/endpoints/school_auth.py`, `app/api/endpoints/college_auth.py` |
| Core | `app/core/auth.py` |
| Templates | `app/templates/index.html`, `app/templates/school/`, `app/templates/college/` |
| Scripts | `scripts/migrate_to_postgres.py` |

---

## Database Summary

| Database | Purpose | Tables |
|----------|---------|--------|
| **auth_db** | Shared authentication | auth_users, auth_sessions |
| **school_db** | School-specific data | users, students, teachers, courses, etc. |
| **college_db** | College-specific data | (to be created in Phase 2) |
