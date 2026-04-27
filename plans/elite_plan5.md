# 🏁 ELITE PLAN 5 — Final Cutover, Verification & Cleanup
## Phase: PRODUCTION READY — Switch to new modules, full test, clean old code
### Goal: Complete the migration with zero broken functionality

---

## 📌 Pre-Conditions (from Plans 1-4)
- [ ] ✅ All 20 modules migrated under `modules/`
- [ ] ✅ All module routers wired under `/api/v2/` prefix
- [ ] ✅ `verify_module.py` passes for all 20 modules (zero old imports)
- [ ] ✅ http://localhost:8000/docs shows ALL routes under v2
- [ ] ✅ Old app/ routes still work (safety net still in place)

---

## 🎯 Plan 5 Overview

```
Phase 5A — Full System Verification (v2 routes)
Phase 5B — Import Audit & Fix Residual Issues
Phase 5C — Switch main.py: remove v1 routes, upgrade v2 → v1
Phase 5D — Run Full Test Suite
Phase 5E — Cleanup: archive old code, final project structure
Phase 5F — Final Health Check
```

---

## 🔍 PHASE 5A — Full System Verification (All v2 Routes)

Before touching anything, document all existing v2 routes:

```powershell
# Start app and dump all routes:
python -c "
from app.main import app
for route in app.routes:
    if hasattr(route, 'methods'):
        for m in route.methods:
            print(f'{m:7} {route.path}')
" | Sort-Object
```

**Expected schema (v2 routes should include):**
```
GET     /api/v2/school/authority/
POST    /api/v2/school/authority/
GET     /api/v2/school/teachers/
POST    /api/v2/school/teachers/
GET     /api/v2/school/students/
GET     /api/v2/school/parents/
GET     /api/v2/school/library/
GET     /api/v2/school/attendance/
GET     /api/v2/school/exams/
GET     /api/v2/school/tests/
GET     /api/v2/school/account/
GET     /api/v2/school/fees/
GET     /api/v2/college/faculty/
GET     /api/v2/college/students/
GET     /api/v2/college/departments/
GET     /api/v2/college/dean/profile
GET     /api/v2/college/programs/
GET     /api/v2/college/exams/
GET     /api/v2/college/fees/
GET     /api/v2/college/library/
GET     /api/v2/college/placement/opportunities
GET     /api/v2/college/research/projects
GET     /api/v2/college/hostel/rooms
GET     /api/v2/college/labs/
```

Save this list. Every single route must return a valid HTTP response (200, 201, 401, or 404 are all acceptable — 500 is NOT).

### Smoke Test Script

**File: `scripts/smoke_test_v2.py`**
```python
"""
Script: scripts/smoke_test_v2.py
Run: python scripts/smoke_test_v2.py
Tests all v2 endpoints with unauthenticated GET requests.
Expects: 200 (OK), 401 (needs auth), 403 (forbidden), 404 (not found) = PASS
Fails on: 500 (internal server error) = FAIL
"""
import requests

BASE = "http://localhost:8000/api/v2"

ENDPOINTS = [
    # School
    f"{BASE}/school/authority/",
    f"{BASE}/school/teachers/",
    f"{BASE}/school/students/",
    f"{BASE}/school/parents/",
    f"{BASE}/school/library/",
    f"{BASE}/school/attendance/",
    f"{BASE}/school/exams/",
    f"{BASE}/school/tests/",
    f"{BASE}/school/account/",
    f"{BASE}/school/fees/",
    # College
    f"{BASE}/college/faculty/",
    f"{BASE}/college/students/",
    f"{BASE}/college/departments/",
    f"{BASE}/college/dean/profile",
    f"{BASE}/college/programs/",
    f"{BASE}/college/exams/",
    f"{BASE}/college/library/",
    f"{BASE}/college/placement/opportunities",
    f"{BASE}/college/research/projects",
    f"{BASE}/college/hostel/rooms",
    f"{BASE}/college/labs/",
]

print("🔍 Smoke Testing All v2 Endpoints...\n")
failed = []
for url in ENDPOINTS:
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 500:
            print(f"❌ FAIL 500: {url}")
            failed.append(url)
        else:
            print(f"✅ OK   {r.status_code}: {url}")
    except Exception as e:
        print(f"💥 ERROR: {url} → {e}")
        failed.append(url)

print(f"\n{'='*50}")
if failed:
    print(f"❌ {len(failed)} endpoints FAILED:")
    for f in failed:
        print(f"  {f}")
else:
    print(f"✅ All {len(ENDPOINTS)} endpoints passed smoke test!")
```

