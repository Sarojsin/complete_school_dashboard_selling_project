# 📐 Model Plan — Converting `model.md` Into a Modular Architecture

> **Purpose:** This document is a deep-research implementation guide for executing the structural
> migration described in `model.md`. It expands on the high-level mapping with concrete file
> inventories, dependency analysis, migration scripts, import-fix strategies, and a risk register.
>
> **Read alongside:** `plans/migration_plan.md`, `plans/migration_phase1.md` … `phase8.md`

---

## 1. Executive Summary

`model.md` proposes moving from a **flat `app/` monolith** to a **top-level `modules/` directory**
with 20 self-contained domain modules (7 school + 12 college + 1 shared core).  
A partial migration already exists under `app/modules/school/` and `app/modules/college/`, and
model files live in `app/models/school/` and `app/models/college/`.  

This plan bridges the gap: it audits what **already exists**, identifies what **must still be done**,
and provides **executable steps** with no ambiguity.

---

## 2. Current State Audit (What Already Exists)

### 2.1 Existing Model Files

| Location | Files Present |
|---|---|
| `app/models/` (root/flat) | `models.py`, `admin_models.py`, `account_models.py`, `chat_models.py`, `group_models.py`, `department_models.py`, `exam_models.py`, `library_models.py`, `test_models.py`, `base.py` |
| `app/models/school/` | `__init__.py`, `authority.py`, `class_model.py`, `fee.py`, `parent.py`, `student.py`, `teacher.py` |
| `app/models/college/` | `__init__.py`, `course.py`, `department.py`, `enrollment.py`, `faculty.py`, `fee.py`, `hostel.py`, `lab.py`, `placement.py`, `program.py`, `research.py`, `semester.py`, `student.py` |

### 2.2 Existing Repositories (32 files, all flat under `app/repositories/`)

```
account_repository.py         admin_academic_repository.py   admin_backup_repository.py
admin_exam_repository.py      admin_finance_repository.py    admin_message_repository.py
admin_notice_repository.py    admin_settings_repository.py   admin_system_repository.py
admin_user_repository.py      assignment_repository.py       attendance_repository.py
chat_repository.py            course_repository.py           dashboard_repository.py
department_repository.py      exam_repository.py             feature_repository.py
fee_repository.py             fee_structure_repository.py    grade_repository.py
group_post_repository.py      group_repository.py            library_repository.py
message_repository.py         notes_repository.py            notice_repository.py
parent_repository.py          student_repository.py          teacher_repository.py
test_repository.py            user_repository.py             videos_repository.py
```

### 2.3 Existing Services (28 files, all flat under `app/services/`)

```
account_service.py       admin_academic_service.py   admin_backup_service.py
admin_exam_service.py    admin_finance_service.py    admin_message_service.py
admin_notice_service.py  admin_system_service.py     admin_user_service.py
attendance_service.py    auth_service.py             authority_service.py
chat_cleanup_service.py  chat_service.py             dashboard_service.py
department_service.py    exam_service.py             feature_service.py
grade_service.py         group_post_service.py       group_service.py
library_service.py       notification_service.py     parent_service.py
password_policy_service.py  student_service.py       teacher_service.py
test_service.py
```

### 2.4 Existing Schemas (20 files, all flat under `app/schemas/`)

```
account_schemas.py  admin.py         assignment.py    attendance.py  auth.py
authority.py        course.py        department_schemas.py  exam_schemas.py  fee.py
grade.py            group.py         group_post.py    library_schemas.py  misc.py
notice.py           parent.py        student.py       teacher.py     user.py
```

### 2.5 Partial `app/modules/` Progress

| Path | Status |
|---|---|
| `app/modules/school/` | Folder exists; needs `api.py`, `web.py`, `service.py`, `repository.py` per sub-module |
| `app/modules/college/` | Folder exists; 28 children (partially built) |
| `app/modules/__init__.py` | Present |

### 2.6 `app/shared/` (Already Exists)

`app/shared/` already contains 10 children. This is good — Phase 1 is **partially done**.

---

## 3. Target Module Architecture (from `model.md`)

The final destination is a **top-level `modules/` directory** (NOT `app/modules/`) with:

