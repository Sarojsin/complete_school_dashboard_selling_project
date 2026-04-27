# 🚀 ELITE PLAN 9 — Database Migration, Data Safety & Production Rollout
## Phase: PRODUCTION — Alembic, Rollback Automation, API Versioning, Feature Flags
### Goal: Fill the 3 critical gaps identified in the plan review

---

## 📌 Three Critical Gaps This Plan Solves

| Gap | Risk | Solution in This Plan |
|-----|------|--------------------|
| No DB schema migration | 🔴 HIGH | Alembic integration for every module |
| No data migration strategy | 🔴 HIGH | Data validation + safe migration scripts |
| No rollback automation | 🟡 MEDIUM | One-command rollback at every phase |
| No API deprecation plan | 🟡 MEDIUM | `/api/v1/` deprecation timeline |
| No feature flags | 🟡 MEDIUM | Module-level feature toggle via DB |

---

## ⏱️ Effort Estimates (From the Review)

| Plan | Estimated Effort |
|------|----------------|
| Plan 1 | 1–2 hours |
| Plan 2 | 4–8 hours |
| Plan 3 | 8–16 hours |
| Plan 4 | 12–24 hours |
| Plan 5 | 4–8 hours |
| Plan 6 | 8–12 hours |
| Plan 7 | 8–16 hours |
| Plan 8 | 6–12 hours |
| **Plan 9** | **4–8 hours** |
| **Total** | **~55–100 hours** |

---

## 🗄️ SECTION A — Database Migration with Alembic

### Why Alembic?
When you add new modules with new models, the DB tables must be created or altered safely. Alembic tracks every schema change as a versioned "migration file" — like git for your database.

### Step A1 — Install & Initialize Alembic

```powershell
pip install alembic
alembic init alembic
```

This creates:
```
claud_sc/
├── alembic/
│   ├── env.py        ← configure your DB URL here
│   ├── script.py.mako
│   └── versions/     ← migration files go here
└── alembic.ini       ← alembic config file
```

### Step A2 — Configure `alembic/env.py`

```python
# alembic/env.py
from modules.shared.database import engine
from modules.shared.base import Base

# Import ALL module models so Alembic can detect them:
from modules.school_authority.models import *
from modules.school_teacher.models import *
from modules.school_student.models import *
from modules.school_parent.models import *
from modules.school_exam_section.models import *
from modules.school_account_section.models import *
from modules.school_library.models import *
from modules.school_attendance.models import *
from modules.college_faculty.models import *
from modules.college_student.models import *
from modules.college_hod.models import *
from modules.college_registrar.models import *
from modules.college_exam_section.models import *
from modules.college_account_section.models import *
from modules.college_library.models import *
from modules.college_placement.models import *
from modules.college_research.models import *
from modules.college_hostel.models import *
from modules.college_lab.models import *
from modules.super_admin.models import *
from modules.chat.models import *
from modules.groups.models import *

target_metadata = Base.metadata
```

### Step A3 — Migration Workflow Per Plan

**After Plan 2** (school simple modules added):
```powershell
alembic revision --autogenerate -m "plan2_school_simple_modules"
alembic upgrade head
```

**After Plan 3** (exam + account sections):
```powershell
alembic revision --autogenerate -m "plan3_school_exam_account"
alembic upgrade head
```

**After Plan 4** (all college modules):
```powershell
alembic revision --autogenerate -m "plan4_college_modules"
alembic upgrade head
```

**After Plan 6** (auth module changes):
```powershell
alembic revision --autogenerate -m "plan6_auth_super_admin_role"
alembic upgrade head
```

**After Plan 7** (super admin models):
```powershell
alembic revision --autogenerate -m "plan7_super_admin_tables"
alembic upgrade head
```

> ✅ **Rule:** Every time you add or change a model, run `alembic revision --autogenerate` BEFORE pushing to production.

### Step A4 — Check Migration Before Running

```powershell
# See what SQL will run (dry-run):
alembic upgrade head --sql

# See current DB version:
alembic current

# See migration history:
alembic history --verbose
```

---

## 💾 SECTION B — Data Migration Strategy

### B1 — Production Data Inventory

Before migrating, document what data currently exists:

**File: `scripts/data_inventory.py`**
```python
"""
Run: python scripts/data_inventory.py
Counts all records in all tables before migration.
Save output → compare after migration to verify zero data loss.
"""
from sqlalchemy import text
from modules.shared.database import SessionLocal

db = SessionLocal()

TABLES = [
    "users", "teachers", "students", "parents",
    "exams", "tests", "fees", "accounts",
    "library_books", "attendance_records",
    "college_students", "departments", "faculty",
    "chat_messages", "groups", "assignments", "grades", "notices"
]

print("=" * 50)
print("📊 DATA INVENTORY — Pre-Migration")
print("=" * 50)
total = 0
for table in TABLES:
    try:
        count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"  {table:<30} {count:>8} rows")
        total += count
    except Exception as e:
        print(f"  {table:<30} {'ERROR':>8} ({e})")
print("-" * 50)
print(f"  {'TOTAL':<30} {total:>8} rows")
print("=" * 50)
db.close()
```