**Run:**
```powershell
# In one terminal: start the app
uvicorn app.main:app --port 8000

# In another terminal: run smoke test
python scripts/smoke_test_v2.py
```

**Required result:** Zero 500 errors before proceeding to Phase 5B.

---

## 🔧 PHASE 5B — Import Audit & Fix Residual Issues

Run the verify script for ALL modules:

```powershell
# Batch verify all modules:
$modules = @(
    "school_authority","school_teacher","school_student","school_parent",
    "school_exam_section","school_account_section","school_library","school_attendance",
    "college_faculty","college_student","college_hod","college_dean",
    "college_registrar","college_exam_section","college_account_section",
    "college_library","college_placement","college_research","college_hostel","college_lab"
)
foreach ($m in $modules) {
    python scripts/verify_module.py $m
}
```

**Fix any remaining `from app.*` imports** found in module files.

### Common Import Patterns to Fix

| Old Import Pattern | New Import Pattern |
|-------------------|-------------------|
| `from app.core.database import get_db` | `from modules.shared.database import get_db` |
| `from app.models.base import Base` | `from modules.shared.base import Base` |
| `from app.models.school.teacher import Teacher` | `from modules.school_teacher.models import Teacher` |
| `from app.schemas.teacher import TeacherCreate` | `from modules.school_teacher.schemas import TeacherCreate` |
| `from app.repositories.teacher_repository import TeacherRepository` | `from modules.school_teacher.repository import TeacherRepository` |
| `from app.services.teacher_service import TeacherService` | `from modules.school_teacher.service import TeacherService` |
| `from app.core.security import verify_password` | `from modules.shared.auth import verify_password` |
| `from app.dependencies import get_current_user` | `from modules.shared.auth import get_current_user` |

---

## 🔄 PHASE 5C — Switch main.py: Remove v1, Upgrade v2 → v1

> ⚠️ **This is the POINT OF NO RETURN.** Make sure smoke test in 5A passes 100% before this step.

### Step 1: Backup current main.py
```powershell
Copy-Item "app\main.py" "app\main.py.pre_cutover_backup"
```

### Step 2: Edit app/main.py

**CURRENT STRUCTURE of app/main.py (simplified):**
```python
# Old v1 routers (from app/api/endpoints/)
from app.api.endpoints.teachers import router as teacher_router
from app.api.endpoints.students import router as student_router
# ... 30+ old router imports

# New v2 routers (from modules/, added in Plans 2-4)
from modules.school_teacher.api import router as school_teacher_router
from modules.school_student.api import router as school_student_router
# ...

app.include_router(teacher_router, prefix="/api/v1/school", tags=["Old - Teacher"])
app.include_router(school_teacher_router, prefix="/api/v2/school", tags=["v2 - School Teacher"])
```

