# Migration Phase 7: Database Separation

**Duration:** 3-5 days  
**Goal:** Migrate from single SQLite database to separate PostgreSQL databases

---

## Overview

Phase 7 implements the database separation strategy, moving from a single database to three separate PostgreSQL databases for better isolation and scalability.

---

## Target Architecture

```
PostgreSQL Server
├── school_db        (School data)
│   ├── authorities
│   ├── teachers
│   ├── students
│   ├── parents
│   ├── courses
│   ├── exams
│   └── ...
│
├── college_db       (College data)
│   ├── faculty
│   ├── students
│   ├── programs
│   ├── semesters
│   ├── enrollments
│   ├── placements
│   └── ...
│
└── auth_db          (Shared authentication)
    ├── users
    ├── roles
    ├── permissions
    └── sessions
```

---

## Step-by-Step Tasks

### Step 1: Setup PostgreSQL

#### 1.1 Install PostgreSQL
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# On Windows
# Download from https://www.postgresql.org/download/windows/
```

#### 1.2 Create Databases
```sql
CREATE DATABASE school_db;
CREATE DATABASE college_db;
CREATE DATABASE auth_db;
```

#### 1.3 Create Database User
```sql
CREATE USER school_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;
GRANT ALL PRIVILEGES ON DATABASE college_db TO school_user;
GRANT ALL PRIVILEGES ON DATABASE auth_db TO school_user;
```

---

### Step 2: Configure Database Connections

#### 2.1 Update Config
**Modify: `app/core/config.py`**
```python
class Settings(BaseSettings):
    # Auth Database
    AUTH_DATABASE_URL: str = "postgresql://school_user:password@localhost/auth_db"
    
    # School Database  
    SCHOOL_DATABASE_URL: str = "postgresql://school_user:password@localhost/school_db"
    
    # College Database
    COLLEGE_DATABASE_URL: str = "postgresql://school_user:password@localhost/college_db"
    
    # Legacy (for migration)
    DATABASE_URL: str = "sqlite:///./school_management.db"
```

#### 2.2 Create Database Engines
**Modify: `app/core/database.py`**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create separate engines
school_engine = create_engine(Settings.SCHOOL_DATABASE_URL)
college_engine = create_engine(Settings.COLLEGE_DATABASE_URL)
auth_engine = create_engine(Settings.AUTH_DATABASE_URL)

# Create session factories
SchoolSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=school_engine)
CollegeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=college_engine)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

# Base for models
Base = declarative_base()

# Separate bases for each database
SchoolBase = declarative_base()
CollegeBase = declarative_base()
AuthBase = declarative_base()
```

---

### Step 3: Create Session Dependencies

#### 3.1 School Session Dependency
**Create: `app/dependencies/school_db.py`**
```python
from typing import Generator
from app.core.database import SchoolSessionLocal

def get_school_db() -> Generator:
    db = SchoolSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 3.2 College Session Dependency
**Create: `app/dependencies/college_db.py`**
```python
from typing import Generator
from app.core.database import CollegeSessionLocal

def get_college_db() -> Generator:
    db = CollegeSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 3.3 Auth Session Dependency
**Create: `app/dependencies/auth_db.py`**
```python
from typing import Generator
from app.core.database import AuthSessionLocal

def get_auth_db() -> Generator:
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### Step 4: Restructure Models for Multi-DB

#### 4.1 Mark Models with Base

**School Models: `app/models/school/__init__.py`**
```python
from app.core.database import SchoolBase

class Authority(SchoolBase):
    __tablename__ = "authorities"
    # ...
```

**College Models: `app/models/college/__init__.py`**
```python
from app.core.database import CollegeBase

class CollegeStudent(CollegeBase):
    __tablename__ = "college_students"
    # ...
```

**Auth Models: `app/models/auth/__init__.py`**
```python
from app.core.database import AuthBase

class User(AuthBase):
    __tablename__ = "users"
    # ...
```

#### 4.2 Update Model Imports

In all endpoint files:
```python
# Old
from app.models.models import Student

# New - School
from app.models.school import Student

# New - College
from app.models.college import CollegeStudent
```

---

### Step 5: Update Repositories for Multi-DB

#### 5.1 School Repository
**Create: `app/repositories/school/student_repository.py`**
```python
from sqlalchemy.orm import Session
from app.models.school import Student

class SchoolStudentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Student).all()
```

#### 5.2 College Repository
**Create: `app/repositories/college/student_repository.py`**
```python
from sqlalchemy.orm import Session
from app.models.college import CollegeStudent

class CollegeStudentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(CollegeStudent).all()
```

#### 5.3 Auth Repository
**Create: `app/repositories/auth/user_repository.py`**
```python
from sqlalchemy.orm import Session
from app.models.auth import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
```

---

### Step 6: Create Migration Script

#### 6.1 Data Export Script
**Create: `scripts/migrate_to_postgres.py`**
```python
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to SQLite
sqlite_conn = sqlite3.connect('school_management.db')

# Read data
def export_table(table_name):
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    return columns, data

# For each table:
# 1. Export from SQLite
# 2. Import to appropriate PostgreSQL database
```

#### 6.2 Migration Command
**Create: `app/commands/migrate.py`**
```python
import click

@click.command()
def migrate():
    """Migrate data to separate databases"""
    click.echo("Starting migration...")
    
    # Migrate school data
    migrate_school_data()
    
    # Migrate college data
    migrate_college_data()
    
    # Migrate auth data
    migrate_auth_data()
    
    click.echo("Migration complete!")
```

---

### Step 7: Update API Endpoints

#### 7.1 School Endpoints
**Modify: `app/api/v1/school/students.py`**
```python
from fastapi import Depends
from app.dependencies.school_db import get_school_db

@router.get("/")
async def list_students(
    db: Session = Depends(get_school_db)
):
    repo = SchoolStudentRepository(db)
    return repo.get_all()
```

#### 7.2 College Endpoints
**Modify: `app/api/v1/college/students.py`**
```python
from fastapi import Depends
from app.dependencies.college_db import get_college_db

@router.get("/")
async def list_students(
    db: Session = Depends(get_college_db)
):
    repo = CollegeStudentRepository(db)
    return repo.get_all()
```

#### 7.3 Auth Endpoints
**Modify: `app/api/v1/auth.py`**
```python
from fastfast import Depends
from app.dependencies.auth_db import get_auth_db

@router.post("/login")
async def login(
    credentials: LoginSchema,
    db: Session = Depends(get_auth_db)
):
    repo = UserRepository(db)
    # Auth logic
```

---

### Step 8: Database Connection Pooling

**Modify: `app/core/database.py`**
```python
from sqlalchemy.pool import QueuePool

school_engine = create_engine(
    Settings.SCHOOL_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

college_engine = create_engine(
    Settings.COLLEGE_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

---

## Configuration Files

### Docker Compose (Optional)
**Create: `docker-compose.postgres.yml`**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: school_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: school_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Files to Modify Summary

| File | Changes |
|------|---------|
| `app/core/config.py` | Add database URLs |
| `app/core/database.py` | Create separate engines |
| `app/dependencies/school_db.py` | NEW - School session |
| `app/dependencies/college_db.py` | NEW - College session |
| `app/dependencies/auth_db.py` | NEW - Auth session |
| `app/models/school/__init__.py` | Use SchoolBase |
| `app/models/college/__init__.py` | Use CollegeBase |
| `app/models/auth/__init__.py` | NEW - AuthBase |
| All endpoint files | Update imports & dependencies |

---

## Verification Checklist

- [ ] PostgreSQL installed
- [ ] Three databases created
- [ ] Database engines configured
- [ ] Session dependencies working
- [ ] Models use correct bases
- [ ] Repositories use correct sessions
- [ ] Migration script works
- [ ] Data properly separated
- [ ] Authentication working

---

## Rollback Plan

If issues occur:
1. Keep SQLite as fallback
2. Use feature flag to switch between databases
3. Keep legacy DATABASE_URL for rollback

---

## Next Phase

After Phase 7 → Go to [Phase 8: Testing & Deployment](migration_phase8.md)

---

*End of Phase 7*