```powershell
# Run BEFORE migration — save to file:
python scripts/data_inventory.py > reports/pre_migration_count.txt

# Run AFTER migration — compare:
python scripts/data_inventory.py > reports/post_migration_count.txt
diff reports/pre_migration_count.txt reports/post_migration_count.txt
```

**Expected result:** Zero difference in row counts.

### B2 — Safe Data Migration Rules

> ⚠️ **NEVER drop a column or table** unless both of these are true:
> 1. The app has been running without that column for at least 7 days
> 2. You have a backup from BEFORE removing it

**Safe operations (can be done at any time):**
- ✅ ADD a new column (with a default value or nullable)
- ✅ ADD a new table
- ✅ ADD an index
- ✅ RENAME via: add new column → copy data → remove old (3-step, never 1-step)

**Dangerous operations (require a maintenance window):**
- ⚠️ CHANGE a column type
- ⚠️ DROP a column
- ⚠️ DROP a table
- ⚠️ ADD a NOT NULL column without a default

### B3 — Alembic Downgrade Safety

Every migration file auto-generated by Alembic has both `upgrade()` and `downgrade()`. Verify the downgrade is correct:

```python
# alembic/versions/XXXX_plan2_school_simple_modules.py
def upgrade():
    op.create_table("school_teachers", ...)  # adds table

def downgrade():
    op.drop_table("school_teachers")         # removes it safely
```

Test downgrade before going live:
```powershell
# Test: can we roll back?
alembic downgrade -1    # undo last migration
alembic upgrade head    # reapply it
```

---

## ⏪ SECTION C — Rollback Automation

### C1 — Rollback Script (One Command)

**File: `scripts/rollback.py`**
```python
"""
Emergency rollback script.
Usage: python scripts/rollback.py [--phase 2|3|4|5|all]
Reverts the DB and code to the last stable state.
"""
import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

PHASE_TAGS = {
    "2": "pre_plan2",
    "3": "pre_plan3",
    "4": "pre_plan4",
    "5": "pre_plan5",
    "all": "pre_migration",
}

def rollback(phase: str):
    tag = PHASE_TAGS.get(phase)
    if not tag:
        print(f"❌ Unknown phase: {phase}")
        sys.exit(1)

    print(f"⏪ Rolling back to: {tag}")

    # Step 1: Revert DB to migration below this phase
    print("  1. Reverting Alembic DB migration...")
    result = subprocess.run(["alembic", "downgrade", tag], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Alembic rollback failed: {result.stderr}")
    else:
        print(f"  ✅ DB reverted to {tag}")

    # Step 2: Revert app/main.py from backup
    backup = ROOT / f"app/main.py.{tag}_backup"
    if backup.exists():
        shutil.copy2(backup, ROOT / "app/main.py")
        print(f"  ✅ app/main.py restored from {backup.name}")
    else:
        print(f"  ⚠️  No main.py backup found for {tag}")

    print(f"\n✅ Rollback to {tag} complete. Restart your app.")

if __name__ == "__main__":
    phase = sys.argv[1].replace("--phase", "").strip() if len(sys.argv) > 1 else "all"
    rollback(phase)
```

**Usage:**
```powershell
# Emergency: undo Plan 3 changes
python scripts/rollback.py --phase 3

# Full emergency rollback
python scripts/rollback.py --phase all
```

### C2 — Git Tag at Every Phase Boundary

Before starting each plan, create a git tag:
```powershell
# Before Plan 2:
git add . && git commit -m "chore: pre-Plan2 checkpoint"
git tag pre_plan2

# Before Plan 3:
git add . && git commit -m "chore: pre-Plan3 checkpoint"
git tag pre_plan3

# etc.
```

Then rollback is simply:
```powershell
git checkout pre_plan2   # go back in time (code only)
alembic downgrade pre_plan2  # revert DB too
```

---

## 🚦 SECTION D — Feature Flags for Gradual Rollout

Instead of switching all 20 modules at once (big-bang), use feature flags to enable modules one by one.

### D1 — Feature Flag Table (already in Plan 7)

The `Feature` table in `modules/super_admin/models.py` doubles as a module enable/disable switch:

```python
# modules/super_admin/models.py (already defined in Plan 7)
class Feature(Base):
    __tablename__ = "features"
    name = Column(String(100), unique=True)
    is_enabled = Column(Boolean, default=True)
```

### D2 — Module Feature Dependency

```python
# modules/shared/feature_guard.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

def require_feature(feature_name: str):
    """Dependency: raises 503 if module feature is disabled."""
    def checker(db: Session):
        from modules.super_admin.models import Feature
        feature = db.query(Feature).filter(Feature.name == feature_name).first()
        if feature and not feature.is_enabled:
            raise HTTPException(
                status_code=503,
                detail=f"Feature '{feature_name}' is currently disabled."
            )
    return checker
```

### D3 — Use in Module api.py