**TARGET STRUCTURE after Phase 5C:**
```python
# ── app/main.py (final version) ─────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.shared.database import engine
from modules.shared.base import Base

# ── Module Routers (School) ──────────────────────────
from modules.school_authority.api import router as school_authority_router
from modules.school_teacher.api import router as school_teacher_router
from modules.school_student.api import router as school_student_router
from modules.school_parent.api import router as school_parent_router
from modules.school_exam_section.api import router as school_exam_router
from modules.school_account_section.api import router as school_account_router
from modules.school_library.api import router as school_library_router
from modules.school_attendance.api import router as school_attendance_router

# ── Module Routers (College) ─────────────────────────
from modules.college_faculty.api import router as college_faculty_router
from modules.college_student.api import router as college_student_router
from modules.college_hod.api import router as college_hod_router
from modules.college_dean.api import router as college_dean_router
from modules.college_registrar.api import router as college_registrar_router
from modules.college_exam_section.api import router as college_exam_router
from modules.college_account_section.api import router as college_account_router
from modules.college_library.api import router as college_library_router
from modules.college_placement.api import router as college_placement_router
from modules.college_research.api import router as college_research_router
from modules.college_hostel.api import router as college_hostel_router
from modules.college_lab.api import router as college_lab_router

app = FastAPI(title="School & College Management System", version="2.0.0")

# ── Middleware ───────────────────────────────────────
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── School Routes ────────────────────────────────────
SCHOOL_PREFIX = "/api/v1/school"
app.include_router(school_authority_router,  prefix=SCHOOL_PREFIX, tags=["School - Authority"])
app.include_router(school_teacher_router,    prefix=SCHOOL_PREFIX, tags=["School - Teacher"])
app.include_router(school_student_router,    prefix=SCHOOL_PREFIX, tags=["School - Student"])
app.include_router(school_parent_router,     prefix=SCHOOL_PREFIX, tags=["School - Parent"])
app.include_router(school_exam_router,       prefix=SCHOOL_PREFIX, tags=["School - Exam"])
app.include_router(school_account_router,    prefix=SCHOOL_PREFIX, tags=["School - Account"])
app.include_router(school_library_router,    prefix=SCHOOL_PREFIX, tags=["School - Library"])
app.include_router(school_attendance_router, prefix=SCHOOL_PREFIX, tags=["School - Attendance"])

# ── College Routes ───────────────────────────────────
COLLEGE_PREFIX = "/api/v1/college"
app.include_router(college_faculty_router,   prefix=COLLEGE_PREFIX, tags=["College - Faculty"])
app.include_router(college_student_router,   prefix=COLLEGE_PREFIX, tags=["College - Student"])
app.include_router(college_hod_router,       prefix=COLLEGE_PREFIX, tags=["College - HOD"])
app.include_router(college_dean_router,      prefix=COLLEGE_PREFIX, tags=["College - Dean"])
app.include_router(college_registrar_router, prefix=COLLEGE_PREFIX, tags=["College - Registrar"])
app.include_router(college_exam_router,      prefix=COLLEGE_PREFIX, tags=["College - Exam"])
app.include_router(college_account_router,   prefix=COLLEGE_PREFIX, tags=["College - Account"])
app.include_router(college_library_router,   prefix=COLLEGE_PREFIX, tags=["College - Library"])
app.include_router(college_placement_router, prefix=COLLEGE_PREFIX, tags=["College - Placement"])
app.include_router(college_research_router,  prefix=COLLEGE_PREFIX, tags=["College - Research"])
app.include_router(college_hostel_router,    prefix=COLLEGE_PREFIX, tags=["College - Hostel"])
app.include_router(college_lab_router,       prefix=COLLEGE_PREFIX, tags=["College - Lab"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "School & College Management System v2.0", "status": "running"}
```

> ✅ Note: After switching, routes use `/api/v1/` prefix (original expected prefix) but are now served by the NEW modular system.

---

## 🧪 PHASE 5D — Run Full Test Suite

```powershell
# Run all tests:
pytest tests/ -v --tb=short

# Run with coverage:
pytest tests/ -v --cov=modules --cov-report=term-missing
```

### Fix test imports if tests use old `app.*` paths:
```powershell
# Find test files with old imports:
Select-String -Path "tests\" -Pattern "from app\." -Recurse
```

For each found test file, update imports to use `modules.*` paths.

### Expected test results:
- All previously passing tests should still pass
- No new failures introduced by migration
- If a test fails due to import path only → fix the import, not the logic

### Auth-specific test:
```powershell
# Test that authentication still works:
python -c "
from modules.shared.auth import create_access_token, verify_token
token = create_access_token({'sub': 'test_user'})
payload = verify_token(token)
print('✅ Auth working:', payload)
"
```

---

## 🧹 PHASE 5E — Cleanup & Archive

> ⚠️ Only do this AFTER Phase 5D passes with zero failures.

### Archive old app code (do NOT delete immediately)
```powershell
# Move old/ (reference copy) to archive
New-Item -ItemType Directory -Path "archive" -Force
Move-Item "old" "archive\old_app_pre_migration"
Write-Host "✅ old/ moved to archive/"
```

### Optional: Archive old app/ code (KEEP for at least 30 days)
```powershell
# Tag it as archived in git:
git add .
git commit -m "feat: Complete migration to modules/ structure (Plans 1-5)"
git tag "v2.0.0-migration-complete"
```

### Clean up migration scripts (optional)
```powershell
# Move migration scripts to archive:
New-Item -ItemType Directory -Path "archive\migration_scripts" -Force
Move-Item "scripts\migrate_school_simple.py" "archive\migration_scripts\"
Move-Item "scripts\init_modules.py" "archive\migration_scripts\"
Move-Item "scripts\smoke_test_v2.py" "archive\migration_scripts\"
Move-Item "scripts\verify_module.py" "archive\migration_scripts\"
```

