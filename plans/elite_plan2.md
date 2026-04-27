# 🏫 ELITE PLAN 2 — School Modules Migration (Simple First)
## Phase: SCHOOL CORE — authority, teacher, student, parent, library, attendance
### Goal: Migrate 6 core school modules with 100% accuracy

---

## 📌 Pre-Conditions (from Plan 1)
- [ ] ✅ Full backup exists
- [ ] ✅ `old/app/` reference copy exists
- [ ] ✅ `modules/shared/` imports cleanly
- [ ] ✅ All module folders have `__init__.py`
- [ ] ✅ `uvicorn app.main:app --reload` runs clean

> ⚠️ **Golden Rule:** After each module is migrated and wired, run the app and test THAT module's endpoints before moving to the next one.

---

## 🗺️ Migration Order (Simplest → Complex)

| Order | Module | Source Files | Complexity |
|-------|--------|-------------|-----------|
| 1 | `school_authority` | authority.py (model, schema, service, api) | Simple |
| 2 | `school_teacher` | teacher.py across models/schemas/services | Simple |
| 3 | `school_parent` | parent.py across layers | Simple |
| 4 | `school_library` | library_models, library_service, library_repository | Medium |
| 5 | `school_attendance` | attendance across layers | Medium |
| 6 | `school_student` | student.py (most complex — cross-module deps) | Complex |

---

## 📁 Module Structure Template

Every module must follow **exactly** this structure:

```
modules/
└── school_authority/
    ├── __init__.py
    ├── models.py        ← SQLAlchemy models from app/models/school/authority.py
    ├── schemas.py       ← Pydantic schemas from app/schemas/authority.py
    ├── repository.py    ← DB operations (new, extracted from admin_user_repository.py)
    ├── service.py       ← Business logic from app/services/authority_service.py
    ├── api.py           ← FastAPI routes from app/api/endpoints/authority.py
    └── tests/
        └── test_authority.py
```

---

## 📋 MODULE 1: `school_authority`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_authority/models.py` | `app/models/school/authority.py` |
| `modules/school_authority/schemas.py` | `app/schemas/authority.py` |
| `modules/school_authority/service.py` | `app/services/authority_service.py` |
| `modules/school_authority/api.py` | `app/api/endpoints/authority.py` |

### Import Fix Rules for This Module

**In `models.py`:**
```python
# CHANGE THIS:
from app.models.base import Base
# TO THIS:
from modules.shared.base import Base
```

**In `repository.py`:**
```python
# CHANGE THIS:
from app.core.database import get_db
from app.models.school.authority import AuthorityUser
# TO THIS:
from modules.shared.database import get_db
from modules.school_authority.models import AuthorityUser
```

**In `service.py`:**
```python
# CHANGE THIS:
from app.repositories.admin_user_repository import AdminUserRepository
# TO THIS:
from modules.school_authority.repository import AuthorityRepository
```

**In `api.py`:**
```python
# CHANGE THIS:
from app.services.authority_service import AuthorityService
from app.schemas.authority import AuthorityCreate, AuthorityResponse
# TO THIS:
from modules.school_authority.service import AuthorityService
from modules.school_authority.schemas import AuthorityCreate, AuthorityResponse
```

### Wire into app/main.py (ADD but KEEP old routes too)
```python
# In app/main.py — ADD these lines (don't remove old routes yet):
from modules.school_authority.api import router as school_authority_router
app.include_router(school_authority_router, prefix="/api/v2/school", tags=["v2 - School Authority"])
```

> ℹ️ We use `/api/v2/school` prefix so old routes at `/api/v1/` keep working. After verification, we switch v2 → v1.

### Verification
```powershell
# 1. App starts:
uvicorn app.main:app --reload

# 2. New routes visible:
# Visit http://localhost:8000/docs → look for "v2 - School Authority" section

# 3. Test endpoint:
curl http://localhost:8000/api/v2/school/authority/
```

---

