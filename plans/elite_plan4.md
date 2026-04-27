# 🎓 ELITE PLAN 4 — College Modules Migration
## Phase: COLLEGE MODULES — All 12 college modules
### Goal: Migrate all college-specific modules with 100% accuracy

---

## 📌 Pre-Conditions (from Plan 3)
- [ ] ✅ All 8 school modules migrated and verified
- [ ] ✅ All school modules route under /api/v2/school/
- [ ] ✅ `verify_module.py` shows zero old imports for school modules
- [ ] ✅ App runs with zero errors

---

## 🗺️ College Modules Overview

| Module | Complexity | Source Status |
|--------|-----------|--------------|
| `college_faculty` | Medium | Has dedicated model + api files |
| `college_student` | Medium | Has model + enrollment model |
| `college_hod` | Medium | Has model + department logic |
| `college_dean` | Low | No dedicated model — build minimal |
| `college_registrar` | High | Has models; API/service need building from scratch |
| `college_exam_section` | High | Shares exam_models.py with school — must split |
| `college_account_section` | High | Shares admin_finance_service.py — must split |
| `college_library` | Medium | Shares library logic with school — context-aware copy |
| `college_placement` | Medium | Model exists; service+api need building |
| `college_research` | Medium | Model exists; service+api need building |
| `college_hostel` | Medium | Model exists (3204 bytes) — full build needed |
| `college_lab` | Medium | Model exists (2370 bytes) — full build needed |

---

## 📋 MODULE 9: `college_faculty`

### Source Files
| Destination | Source in app/ |
|-------------|---------------|
| `modules/college_faculty/models.py` | `app/models/college/faculty.py` |
| `modules/college_faculty/schemas.py` | `app/schemas/college_faculty.py` |
| `modules/college_faculty/repository.py` | Extract from `app/repositories/admin_user_repository.py` (faculty parts only) |
| `modules/college_faculty/service.py` | Extract from `app/services/admin_user_service.py` (faculty parts) |
| `modules/college_faculty/api.py` | `app/api/v1/college/faculty.py` (if exists) OR build from endpoints |

### Finding Faculty Parts in admin_user_repository.py
```powershell
# Find faculty-specific methods:
Select-String -Path "app\repositories\admin_user_repository.py" -Pattern "(faculty|Faculty)"
```

### Import Fix Template
```python
# modules/college_faculty/models.py
from modules.shared.base import Base
# from app.models.college.faculty import Faculty → NO
# → define Faculty class here directly

# modules/college_faculty/repository.py
from modules.college_faculty.models import Faculty
from modules.shared.database import get_db

# modules/college_faculty/schemas.py
# Use app/schemas/college_faculty.py as source
# All pydantic models for faculty operations

# modules/college_faculty/api.py
from modules.college_faculty.service import FacultyService
from modules.college_faculty.schemas import FacultyCreate, FacultyResponse
router = APIRouter()
```

### Wire into main.py
```python
from modules.college_faculty.api import router as college_faculty_router
app.include_router(college_faculty_router, prefix="/api/v2/college", tags=["v2 - College Faculty"])
```

---

## 📋 MODULE 10: `college_student`

### Source Files
| Destination | Source in app/ |
|-------------|---------------|
| `modules/college_student/models.py` | `app/models/college/student.py` |
| `modules/college_student/models_enrollment.py` → merge → `models.py` | `app/models/college/enrollment.py` |
| `modules/college_student/schemas.py` | `app/schemas/college_student.py` |
| `modules/college_student/repository.py` | Extract from `app/repositories/student_repository.py` (college parts) |
| `modules/college_student/service.py` | Extract from `app/services/student_service.py` (college parts, 14517 bytes) |
| `modules/college_student/api.py` | `app/api/v1/college/students.py` (if exists) |

### ⚠️ Split student_service.py Carefully
`student_service.py` is 14517 bytes and handles BOTH school and college students. Before copying:

```powershell
# Find college-specific methods in student_service.py:
Select-String -Path "app\services\student_service.py" -Pattern "(college|College|enrollment|Enrollment)"
# Find school-specific methods:
Select-String -Path "app\services\student_service.py" -Pattern "(school|School|class_room|homeroom)"
```