```
modules/
├── shared/                    ← Core shared infrastructure
│   ├── __init__.py
│   ├── base.py                ← Base model, repository, service
│   ├── auth.py                ← JWT, permissions
│   ├── config.py              ← Configuration
│   ├── database.py            ← DB session
│   ├── exceptions.py          ← Common exceptions
│   └── utils.py               ← Helpers
│
│── school_authority/
├── school_teacher/
├── school_student/
├── school_parent/
├── school_exam_section/
├── school_account_section/
├── school_library/
├── school_attendance/
│
├── college_dean/
├── college_hod/
├── college_faculty/
├── college_student/
├── college_registrar/
├── college_exam_section/
├── college_account_section/
├── college_library/
├── college_placement/
├── college_research/
├── college_hostel/
└── college_lab/
```

Each module contains:

```
<module_name>/
├── __init__.py
├── models.py         ← SQLAlchemy models (merged from multiple sources)
├── schemas.py        ← Pydantic schemas
├── repository.py     ← DB CRUD layer
├── service.py        ← Business logic
├── api.py            ← FastAPI REST routes
├── web.py            ← Jinja2 HTML routes
├── constants.py      ← Module constants (if needed)
├── exceptions.py     ← Module-specific errors (if needed)
├── utils.py          ← Module helpers (if needed)
├── templates/        ← Jinja2 HTML templates
└── tests/            ← Unit + integration tests
```

---

## 4. Complete Source-to-Destination Mapping

### 4.1 `modules/shared/`

| Source File | Destination |
|---|---|
| `app/core/config.py` | `modules/shared/config.py` |
| `app/core/database.py` | `modules/shared/database.py` |
| `app/core/exceptions.py` | `modules/shared/exceptions.py` |
| `app/core/crypto.py` | `modules/shared/utils.py` |
| `app/dependencies/auth.py` | `modules/shared/auth.py` |
| `app/models/base.py` | `modules/shared/base.py` |
| `app/models/models.py` (User, Role) | `modules/shared/models.py` |
| `app/models/chat_models.py` | `modules/shared/chat.py` |
| `app/models/group_models.py` | `modules/shared/groups.py` |
| `app/shared/` (existing) | Merge into `modules/shared/` |

---

### 4.2 `modules/school_authority/`

| Source | Destination File |
|---|---|
| `app/models/school/authority.py` | `models.py` |
| `app/schemas/authority.py` | `schemas.py` |
| `app/repositories/admin_user_repository.py` *(authority parts)* | `repository.py` |
| `app/services/authority_service.py` | `service.py` |
| `app/api/endpoints/authority.py` | `api.py` |
| `app/web/routers/authority.py` | `web.py` |
| `app/templates/authority/` | `templates/` |
| `app/tests/test_authority_routes.py` | `tests/` |

---

### 4.3 `modules/school_teacher/`

| Source | Destination File |
|---|---|
| `app/models/school/teacher.py` | `models.py` |
| `app/schemas/teacher.py` | `schemas.py` |
| `app/repositories/teacher_repository.py` | `repository.py` |
| `app/services/teacher_service.py` | `service.py` |
| `app/api/endpoints/teachers.py` | `api.py` |
| `app/web/routers/teacher.py` | `web.py` |
| `app/templates/teacher/` | `templates/` |
| `app/tests/test_teacher_*.py` | `tests/` |

---

### 4.4 `modules/school_student/`

| Source | Destination File |
|---|---|
| `app/models/school/student.py` | `models.py` |
| `app/schemas/student.py` | `schemas.py` |
| `app/repositories/student_repository.py` | `repository.py` |
| `app/services/student_service.py` | `service.py` |
| `app/api/endpoints/students.py` | `api.py` |
| `app/web/routers/student.py` | `web.py` |
| `app/templates/student/` | `templates/` |
| `app/tests/test_student_*.py` | `tests/` |

---

### 4.5 `modules/school_parent/`

| Source | Destination File |
|---|---|
| `app/models/school/parent.py` | `models.py` |
| `app/schemas/parent.py` | `schemas.py` |
| `app/repositories/parent_repository.py` | `repository.py` |
| `app/services/parent_service.py` | `service.py` |
| `app/api/endpoints/parents.py` | `api.py` |
| `app/web/routers/parent.py` | `web.py` |
| `app/templates/parent/` | `templates/` |
| `app/tests/test_parent_*.py` | `tests/` |

---

### 4.6 `modules/school_exam_section/`

| Source | Destination File |
|---|---|
| `app/models/exam_models.py` | `models.py` (merge) |
| `app/models/test_models.py` | `models.py` (merge) |
| `app/schemas/exam_schemas.py` | `schemas.py` (merge) |
| `app/repositories/exam_repository.py` | `repository.py` (merge) |
| `app/repositories/test_repository.py` | `repository.py` (merge) |
| `app/services/exam_service.py` | `service.py` (merge) |
| `app/services/test_service.py` | `service.py` (merge) |
| `app/api/endpoints/exam_section.py` | `api.py` |
| `app/web/routers/exam_section.py` | `web.py` |
| `app/templates/exam_section/` | `templates/` |
| `app/tests/test_exam_*.py` | `tests/` |