## 📋 MODULE 2: `school_teacher`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_teacher/models.py` | `app/models/school/teacher.py` |
| `modules/school_teacher/schemas.py` | `app/schemas/teacher.py` |
| `modules/school_teacher/repository.py` | `app/repositories/teacher_repository.py` |
| `modules/school_teacher/service.py` | `app/services/teacher_service.py` |
| `modules/school_teacher/api.py` | `app/api/endpoints/teachers.py` |

### Key Import Changes

**In `models.py`:**
```python
# OLD:
from app.models.base import Base
from app.models.models import User
# NEW:
from modules.shared.base import Base
from modules.shared.models import User   # or use direct import if User is in shared
```

**In `repository.py`:**
```python
# OLD:
from app.models.school.teacher import Teacher
from app.core.database import get_db
# NEW:
from modules.school_teacher.models import Teacher
from modules.shared.database import get_db
```

**In `service.py`:**
```python
# OLD:
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.teacher import TeacherCreate, TeacherUpdate
# NEW:
from modules.school_teacher.repository import TeacherRepository
from modules.school_teacher.schemas import TeacherCreate, TeacherUpdate
```

### Wire into app/main.py
```python
from modules.school_teacher.api import router as school_teacher_router
app.include_router(school_teacher_router, prefix="/api/v2/school", tags=["v2 - School Teacher"])
```

---

## 📋 MODULE 3: `school_parent`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_parent/models.py` | `app/models/school/parent.py` |
| `modules/school_parent/schemas.py` | `app/schemas/parent.py` |
| `modules/school_parent/repository.py` | `app/repositories/parent_repository.py` |
| `modules/school_parent/service.py` | `app/services/parent_service.py` |
| `modules/school_parent/api.py` | `app/api/endpoints/parents.py` |

> ℹ️ Parent model likely depends on Student. Keep this dependency noted:
> - `modules/school_parent/models.py` may ForeignKey to Student table
> - Reference by table name string `"students"` not by import to avoid circular deps

---

## 📋 MODULE 4: `school_library`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_library/models.py` | `app/models/library_models.py` |
| `modules/school_library/schemas.py` | `app/schemas/library_schemas.py` |
| `modules/school_library/repository.py` | `app/repositories/library_repository.py` |
| `modules/school_library/service.py` | `app/services/library_service.py` |
| `modules/school_library/api.py` | `app/api/endpoints/library.py` |

> ⚠️ **Note:** `library_models.py` is shared between school and college. In this phase, copy it for school_library. In college_library (Plan 4), we'll reuse with a context flag.

---

## 📋 MODULE 5: `school_attendance`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_attendance/models.py` | `app/models/models.py` (extract attendance-related classes only) |
| `modules/school_attendance/schemas.py` | `app/schemas/attendance.py` |
| `modules/school_attendance/repository.py` | `app/repositories/attendance_repository.py` |
| `modules/school_attendance/service.py` | `app/services/attendance_service.py` |
| `modules/school_attendance/api.py` | `app/api/endpoints/attendance.py` |

> ⚠️ **Attention:** `app/models/models.py` (18628 bytes, large!) contains many models mixed together. Only extract the attendance-related models. Do NOT copy the whole file.

**How to identify attendance models:**
```powershell
# Find attendance-related class names:
Select-String -Path "app\models\models.py" -Pattern "class.*Attendance"
```

---

## 📋 MODULE 6: `school_student`

### Source Files to Copy
| Destination | Source in app/ |
|-------------|---------------|
| `modules/school_student/models.py` | `app/models/school/student.py` |
| `modules/school_student/schemas.py` | `app/schemas/student.py` |
| `modules/school_student/repository.py` | `app/repositories/student_repository.py` |
| `modules/school_student/service.py` | `app/services/student_service.py` (14517 bytes — LARGE) |
| `modules/school_student/api.py` | `app/api/endpoints/students.py` (14172 bytes) |

> ⚠️ **WARNING:** `student_service.py` is 14517 bytes and `students.py` is 14172 bytes. These are the most complex files. Migrate last within this plan. Read them fully before migrating.