### Merge enrollment into student models
```python
# modules/college_student/models.py
from modules.shared.base import Base
from sqlalchemy import ...

# ── From college/student.py ─────────────────────────
class CollegeStudent(Base):
    __tablename__ = "college_students"
    ...

# ── From college/enrollment.py ──────────────────────
class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id = Column(Integer, ForeignKey("college_students.id"))
    ...
```

---

## 📋 MODULE 11: `college_hod`

### Source Files
| Destination | Source in app/ |
|-------------|---------------|
| `modules/college_hod/models.py` | `app/models/college/department.py` + extract from `app/models/department_models.py` |
| `modules/college_hod/schemas.py` | `app/schemas/department_schemas.py` |
| `modules/college_hod/repository.py` | `app/repositories/department_repository.py` |
| `modules/college_hod/service.py` | `app/services/department_service.py` |
| `modules/college_hod/api.py` | `app/api/endpoints/hod.py` (1356 bytes — small, likely minimal) |

### Merge department models
```python
# modules/college_hod/models.py
# Merge app/models/college/department.py + app/models/department_models.py
# Remove duplicates
# Example:
class Department(Base):
    __tablename__ = "departments"
    ...

class DepartmentCourse(Base):
    # from department_models.py if different from college/department.py
    ...
```

---

## 📋 MODULE 12: `college_dean`

### Special Case: No Dedicated Model Yet
As noted in `elite_migration.md`: *"This role may not have dedicated models yet."*

**Strategy:** Build a minimal module that delegates to `college_faculty` with a `role="dean"` filter.

```python
# modules/college_dean/models.py
# Dean uses the Faculty model with role flag
# No separate table needed at this stage

# Option A: Re-export Faculty model
from modules.college_faculty.models import Faculty
Dean = Faculty  # alias

# Option B: Minimal placeholder
# (Nothing needed if Dean is just a role filter)
```

```python
# modules/college_dean/api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.college_faculty.models import Faculty

router = APIRouter()

@router.get("/dean/profile")
def get_dean(db: Session = Depends(get_db)):
    # Return faculty member with role='dean'
    dean = db.query(Faculty).filter(Faculty.role == "dean").first()
    return dean
```

---

## 📋 MODULE 13: `college_registrar`

### High Complexity: Needs New Service + API Built

```
app/models/college/program.py   ─┐
app/models/college/semester.py  ─┤──→ modules/college_registrar/models.py (MERGE)
app/models/college/course.py    ─┘

app/schemas/course.py           ──→ modules/college_registrar/schemas.py

app/repositories/course_repository.py ──→ modules/college_registrar/repository.py

                                    Service + API → BUILD FROM SCRATCH
```

### Building service.py from scratch
```python
# modules/college_registrar/service.py
from modules.college_registrar.repository import RegistrarRepository
from modules.college_registrar.schemas import ProgramCreate, SemesterCreate, CourseCreate

class RegistrarService:
    def __init__(self, db):
        self.repo = RegistrarRepository(db)

    def create_program(self, data: ProgramCreate):
        return self.repo.create_program(data)

    def get_all_programs(self):
        return self.repo.get_all_programs()

    def create_semester(self, program_id: int, data: SemesterCreate):
        return self.repo.create_semester(program_id, data)

    def assign_course(self, semester_id: int, data: CourseCreate):
        return self.repo.assign_course(semester_id, data)
```

### Building api.py from scratch
```python
# modules/college_registrar/api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.college_registrar.service import RegistrarService
from modules.college_registrar.schemas import ProgramCreate, SemesterCreate

router = APIRouter()

@router.get("/programs/")
def list_programs(db: Session = Depends(get_db)):
    return RegistrarService(db).get_all_programs()

@router.post("/programs/")
def create_program(data: ProgramCreate, db: Session = Depends(get_db)):
    return RegistrarService(db).create_program(data)

@router.get("/semesters/")
def list_semesters(db: Session = Depends(get_db)):
    return RegistrarService(db).get_all_semesters()
```

### Merge registrar models
```python
# modules/college_registrar/models.py
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

# From college/program.py
class Program(Base):
    __tablename__ = "programs"
    ...

# From college/semester.py
class Semester(Base):
    __tablename__ = "semesters"
    program_id = Column(Integer, ForeignKey("programs.id"))
    ...

# From college/course.py
class Course(Base):
    __tablename__ = "courses"
    ...
```