---

### 4.7 `modules/school_account_section/`

| Source | Destination File |
|---|---|
| `app/models/account_models.py` | `models.py` (merge) |
| `app/models/school/fee.py` | `models.py` (merge) |
| `app/schemas/account_schemas.py` | `schemas.py` (merge) |
| `app/schemas/fee.py` | `schemas.py` (merge) |
| `app/repositories/account_repository.py` | `repository.py` (merge) |
| `app/repositories/fee_repository.py` | `repository.py` (merge) |
| `app/repositories/fee_structure_repository.py` | `repository.py` (merge) |
| `app/services/account_service.py` | `service.py` (merge) |
| `app/services/admin_finance_service.py` *(school fee parts)* | `service.py` |
| `app/api/endpoints/account.py` | `api.py` |
| `app/web/routers/account.py` | `web.py` |
| `app/templates/account/` | `templates/` |

---

### 4.8 `modules/school_library/`

| Source | Destination File |
|---|---|
| `app/models/library_models.py` | `models.py` |
| `app/schemas/library_schemas.py` | `schemas.py` |
| `app/repositories/library_repository.py` | `repository.py` |
| `app/services/library_service.py` | `service.py` |
| `app/api/endpoints/library.py` | `api.py` |
| `app/web/routers/library.py` | `web.py` |
| `app/templates/library/` | `templates/` |

---

### 4.9 `modules/school_attendance/`

| Source | Destination File |
|---|---|
| `app/models/attendance.py` *(if exists)* | `models.py` |
| `app/schemas/attendance.py` | `schemas.py` |
| `app/repositories/attendance_repository.py` | `repository.py` |
| `app/services/attendance_service.py` | `service.py` |
| `app/api/endpoints/attendance.py` | `api.py` |
| `app/web/routers/attendance.py` | `web.py` |
| `app/templates/attendance/` | `templates/` |

> **Note:** Attendance is split between `school_teacher` (basic mark-attendance) and
> `school_attendance` (monthly reports, analytics). Decide at coding time, and consolidate.

---

### 4.10 College Modules (12)

#### `modules/college_faculty/`
| Source | Destination |
|---|---|
| `app/models/college/faculty.py` | `models.py` |
| `app/schemas/teacher.py` *(faculty-specific parts)* | `schemas.py` |
| `app/repositories/admin_user_repository.py` *(faculty parts)* | `repository.py` |
| `app/services/admin_user_service.py` *(faculty parts)* | `service.py` |
| `app/api/v1/college/faculty.py` | `api.py` |
| `app/templates/college/faculty/` | `templates/` |

#### `modules/college_student/`
| Source | Destination |
|---|---|
| `app/models/college/student.py` | `models.py` |
| `app/models/college/enrollment.py` | `models.py` (merge) |
| `app/api/v1/college/students.py` | `api.py` |
| `app/templates/college/student/` | `templates/` |

#### `modules/college_dean/`
| Source | Destination |
|---|---|
| `app/models/models.py` *(Dean role entries)* | `models.py` |
| `app/api/v1/college/dean.py` | `api.py` |
| `app/templates/college/dean/` | `templates/` |

#### `modules/college_hod/`
| Source | Destination |
|---|---|
| `app/models/department_models.py` *(HOD parts)* | `models.py` |
| `app/models/college/department.py` | `models.py` (merge) |
| `app/schemas/department_schemas.py` | `schemas.py` |
| `app/repositories/department_repository.py` | `repository.py` |
| `app/services/department_service.py` | `service.py` |
| `app/api/v1/college/hod.py` | `api.py` |

#### `modules/college_registrar/`
| Source | Destination |
|---|---|
| `app/models/college/enrollment.py` *(registrar parts)* | `models.py` |
| `app/models/college/program.py` | `models.py` (merge) |
| `app/models/college/semester.py` | `models.py` (merge) |
| `app/models/college/course.py` | `models.py` (merge) |
| `app/schemas/course.py` | `schemas.py` |
| `app/repositories/course_repository.py` | `repository.py` |
| *(new)* | `service.py` |
| `app/api/v1/college/registrar.py` | `api.py` |