> ⚠️ **Circular Dependency Risk:** Student likely depends on Teacher (homeroom), Parent (guardian), and Attendance. Use string-based ForeignKey references.

---

## 🔧 Rapid Migration Script

Use this to copy files quickly (adjust paths as needed):

**File: `scripts/migrate_school_simple.py`**
```python
"""
Script: scripts/migrate_school_simple.py
Purpose: Copy school module source files into module structure
Run AFTER manually reviewing each file for correctness.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

COPIES = [
    # school_authority
    ("app/models/school/authority.py",   "modules/school_authority/models.py"),
    ("app/schemas/authority.py",          "modules/school_authority/schemas.py"),
    ("app/services/authority_service.py", "modules/school_authority/service.py"),
    ("app/api/endpoints/authority.py",    "modules/school_authority/api.py"),
    # school_teacher
    ("app/models/school/teacher.py",     "modules/school_teacher/models.py"),
    ("app/schemas/teacher.py",            "modules/school_teacher/schemas.py"),
    ("app/repositories/teacher_repository.py", "modules/school_teacher/repository.py"),
    ("app/services/teacher_service.py",   "modules/school_teacher/service.py"),
    ("app/api/endpoints/teachers.py",     "modules/school_teacher/api.py"),
    # school_parent
    ("app/models/school/parent.py",      "modules/school_parent/models.py"),
    ("app/schemas/parent.py",             "modules/school_parent/schemas.py"),
    ("app/repositories/parent_repository.py", "modules/school_parent/repository.py"),
    ("app/services/parent_service.py",    "modules/school_parent/service.py"),
    ("app/api/endpoints/parents.py",      "modules/school_parent/api.py"),
    # school_library
    ("app/models/library_models.py",     "modules/school_library/models.py"),
    ("app/schemas/library_schemas.py",    "modules/school_library/schemas.py"),
    ("app/repositories/library_repository.py", "modules/school_library/repository.py"),
    ("app/services/library_service.py",   "modules/school_library/service.py"),
    ("app/api/endpoints/library.py",      "modules/school_library/api.py"),
    # school_attendance
    ("app/schemas/attendance.py",         "modules/school_attendance/schemas.py"),
    ("app/repositories/attendance_repository.py", "modules/school_attendance/repository.py"),
    ("app/services/attendance_service.py","modules/school_attendance/service.py"),
    ("app/api/endpoints/attendance.py",   "modules/school_attendance/api.py"),
    # school_student
    ("app/models/school/student.py",     "modules/school_student/models.py"),
    ("app/schemas/student.py",            "modules/school_student/schemas.py"),
    ("app/repositories/student_repository.py", "modules/school_student/repository.py"),
    ("app/services/student_service.py",   "modules/school_student/service.py"),
    ("app/api/endpoints/students.py",     "modules/school_student/api.py"),
]

for src, dst in COPIES:
    src_path = ROOT / src
    dst_path = ROOT / dst
    if not src_path.exists():
        print(f"⚠️  MISSING SOURCE: {src}")
        continue
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"✅ Copied: {src} → {dst}")

print("\n⚠️  Remember: Now fix all imports in each copied file!")
```

---

## 📊 Phase 2 Completion Checklist

For each module (`school_authority`, `school_teacher`, `school_parent`, `school_library`, `school_attendance`, `school_student`):

- [ ] Source files copied into module folder
- [ ] All imports updated from `app.*` → `modules.*`
- [ ] Module has `models.py`, `schemas.py`, `repository.py`, `service.py`, `api.py`
- [ ] Router wired into `app/main.py` under `/api/v2/school` prefix
- [ ] `uvicorn app.main:app --reload` runs without errors
- [ ] Module endpoints show up in http://localhost:8000/docs
- [ ] At least one GET endpoint tested and returns 200

---

## 🔜 What Comes Next (Plan 3)

Plan 3 handles the **complex school modules** that require merging multiple files:
- `school_exam_section` (merge exam_models + test_models + exam_service + test_service)
- `school_account_section` (merge account_models + fee model + multiple repositories + services)