```python
# modules/chat/api.py
from modules.shared.feature_guard import require_feature

@router.get("/rooms/", dependencies=[Depends(require_feature("chat"))])
def list_rooms(db: Session = Depends(get_db)):
    ...
```

### D4 — Mini-Pilot Strategy (After Plan 2)

As the reviewer recommended, **do a mini-release** after Plan 2 with just 2 modules:
1. Enable ONLY `school_authority` and `school_teacher` in production
2. Keep all other modules disabled via feature flags
3. Run for 1–2 days — verify zero errors
4. Enable next batch (school_student, school_parent)
5. Continue rolling forward

```powershell
# In DB: disable all new modules initially
INSERT INTO features (name, is_enabled) VALUES
  ('school_student', false),
  ('school_parent', false),
  ('school_exam_section', false),
  -- etc.
  ('school_authority', true),   -- ONLY enable these 2
  ('school_teacher', true);
```

---

## 📋 SECTION E — API Versioning & Deprecation Plan

### E1 — Current Parallel Running

During Plans 2–4, BOTH versions run simultaneously:
- `/api/v1/school/teachers/` → **old code** (from `app/api/endpoints/teachers.py`)
- `/api/v2/school/teachers/` → **new code** (from `modules/school_teacher/api.py`)

### E2 — Version Deprecation Timeline

| Week | Action |
|------|--------|
| Week 1 | Plan 2–3 complete. `/api/v2/` routes live. `/api/v1/` still primary. |
| Week 2 | Plan 4 complete. All v2 routes available. Start notifying frontend. |
| Week 3 | Plan 5 cutover: v2 routes renamed to v1. Old `app/` routes retired. |
| Week 4–6 | Monitor. If any bugs: rollback to pre_plan5 tag. |
| Week 7+ | Old `app/` code moved to `archive/`. Migration complete. |

### E3 — Deprecation Header in v1 Old Routes

During the parallel period, add a warning header to old v1 routes:

```python
# In old app/api/endpoints/teachers.py — add deprecation warning:
from fastapi import Response

@router.get("/teachers/")
def list_teachers_deprecated(response: Response, ...):
    response.headers["X-Deprecated"] = "true"
    response.headers["X-Migrate-To"] = "/api/v2/school/teachers/"
    response.headers["X-Sunset-Date"] = "2026-04-30"
    # ... rest of existing logic
```

---

## ✅ SECTION F — Integration Test Strategy

The review noted only unit tests were mentioned. Add integration tests:

**File: `tests/integration/test_full_flow.py`**
```python
"""
Integration test: full user journey for each role
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(username, password):
    r = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    return r.json()["access_token"]

class TestSchoolTeacherJourney:
    def setup_method(self):
        self.token = get_token("teacher1", "password123")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_teacher_can_list_students(self):
        r = client.get("/api/v1/school/students/", headers=self.headers)
        assert r.status_code == 200

    def test_teacher_can_create_attendance(self):
        r = client.post("/api/v1/school/attendance/", json={...}, headers=self.headers)
        assert r.status_code in (200, 201)

    def test_teacher_cannot_access_admin(self):
        r = client.get("/api/v1/admin/users", headers=self.headers)
        assert r.status_code == 403  # forbidden

class TestSuperAdminJourney:
    def setup_method(self):
        self.token = get_token("superadmin", "adminpass")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_admin_can_see_dashboard(self):
        r = client.get("/api/v1/admin/dashboard", headers=self.headers)
        assert r.status_code == 200

    def test_admin_can_see_all_users(self):
        r = client.get("/api/v1/admin/users", headers=self.headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
```

```powershell
# Run integration tests:
pytest tests/integration/ -v

# Run with markers:
pytest -m "integration" -v
```

---

## 📊 Summary Checklist — Plan 9

### Database
- [ ] Alembic initialized (`alembic init alembic`)
- [ ] `alembic/env.py` configured with all module model imports
- [ ] Migration generated + applied after Plans 2, 3, 4, 6, 7
- [ ] Each migration's `downgrade()` tested before going live

### Data Safety
- [ ] `data_inventory.py` run before migration → saved to `reports/`
- [ ] `data_inventory.py` run after migration → diff shows zero changes
- [ ] No `DROP COLUMN` or `DROP TABLE` until 7 days after cutover

### Rollback
- [ ] Git tag created before every plan (`pre_plan2`, `pre_plan3`, etc.)
- [ ] `rollback.py` script tested in dev environment
- [ ] `app/main.py` backup made before Plan 5 cutover

### Feature Flags
- [ ] `features` table seeded in DB with all module names
- [ ] Mini-pilot done after Plan 2 (just authority + teacher live)
- [ ] Modules enabled one-by-one over 1–2 weeks

### API Versioning
- [ ] Deprecation headers added to old v1 routes
- [ ] Frontend team notified of v2 routes availability
- [ ] Sunset date set: old v1 routes retired by Week 3

### Integration Tests
- [ ] `tests/integration/` folder with journey tests for each role
- [ ] Super admin, teacher, student, parent journeys all tested
- [ ] Cross-role access denial tested (403 checks)