#### `modules/college_exam_section/`
| Source | Destination |
|---|---|
| `app/models/exam_models.py` *(college exam parts)* | `models.py` |
| `app/schemas/exam_schemas.py` *(college parts)* | `schemas.py` |
| `app/repositories/exam_repository.py` *(college parts)* | `repository.py` |
| `app/repositories/grade_repository.py` | `repository.py` (merge) |
| `app/services/exam_service.py` *(college parts)* | `service.py` |
| `app/services/grade_service.py` | `service.py` (merge) |
| `app/schemas/grade.py` | `schemas.py` (merge) |

#### `modules/college_account_section/`
| Source | Destination |
|---|---|
| `app/models/college/fee.py` | `models.py` |
| `app/repositories/fee_repository.py` *(college parts)* | `repository.py` |
| `app/services/admin_finance_service.py` *(college parts)* | `service.py` |

#### `modules/college_library/`
| Source | Destination |
|---|---|
| `app/models/library_models.py` *(shared with school, fork or re-use)* | `models.py` |
| `app/repositories/library_repository.py` | `repository.py` |
| `app/services/library_service.py` | `service.py` |

> **Decision point:** Library may share models between `school_library` and `college_library`.
> Options: (a) import from `modules/shared/library.py`, (b) duplicate for independent evolution.
> **Recommendation:** Keep a `shared/library_base.py` and extend per module.

#### `modules/college_placement/`
| Source | Destination |
|---|---|
| `app/models/college/placement.py` | `models.py` |
| *(new — needs full build)* | `repository.py`, `service.py`, `api.py`, `web.py` |

#### `modules/college_research/`
| Source | Destination |
|---|---|
| `app/models/college/research.py` | `models.py` |
| *(new — needs full build)* | `repository.py`, `service.py`, `api.py`, `web.py` |

#### `modules/college_hostel/`
| Source | Destination |
|---|---|
| `app/models/college/hostel.py` | `models.py` |
| *(new — needs full build)* | `repository.py`, `service.py`, `api.py`, `web.py` |

#### `modules/college_lab/`
| Source | Destination |
|---|---|
| `app/models/college/lab.py` | `models.py` |
| *(new — needs full build)* | `repository.py`, `service.py`, `api.py`, `web.py` |

---

## 5. Admin Module Decision

The 10 `admin_*` files (`admin_user_repository.py`, `admin_academic_service.py`, etc.) are
cross-cutting. They should be handled as follows:

| Admin File | Route to Module |
|---|---|
| `admin_user_repository/service` | **Split**: authority parts → `school_authority`, faculty parts → `college_faculty`, shared user parts → `shared` |
| `admin_academic_repository/service` | → `school_exam_section` + `college_exam_section` |
| `admin_finance_repository/service` | → `school_account_section` + `college_account_section` |
| `admin_exam_repository/service` | → `school_exam_section` |
| `admin_notice_repository/service` | → `shared` (notices are system-wide) |
| `admin_message_repository/service` | → `shared` |
| `admin_backup_repository/service` | → `shared` |
| `admin_settings_repository` | → `shared` |
| `admin_system_service` | → `shared` |
| Feature/notice management | → `shared` or new `admin_panel` module |

---

## 6. Shared / Cross-Cutting Resources

These do **NOT** belong to any single domain module and must stay in `modules/shared/`:

- **Chat:** `chat_models.py`, `chat_repository.py`, `chat_service.py`, `chat_cleanup_service.py`
- **Groups/Posts:** `group_models.py`, `group_repository.py`, `group_post_repository.py`, `group_service.py`, `group_post_service.py`
- **Auth:** `auth_service.py`, `dependencies/auth.py`, JWT handling
- **Notifications:** `notification_service.py`
- **Dashboard:** `dashboard_repository.py`, `dashboard_service.py` (aggregates data from all modules)
- **Password Policy:** `password_policy_service.py`
- **Feature flags:** `feature_repository.py`, `feature_service.py`

---

## 7. Full Migration Script (Production-Ready)

Save as `scripts/migrate_to_modules.py` and run from the project root:

```python
"""
Migration Script: Restructure app/ → modules/
Usage: python scripts/migrate_to_modules.py [--dry-run]
"""

import os
import sys
import shutil
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent  # project root

def cp(src: str, dst: str):
    s, d = ROOT / src, ROOT / dst
    if not s.exists():
        print(f"  ⚠️  MISSING: {src}")
        return
    if DRY_RUN:
        print(f"  [dry] {src} → {dst}")
        return
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
    print(f"  ✅  {src} → {dst}")


def mkdir(path: str):
    p = ROOT / path
    if DRY_RUN:
        print(f"  [dry] MKDIR {path}")
        return
    for sub in ["", "templates", "tests"]:
        (p / sub).mkdir(parents=True, exist_ok=True)
    (p / "__init__.py").touch(exist_ok=True)
    print(f"  📁  Created {path}")


# ── SHARED ──────────────────────────────────────────────────────────────────
SHARED = {
    "modules/shared": [
        ("app/core/config.py",            "config.py"),
        ("app/core/database.py",          "database.py"),
        ("app/core/exceptions.py",        "exceptions.py"),
        ("app/core/crypto.py",            "utils.py"),
        ("app/dependencies/auth.py",      "auth.py"),
        ("app/models/base.py",            "base.py"),
        ("app/models/models.py",          "models.py"),
        ("app/models/chat_models.py",     "chat.py"),
        ("app/models/group_models.py",    "groups.py"),
    ],
}

# ── SCHOOL MODULES ───────────────────────────────────────────────────────────
SCHOOL = {
    "modules/school_authority": [
        ("app/models/school/authority.py",          "models.py"),
        ("app/schemas/authority.py",                "schemas.py"),
        ("app/services/authority_service.py",       "service.py"),
        ("app/api/endpoints/authority.py",          "api.py"),
    ],
    "modules/school_teacher": [
        ("app/models/school/teacher.py",            "models.py"),
        ("app/schemas/teacher.py",                  "schemas.py"),
        ("app/repositories/teacher_repository.py",  "repository.py"),
        ("app/services/teacher_service.py",         "service.py"),
        ("app/api/endpoints/teachers.py",           "api.py"),
    ],
    "modules/school_student": [
        ("app/models/school/student.py",            "models.py"),
        ("app/schemas/student.py",                  "schemas.py"),
        ("app/repositories/student_repository.py",  "repository.py"),
        ("app/services/student_service.py",         "service.py"),
        ("app/api/endpoints/students.py",           "api.py"),
    ],
    "modules/school_parent": [
        ("app/models/school/parent.py",             "models.py"),
        ("app/schemas/parent.py",                   "schemas.py"),
        ("app/repositories/parent_repository.py",   "repository.py"),
        ("app/services/parent_service.py",          "service.py"),
        ("app/api/endpoints/parents.py",            "api.py"),
    ],
    "modules/school_exam_section": [
        ("app/models/exam_models.py",               "models.py"),
        ("app/schemas/exam_schemas.py",             "schemas.py"),
        ("app/repositories/exam_repository.py",     "repository.py"),
        ("app/services/exam_service.py",            "service.py"),
    ],
    "modules/school_account_section": [
        ("app/models/account_models.py",                   "models.py"),
        ("app/models/school/fee.py",                       "fee_models.py"),
        ("app/schemas/account_schemas.py",                 "schemas.py"),
        ("app/schemas/fee.py",                             "fee_schemas.py"),
        ("app/repositories/account_repository.py",         "repository.py"),
        ("app/repositories/fee_repository.py",             "fee_repository.py"),
        ("app/repositories/fee_structure_repository.py",   "fee_structure_repository.py"),
        ("app/services/account_service.py",                "service.py"),
    ],
    "modules/school_library": [
        ("app/models/library_models.py",            "models.py"),
        ("app/schemas/library_schemas.py",          "schemas.py"),
        ("app/repositories/library_repository.py",  "repository.py"),
        ("app/services/library_service.py",         "service.py"),
    ],
    "modules/school_attendance": [
        ("app/schemas/attendance.py",                   "schemas.py"),
        ("app/repositories/attendance_repository.py",   "repository.py"),
        ("app/services/attendance_service.py",          "service.py"),
    ],
}

# ── COLLEGE MODULES ──────────────────────────────────────────────────────────
COLLEGE = {
    "modules/college_faculty": [
        ("app/models/college/faculty.py",   "models.py"),
    ],
    "modules/college_student": [
        ("app/models/college/student.py",   "models.py"),
        ("app/models/college/enrollment.py", "enrollment_models.py"),
    ],
    "modules/college_hod": [
        ("app/models/college/department.py",        "models.py"),
        ("app/schemas/department_schemas.py",        "schemas.py"),
        ("app/repositories/department_repository.py","repository.py"),
        ("app/services/department_service.py",       "service.py"),
    ],
    "modules/college_registrar": [
        ("app/models/college/program.py",   "program_models.py"),
        ("app/models/college/semester.py",  "semester_models.py"),
        ("app/models/college/course.py",    "course_models.py"),
        ("app/schemas/course.py",           "schemas.py"),
        ("app/repositories/course_repository.py", "repository.py"),
    ],
    "modules/college_exam_section": [
        ("app/models/exam_models.py",               "models.py"),
        ("app/schemas/exam_schemas.py",             "schemas.py"),
        ("app/repositories/exam_repository.py",     "exam_repository.py"),
        ("app/repositories/grade_repository.py",    "grade_repository.py"),
        ("app/services/exam_service.py",            "exam_service.py"),
        ("app/services/grade_service.py",           "grade_service.py"),
        ("app/schemas/grade.py",                    "grade_schemas.py"),
    ],
    "modules/college_account_section": [
        ("app/models/college/fee.py",               "models.py"),
        ("app/repositories/fee_repository.py",      "repository.py"),
    ],
    "modules/college_library": [
        ("app/models/library_models.py",            "models.py"),
        ("app/repositories/library_repository.py",  "repository.py"),
        ("app/services/library_service.py",         "service.py"),
    ],
    "modules/college_placement": [
        ("app/models/college/placement.py",         "models.py"),
    ],
    "modules/college_research": [
        ("app/models/college/research.py",          "models.py"),
    ],
    "modules/college_hostel": [
        ("app/models/college/hostel.py",            "models.py"),
    ],
    "modules/college_lab": [
        ("app/models/college/lab.py",               "models.py"),
    ],
    "modules/college_dean": [],  # models extracted from models.py manually
}

if __name__ == "__main__":
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Starting migration...\n")
    ALL_MODULES = {**SHARED, **SCHOOL, **COLLEGE}
    for module_path, files in ALL_MODULES.items():
        print(f"\n📦 {module_path}")
        mkdir(module_path)
        for src, dst in files:
            cp(src, f"{module_path}/{dst}")
    print("\n✅ Done. Now manually merge split files and fix imports.")
```

---

## 8. Import Fix Strategy (Post-Migration)

After running the migration script, every file will still have old imports.
Use the following search-and-replace patterns:

### 8.1 Pattern Table

| Old Import | New Import |
|---|---|
| `from app.core.config import` | `from modules.shared.config import` |
| `from app.core.database import` | `from modules.shared.database import` |
| `from app.dependencies.auth import` | `from modules.shared.auth import` |
| `from app.models.models import` | `from modules.shared.models import` |
| `from app.models.base import` | `from modules.shared.base import` |
| `from app.models.school.teacher import` | `from modules.school_teacher.models import` |
| `from app.models.school.student import` | `from modules.school_student.models import` |
| `from app.models.school.authority import` | `from modules.school_authority.models import` |
| `from app.models.school.parent import` | `from modules.school_parent.models import` |
| `from app.models.college.faculty import` | `from modules.college_faculty.models import` |
| `from app.models.college.department import` | `from modules.college_hod.models import` |
| `from app.repositories.teacher_repository import` | `from modules.school_teacher.repository import` |
| `from app.repositories.student_repository import` | `from modules.school_student.repository import` |
| `from app.services.teacher_service import` | `from modules.school_teacher.service import` |
| `from app.services.student_service import` | `from modules.school_student.service import` |

### 8.2 Automated Import Fixer Script

Save as `scripts/fix_imports.py`:

```python
"""Fix imports after migration. Run from project root."""
import re
from pathlib import Path

REPLACEMENTS = [
    (r"from app\.core\.config import", "from modules.shared.config import"),
    (r"from app\.core\.database import", "from modules.shared.database import"),
    (r"from app\.core\.exceptions import", "from modules.shared.exceptions import"),
    (r"from app\.dependencies\.auth import", "from modules.shared.auth import"),
    (r"from app\.models\.base import", "from modules.shared.base import"),
    (r"from app\.models\.models import", "from modules.shared.models import"),
    (r"from app\.models\.school\.teacher import", "from modules.school_teacher.models import"),
    (r"from app\.models\.school\.student import", "from modules.school_student.models import"),
    (r"from app\.models\.school\.parent import", "from modules.school_parent.models import"),
    (r"from app\.models\.school\.authority import", "from modules.school_authority.models import"),
    (r"from app\.models\.college\.faculty import", "from modules.college_faculty.models import"),
    (r"from app\.models\.college\.department import", "from modules.college_hod.models import"),
    (r"from app\.repositories\.teacher_repository import", "from modules.school_teacher.repository import"),
    (r"from app\.repositories\.student_repository import", "from modules.school_student.repository import"),
    (r"from app\.repositories\.parent_repository import", "from modules.school_parent.repository import"),
    (r"from app\.services\.teacher_service import", "from modules.school_teacher.service import"),
    (r"from app\.services\.student_service import", "from modules.school_student.service import"),
    (r"from app\.services\.authority_service import", "from modules.school_authority.service import"),
]

files = list(Path("modules").rglob("*.py")) + list(Path("app").rglob("*.py"))
changed = 0
for fpath in files:
    content = fpath.read_text(encoding="utf-8", errors="ignore")
    new_content = content
    for old_pat, new_pat in REPLACEMENTS:
        new_content = re.sub(old_pat, new_pat, new_content)
    if new_content != content:
        fpath.write_text(new_content, encoding="utf-8")
        print(f"  Fixed: {fpath}")
        changed += 1
print(f"\n✅ Fixed {changed} files.")
```