### Final project structure should look like:
```
claud_sc/
├── app/
│   ├── main.py           ← uses ONLY modules/ imports now
│   ├── core/             ← keep (auth, config, middleware)
│   ├── static/           ← keep (CSS, JS assets)
│   ├── templates/        ← keep (if Jinja2 still used)
│   └── __init__.py
├── modules/
│   ├── shared/           ← database, base, config, auth
│   ├── school_authority/
│   ├── school_teacher/
│   ├── school_student/
│   ├── school_parent/
│   ├── school_exam_section/
│   ├── school_account_section/
│   ├── school_library/
│   ├── school_attendance/
│   ├── college_faculty/
│   ├── college_student/
│   ├── college_hod/
│   ├── college_dean/
│   ├── college_registrar/
│   ├── college_exam_section/
│   ├── college_account_section/
│   ├── college_library/
│   ├── college_placement/
│   ├── college_research/
│   ├── college_hostel/
│   └── college_lab/
├── tests/
├── scripts/              ← only operational scripts
├── archive/              ← old code (safe to delete after 30 days)
├── plans/                ← all migration plans
├── requirements.txt
├── .env
└── main.py
```

---

## ✅ PHASE 5F — Final Health Check

Run this complete health check after everything is done:

```powershell
# 1. App starts cleanly
uvicorn app.main:app --reload --port 8000

# 2. Root endpoint
curl http://localhost:8000/
# Expected: {"message": "School & College Management System v2.0", "status": "running"}

# 3. API docs load
# Visit: http://localhost:8000/docs
# Expected: All 20 modules visible as tag groups, all routes listed

# 4. Full test suite
pytest tests/ -v

# 5. Module import check
python -c "
from modules.school_authority.api import router as r1
from modules.school_teacher.api import router as r2
from modules.school_student.api import router as r3
from modules.school_parent.api import router as r4
from modules.school_exam_section.api import router as r5
from modules.school_account_section.api import router as r6
from modules.school_library.api import router as r7
from modules.school_attendance.api import router as r8
from modules.college_faculty.api import router as r9
from modules.college_student.api import router as r10
from modules.college_hod.api import router as r11
from modules.college_dean.api import router as r12
from modules.college_registrar.api import router as r13
from modules.college_exam_section.api import router as r14
from modules.college_account_section.api import router as r15
from modules.college_library.api import router as r16
from modules.college_placement.api import router as r17
from modules.college_research.api import router as r18
from modules.college_hostel.api import router as r19
from modules.college_lab.api import router as r20
print('✅ All 20 module routers import successfully!')
"
```

---

## 📊 Final Migration Completion Checklist

### Foundation (Plan 1)
- [ ] Backup created
- [ ] old/ reference exists
- [ ] modules/shared/ functional
- [ ] All module __init__.py exist

### School Simple Modules (Plan 2)
- [ ] school_authority ✅
- [ ] school_teacher ✅
- [ ] school_parent ✅
- [ ] school_library ✅
- [ ] school_attendance ✅
- [ ] school_student ✅

### School Complex Modules (Plan 3)
- [ ] school_exam_section (merged) ✅
- [ ] school_account_section (merged) ✅

### College Modules (Plan 4)
- [ ] college_faculty ✅
- [ ] college_student ✅
- [ ] college_hod ✅
- [ ] college_dean (role-based minimal) ✅
- [ ] college_registrar (built from scratch) ✅
- [ ] college_exam_section ✅
- [ ] college_account_section ✅
- [ ] college_library ✅
- [ ] college_placement ✅
- [ ] college_research ✅
- [ ] college_hostel ✅
- [ ] college_lab ✅

### Cutover & Verification (Plan 5)
- [ ] Smoke test passes (zero 500 errors) ✅
- [ ] Import audit passes (zero old imports) ✅
- [ ] app/main.py switched to module routers at /api/v1/ ✅
- [ ] Full pytest suite passes ✅
- [ ] Old code archived ✅
- [ ] Git commit tagged ✅

---

## 🎉 Migration Done!

**Summary of what was accomplished:**
- Moved from monolithic `app/` structure to 20 self-contained modules
- Each module owns: models, schemas, repository, service, api
- Shared utilities centralized in `modules/shared/`
- Zero functionality lost — all endpoints preserved
- Old code safely archived, not deleted
- Full test coverage maintained

**Future improvements enabled by this structure:**
- Easy to add new modules without touching other code
- Modules can be independently tested
- Ready for microservices split (each module → its own service)
- Clean separation of school and college business logic