---

## 📋 MODULE 14: `college_exam_section`

### ⚠️ SPLIT from school_exam_section — Critical Step

`exam_models.py` is used by BOTH school and college. In Plan 3, we already copied it for school. Now we need **college-specific exam logic only**.

```powershell
# Find college-specific exam logic:
Select-String -Path "app\services\exam_service.py" -Pattern "(college|College|grade_point|GPA|credit)"
```

```python
# modules/college_exam_section/models.py
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# College exams may include GPA / credit hours
class CollegeExam(Base):
    __tablename__ = "college_exams"
    ...

class CollegeGrade(Base):
    __tablename__ = "college_grades"
    gpa = Column(Float)
    credit_hours = Column(Integer)
    ...
```

Wire into main.py:
```python
from modules.college_exam_section.api import router as college_exam_router
app.include_router(college_exam_router, prefix="/api/v2/college", tags=["v2 - College Exam"])
```

---

## 📋 MODULE 15: `college_account_section`

### Source (College-Only Parts)
```python
# modules/college_account_section/models.py
# From app/models/college/fee.py
class CollegeFee(Base):
    __tablename__ = "college_fees"
    ...

# modules/college_account_section/service.py
# COLLEGE-ONLY methods from app/services/admin_finance_service.py
class CollegeFinanceService:
    # Only college-related fee operations
```

---

## 📋 MODULE 16: `college_library`

### Shared with school_library — Context-Aware Copy
```python
# modules/college_library/models.py
# Same Book, Borrow models as school_library
# But add college-specific fields if any (e.g., research_reference)

# modules/college_library/service.py
# Same logic but different borrow rules (e.g., longer loan period for college)
```

---

## 📋 MODULES 17-20: Stub-to-Full Build (placement, research, hostel, lab)

These 4 modules have models but no service/api. Build them in a consistent pattern:

### Template for Each
```python
# models.py → COPY from app/models/college/<name>.py
# schemas.py → BUILD new (derive fields from model columns)
# repository.py → BUILD standard CRUD
# service.py → BUILD wrapping repository
# api.py → BUILD standard CRUD routes
```

#### `college_placement` (models from `app/models/college/placement.py`, 2789 bytes)
```python
# api.py routes:
GET  /placement/opportunities
POST /placement/register
GET  /placement/my-applications
POST /placement/apply/{opportunity_id}
```

#### `college_research` (models from `app/models/college/research.py`, 2367 bytes)
```python
# api.py routes:
GET  /research/projects
POST /research/projects
GET  /research/publications
POST /research/publications
```

#### `college_hostel` (models from `app/models/college/hostel.py`, 3204 bytes)
```python
# api.py routes:
GET  /hostel/rooms
POST /hostel/rooms
GET  /hostel/allocations
POST /hostel/allocate/{room_id}
```

#### `college_lab` (models from `app/models/college/lab.py`, 2370 bytes)
```python
# api.py routes:
GET  /labs/
POST /labs/
GET  /labs/{id}/schedule
POST /labs/{id}/book
```

---

## 📊 Phase 4 Completion Checklist

For each of the 12 college modules:
- [ ] `models.py` created (copied or built)
- [ ] `schemas.py` created (copied or built)
- [ ] `repository.py` created
- [ ] `service.py` created
- [ ] `api.py` created with router
- [ ] Wired into `app/main.py` under `/api/v2/college` prefix
- [ ] `verify_module.py <module_name>` shows zero old imports
- [ ] Routes appear in http://localhost:8000/docs

### Specific college checks:
- [ ] `college_dean` uses `college_faculty.models.Faculty` with role filter
- [ ] `college_registrar` has new service + api built from scratch
- [ ] `college_exam_section` has college-specific exam logic, not school copies
- [ ] `college_account_section` has ONLY college parts of admin_finance_service
- [ ] `college_placement`, `college_research`, `college_hostel`, `college_lab` all have working CRUD

---

## 🔜 What Comes Next (Plan 5)

Plan 5 is the **Cutover & Cleanup Phase**:
- Switch all routes from `/api/v1/` (old) to `/api/v2/` (new, modules-based)
- Remove old router registrations from `app/main.py`
- Run full test suite
- Final cleanup and verification