---

## 9. `main.py` Router Registration (New Pattern)

After migration, update `app/main.py` router includes to:

```python
# ── School Modules ─────────────────────────────────────────
from modules.school_authority.api import router as school_authority_api
from modules.school_teacher.api import router as school_teacher_api
from modules.school_student.api import router as school_student_api
from modules.school_parent.api import router as school_parent_api
from modules.school_exam_section.api import router as school_exam_api
from modules.school_account_section.api import router as school_account_api
from modules.school_library.api import router as school_library_api
from modules.school_attendance.api import router as school_attendance_api

# ── College Modules ────────────────────────────────────────
from modules.college_dean.api import router as college_dean_api
from modules.college_hod.api import router as college_hod_api
from modules.college_faculty.api import router as college_faculty_api
from modules.college_student.api import router as college_student_api
from modules.college_registrar.api import router as college_registrar_api
from modules.college_exam_section.api import router as college_exam_api
from modules.college_account_section.api import router as college_account_api
from modules.college_library.api import router as college_library_api
from modules.college_placement.api import router as college_placement_api
from modules.college_research.api import router as college_research_api
from modules.college_hostel.api import router as college_hostel_api
from modules.college_lab.api import router as college_lab_api

# Register School
app.include_router(school_authority_api, prefix="/api/v1/school", tags=["School - Authority"])
app.include_router(school_teacher_api,   prefix="/api/v1/school", tags=["School - Teacher"])
app.include_router(school_student_api,   prefix="/api/v1/school", tags=["School - Student"])
app.include_router(school_parent_api,    prefix="/api/v1/school", tags=["School - Parent"])
app.include_router(school_exam_api,      prefix="/api/v1/school", tags=["School - Exam"])
app.include_router(school_account_api,   prefix="/api/v1/school", tags=["School - Account"])
app.include_router(school_library_api,   prefix="/api/v1/school", tags=["School - Library"])
app.include_router(school_attendance_api, prefix="/api/v1/school", tags=["School - Attendance"])

# Register College
app.include_router(college_dean_api,      prefix="/api/v1/college", tags=["College - Dean"])
app.include_router(college_hod_api,       prefix="/api/v1/college", tags=["College - HOD"])
app.include_router(college_faculty_api,   prefix="/api/v1/college", tags=["College - Faculty"])
app.include_router(college_student_api,   prefix="/api/v1/college", tags=["College - Student"])
app.include_router(college_registrar_api, prefix="/api/v1/college", tags=["College - Registrar"])
app.include_router(college_exam_api,      prefix="/api/v1/college", tags=["College - Exam"])
app.include_router(college_account_api,   prefix="/api/v1/college", tags=["College - Account"])
app.include_router(college_library_api,   prefix="/api/v1/college", tags=["College - Library"])
app.include_router(college_placement_api, prefix="/api/v1/college", tags=["College - Placement"])
app.include_router(college_research_api,  prefix="/api/v1/college", tags=["College - Research"])
app.include_router(college_hostel_api,    prefix="/api/v1/college", tags=["College - Hostel"])
app.include_router(college_lab_api,       prefix="/api/v1/college", tags=["College - Lab"])
```

---

## 10. Migration Execution Order (Step-by-Step)

Follow this order to minimize breakage:

```
Step 1  ──  Backup the entire project (git commit or zip)
Step 2  ──  Run: python scripts/migrate_to_modules.py --dry-run    (verify paths)
Step 3  ──  Run: python scripts/migrate_to_modules.py              (copy files)
Step 4  ──  Manually MERGE split files (exam, account, etc.) inside each module
Step 5  ──  Run: python scripts/fix_imports.py                     (update imports)
Step 6  ──  Manually fix any remaining import errors (check app/main.py first)
Step 7  ──  Update app/main.py router registrations (Section 9 above)
Step 8  ──  Run: python run.py                                     (smoke test)
Step 9  ──  Run: pytest tests/                                     (full test suite)
Step 10 ──  Clean up old app/repositories/, app/services/, app/schemas/ (after all tests pass)
```

---

## 11. Files That Still Need to Be Built From Scratch

These modules have models but **no service/repo/api** yet:

| Module | Missing Files |
|---|---|
| `college_placement` | `repository.py`, `service.py`, `api.py`, `web.py`, `schemas.py` |
| `college_research` | `repository.py`, `service.py`, `api.py`, `web.py`, `schemas.py` |
| `college_hostel` | `repository.py`, `service.py`, `api.py`, `web.py`, `schemas.py` |
| `college_lab` | `repository.py`, `service.py`, `api.py`, `web.py`, `schemas.py` |
| `college_dean` | `models.py` (extract from models.py), `repository.py`, `service.py`, `api.py` |
| `college_registrar` | `service.py`, `api.py` (partial) |
| `school_attendance` | `models.py` (check if exists separately or in teacher) |

---

## 12. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Circular imports between modules | High | High | Use `modules/shared/` for cross-cutting types; avoid cross-module imports |
| Duplicate models (e.g., `exam_models` used by both school and college) | High | Medium | Fork the model per module, or create `shared/exam_base.py` |
| Missing source files (paths in model.md that don't exist) | Medium | Medium | Dry-run script will print `⚠️ MISSING:` warnings |
| SQLAlchemy `Base` registry conflicts (same table in two modules) | Medium | High | All models must import from ONE `modules/shared/base.py` |
| Admin routes break during split | High | High | Keep old `app/api/endpoints/admin.py` until new admin module is wired |
| Test suite import failures | High | Medium | Update test imports in batch; run `pytest --co` to detect before running |
| `app/shared/` conflicts with `modules/shared/` | Low | Low | Merge / alias; keep `app/shared/` as backward-compat shim during transition |

---

## 13. Template Migration Map

| Current Template Dir | New Location |
|---|---|
| `app/templates/authority/` | `modules/school_authority/templates/` |
| `app/templates/teacher/` | `modules/school_teacher/templates/` |
| `app/templates/student/` | `modules/school_student/templates/` |
| `app/templates/parent/` | `modules/school_parent/templates/` |
| `app/templates/exam_section/` | `modules/school_exam_section/templates/` |
| `app/templates/account/` | `modules/school_account_section/templates/` |
| `app/templates/library/` | `modules/school_library/templates/` |
| `app/templates/attendance/` | `modules/school_attendance/templates/` |
| `app/templates/college/faculty/` | `modules/college_faculty/templates/` |
| `app/templates/college/hod/` | `modules/college_hod/templates/` |
| `app/templates/college/student/` | `modules/college_student/templates/` |
| `app/templates/base.html` | `app/templates/base.html` *(keep global)* |
| `app/templates/index.html` | `app/templates/index.html` *(keep global)* |

Update Jinja2 `TemplateResponse` path calls inside `web.py` files after moving templates.

---

## 14. Verification Checklist

- [ ] `modules/` directory created at project root
- [ ] All 20 module folders present with `__init__.py`
- [ ] `modules/shared/` has: `config.py`, `database.py`, `auth.py`, `base.py`, `models.py`, `exceptions.py`, `utils.py`
- [ ] Each school module has: `models.py`, `schemas.py`, `repository.py`, `service.py`, `api.py`
- [ ] Each college module has: `models.py` at minimum
- [ ] `python -c "from modules.shared.database import get_db"` runs without error
- [ ] `python -c "from modules.school_student.api import router"` runs without error
- [ ] `python run.py` starts without import errors
- [ ] `pytest tests/` passes (or known test failures documented)
- [ ] Old flat `app/repositories/`, `app/services/`, `app/schemas/` removed (final cleanup)

---

## 15. Estimated Timeline

| Task | Effort |
|---|---|
| Run migration script + dry-run verification | 0.5 day |
| Manual file merges (exam, account, library) | 1 day |
| Fix all imports | 1 day |
| Update `main.py` router registration | 0.5 day |
| Build missing college modules (placement, research, hostel, lab) | 3–5 days |
| Migrate templates + update web.py paths | 1 day |
| Fix test suite imports | 1 day |
| Smoke test + integration test | 1 day |
| **Total** | **~9–11 days** |

---

*Generated from deep research of `model.md`, `plans/migration_plan.md`, `plans/migration_phase*.md`,
and live source audit of `app/` directory — March 2026.*
