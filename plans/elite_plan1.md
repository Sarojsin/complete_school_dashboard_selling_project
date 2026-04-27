# 🛡️ ELITE PLAN 1 — Foundation & Safety Setup
## Phase: ZERO RISK — Backup, Scaffold, Shared Layer
### Goal: Prepare the migration battlefield with zero damage to existing code

---

## 📌 Overview

This is the **starting phase**. We do NOT touch any business logic. We only:
1. Create a full backup
2. Ensure `old/` folder structure is ready as reference
3. Confirm `modules/` folder exists with all 21 module directories
4. Build the `modules/shared/` layer completely
5. Create a minimal working `app/main.py` that boots with zero errors

> ⚠️ **Rule:** After every step, the app must still run. Never break the running system.

---

## 🗂️ Current State (as of right now)

```
claud_sc/
├── app/                    ← OLD code (ALL business logic lives here)
│   ├── models/
│   │   ├── school/         → authority.py, class_model.py, fee.py, parent.py, student.py, teacher.py
│   │   ├── college/        → course.py, department.py, enrollment.py, faculty.py, fee.py,
│   │   │                     hostel.py, lab.py, placement.py, program.py, research.py, semester.py, student.py
│   │   ├── account_models.py, admin_models.py, base.py, chat_models.py,
│   │   │   department_models.py, exam_models.py, group_models.py,
│   │   │   library_models.py, models.py, test_models.py
│   ├── schemas/            → 23 schema files
│   ├── services/           → 29 service files
│   ├── repositories/       → 34 repository files
│   ├── api/endpoints/      → 39 endpoint files
│   ├── web/                → authority_crud.py, routers/, routes.py.old
│   ├── templates/          → HTML Jinja2 templates
│   ├── core/               → config, security, etc.
│   ├── shared/             → shared utilities
│   └── main.py             ← current app entry point (11499 bytes, production-grade)
│
├── modules/                ← NEW target (21 module folders exist but mostly empty)
│   ├── shared/             → auth.py, base.py, config.py, database.py, exceptions.py, models.py, utils.py
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
```

---

## ✅ STEP 1 — Full Project Backup

**Run this from the project root (PowerShell on Windows):**

```powershell
# Create a timestamped backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Path "." -Destination "..\claud_sc_backup_$timestamp" -Recurse
Write-Host "✅ Backup created at: ..\claud_sc_backup_$timestamp"
```

**Expected result:** A full copy of `claud_sc` exists one folder up on the Desktop.

**Verify:** Check that `..\claud_sc_backup_XXXXXXXX` folder exists and has the same files.

---

## ✅ STEP 2 — Create `old/` as a Reference Copy (DO NOT DELETE app/)

> ⚠️ In our case, `app/` is still live and running. We create `old/` as a READ-ONLY reference — a lens to look at the original structure. We do NOT move `app/`.

```powershell
# Create old/ as a reference copy of app/
New-Item -ItemType Directory -Path "old" -Force
Copy-Item -Path "app\" -Destination "old\app" -Recurse
Write-Host "✅ old/app/ created as reference copy"
```

**Expected result:**
```
claud_sc/
├── app/        ← still live (DO NOT TOUCH)
├── old/
│   └── app/    ← read-only reference
├── modules/
```

**Reason:** `elite_migration.md` says "move app to old/", but since our app is running, we COPY instead. We will migrate gradually from `app/` directly. `old/` is our safety reference.

---

## ✅ STEP 3 — Verify modules/shared/ is Complete

The `modules/shared/` folder already exists with critical files. Verify each:

| File | Purpose | Status Check |
|------|---------|-------------|
| `modules/shared/database.py` | SQLAlchemy engine + `get_db` | Must export `engine`, `SessionLocal`, `get_db` |
| `modules/shared/base.py` | Declarative Base | Must export `Base` |
| `modules/shared/config.py` | Settings/env vars | Must work with `.env` file |
| `modules/shared/auth.py` | JWT utilities | Must export token creation/verification |
| `modules/shared/exceptions.py` | Custom exceptions | Must be importable |
| `modules/shared/utils.py` | Shared utilities | Must be importable |
| `modules/shared/models.py` | Shared model markers | Check it references Base correctly |

**Manual check command:**
```powershell
python -c "from modules.shared.database import engine, get_db; from modules.shared.base import Base; print('✅ shared layer OK')"
```

**If this fails:** Fix `modules/shared/` files before proceeding. This is the foundation everything depends on.

---

## ✅ STEP 4 — Ensure Every Module Folder Has `__init__.py`

Every module folder in `modules/` needs a proper `__init__.py`. Run this script:

**File to create:** `scripts/init_modules.py`

```python
"""
Script: scripts/init_modules.py
Purpose: Ensure every module has __init__.py
Run: python scripts/init_modules.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
MODULES_DIR = ROOT / "modules"

MODULES = [
    "school_authority", "school_teacher", "school_student", "school_parent",
    "school_exam_section", "school_account_section", "school_library", "school_attendance",
    "college_faculty", "college_student", "college_hod", "college_dean",
    "college_registrar", "college_exam_section", "college_account_section",
    "college_library", "college_placement", "college_research", "college_hostel", "college_lab",
]

INIT_CONTENT = '"""Module: {name}"""\n'

for module in MODULES:
    module_dir = MODULES_DIR / module
    module_dir.mkdir(parents=True, exist_ok=True)
    init_file = module_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text(INIT_CONTENT.format(name=module))
        print(f"✅ Created: modules/{module}/__init__.py")
    else:
        print(f"⏭️ Exists:  modules/{module}/__init__.py")

print("\n✅ All module __init__.py files ensured.")
```

**Run:**
```powershell
python scripts/init_modules.py
```

---

## ✅ STEP 5 — Confirm App Still Runs

After all setup steps, the existing `app/` must still boot perfectly:

```powershell
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs

**Expected:** All routes from old app still appear in Swagger UI. No migration changes should break anything at this stage.

---

## 📊 Phase 1 Completion Checklist

- [ ] Full backup created outside project
- [ ] `old/app/` created as reference copy
- [ ] `modules/shared/` can be imported without errors
- [ ] All 20 module folders have `__init__.py`
- [ ] `uvicorn app.main:app --reload` runs with zero errors
- [ ] http://localhost:8000/docs shows all existing routes

---

## 🔜 What Comes Next (Plan 2)

Phase 2 begins migrating the **SCHOOL modules** — starting with the simplest two:
- `school_authority` — role-based authority management
- `school_teacher` — teacher CRUD operations

Each module gets: `models.py`, `schemas.py`, `repository.py`, `service.py`, `api.py`
