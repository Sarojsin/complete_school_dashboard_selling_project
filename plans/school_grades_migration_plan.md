# Plan: Migrate school_grades Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_grades/)
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
| `backup/models/models.py` | Grade class with student_id, course_id, grade_type, score, max_score, grade, remarks |
| `backup/models/school/grade.py` | SchoolGrade model (if exists) |
| `backup/schemas/grade.py` | GradeBase, GradeCreate, GradeUpdate, GradeResponse |
| `backup/repositories/grade_repository.py` | GradeRepository with create, get, get_by_student, get_by_course, get_all |
| `backup/api/endpoints/grades.py` | Grades API endpoints |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/models.py` (Grade class lines ~250-266)
**Target:** `modules/school/school_grades/models.py`

```python
# Expected structure:
class Grade(Base):
    __tablename__ = "school_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    grade_type = Column(String(50))  # midterm, final, quiz, assignment
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    grade = Column(String(5))  # A, B+, B, etc.
    remarks = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("SchoolStudent", back_populates="school_grades")
    course = relationship("SchoolCourse", back_populates="grades")
```

### Step 2: Create `schemas.py`
**Source:** `backup/schemas/grade.py`
**Target:** `modules/school/school_grades/schemas.py`

```python
# Expected schemas:
class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade_type: Optional[str] = None
    score: float
    max_score: float
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeUpdate(BaseModel):
    score: Optional[float] = None
    max_score: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeResponse(GradeBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/grade_repository.py`
**Target:** `modules/school/school_grades/repository.py`

Methods needed:
- `create(grade_data)` - Create new grade
- `get(grade_id)` - Get grade by ID
- `get_by_student(student_id)` - Get grades by student
- `get_by_course(course_id)` - Get grades by course
- `get_all(filters)` - Get all grades with filters
- `update(grade_id, data)` - Update grade
- `delete(grade_id)` - Delete grade

### Step 4: Create `api.py`
**Source:** `backup/api/endpoints/grades.py` or from web routers
**Target:** `modules/school/school_grades/api.py`

Endpoints needed:
- `POST /` - Create grade
- `GET /{id}` - Get grade
- `GET /` - List grades (with filters: student_id, course_id, grade_type)
- `PUT /{id}` - Update grade
- `DELETE /{id}` - Delete grade
- `GET /student/{student_id}` - Get student grades
- `GET /course/{course_id}` - Get course grades

### Step 5: Create `router.py`
**Target:** `modules/school/school_grades/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| Grade class | Create with table name "school_grades" |
| Relationships | Add student and course relationships |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| GradeBase | student_id, course_id, grade_type, score, max_score, grade, remarks |
| GradeCreate | All required fields |
| GradeUpdate | Optional fields for partial update |
| GradeResponse | All fields with id and date |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create | Insert new grade record |
| get | Fetch grade by ID |
| get_by_student | Fetch grades for a student |
| get_by_course | Fetch grades for a course |
| get_all | List with pagination and filters |
| update | Modify existing grade |
| delete | Remove grade record |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST / | Add new grade |
| GET /{id} | Get grade details |
| GET / | List grades |
| PUT /{id} | Update grade |
| DELETE /{id} | Delete grade |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.schemas.grade import ...` | `from .schemas import ...` |
| `from backup.repositories.grade_repository import ...` | Create new repository |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules
