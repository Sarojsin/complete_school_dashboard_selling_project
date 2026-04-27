# 🔬 ELITE PLAN 3 — Complex School Modules (Exam + Account)
## Phase: SCHOOL ADVANCED — school_exam_section & school_account_section
### Goal: Migrate the 2 complex school modules requiring multi-file merging

---

## 📌 Pre-Conditions (from Plan 2)
- [ ] ✅ All 6 simple school modules migrated and tested
- [ ] ✅ Each module's routes visible in /docs under /api/v2/school/
- [ ] ✅ App still runing on port 8000 with zero errors

> ⚠️ **Why these are "complex":** These modules pull code from MULTIPLE source files that must be merged into single `models.py`, `schemas.py`, `repository.py`, and `service.py` files. Doing this wrong = data corruption or import errors.

---

## 📋 MODULE 7: `school_exam_section`

### What needs to be merged
This module receives code from **multiple old files** that must be combined:

```
app/models/exam_models.py         ─┐
app/models/test_models.py         ─┤──→ modules/school_exam_section/models.py (MERGE)

app/schemas/exam_schemas.py       ─┐
                                   ├──→ modules/school_exam_section/schemas.py (MERGE)
                              (test schemas from admin_exam)

app/repositories/exam_repository.py  ─┐
app/repositories/test_repository.py  ─┤──→ modules/school_exam_section/repository.py (MERGE)

app/services/exam_service.py         ─┐
app/services/test_service.py         ─┤──→ modules/school_exam_section/service.py (MERGE)

app/api/endpoints/exam_section.py    ─┐
app/api/endpoints/tests.py           ─┤──→ modules/school_exam_section/api.py (MERGE)
```

---

### Step 3.1 — Merge `models.py`

**Read both source files:**
```powershell
# Check what classes are in each:
Select-String -Path "app\models\exam_models.py" -Pattern "^class "
Select-String -Path "app\models\test_models.py" -Pattern "^class "
```

**Merge strategy:**
```python
# modules/school_exam_section/models.py

# ── Single import block ──────────────────────────────
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# ── From exam_models.py ─────────────────────────────
class Exam(Base):
    __tablename__ = "exams"
    # ... paste all fields from app/models/exam_models.py
    # Change: from app.models.base import Base → already done above

# ── From test_models.py ─────────────────────────────
class Test(Base):
    __tablename__ = "tests"
    # ... paste all fields from app/models/test_models.py

class TestQuestion(Base):
    __tablename__ = "test_questions"
    # ... etc.

# ── ForeignKey note ─────────────────────────────────
# If Exam/Test references Student table:
#   student_id = Column(Integer, ForeignKey("students.id"))
#   — use TABLE NAME string, NOT model class import
```

**Checklist for models merge:**
- [ ] No duplicate class names
- [ ] No duplicate imports
- [ ] Single `Base` import from `modules.shared.base`
- [ ] All `ForeignKey` references use table name strings
- [ ] File has exactly ONE `from modules.shared.base import Base` line

---

### Step 3.2 — Merge `schemas.py`

```powershell
# Check what schemas exist:
Select-String -Path "app\schemas\exam_schemas.py" -Pattern "^class "
```

**Merge strategy:**
```python
# modules/school_exam_section/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ── From exam_schemas.py ────────────────────────────
class ExamBase(BaseModel): ...
class ExamCreate(ExamBase): ...
class ExamResponse(ExamBase): ...

# ── Test schemas (from admin_exam or inline) ────────
class TestBase(BaseModel): ...
class TestCreate(TestBase): ...
class TestQuestionCreate(BaseModel): ...
class TestResponse(TestBase): ...
```

---

### Step 3.3 — Merge `repository.py`

```python
# modules/school_exam_section/repository.py

from sqlalchemy.orm import Session
from modules.school_exam_section.models import Exam, Test, TestQuestion
from modules.shared.database import get_db  # used in API layer

class ExamRepository:
    def __init__(self, db: Session): self.db = db
    # ... paste methods from app/repositories/exam_repository.py
    # Fix: from app.models.exam_models import Exam → from .models import Exam

class TestRepository:
    def __init__(self, db: Session): self.db = db
    # ... paste methods from app/repositories/test_repository.py
    # Fix: from app.models.test_models import Test → from .models import Test
```

---

### Step 3.4 — Merge `service.py`

```python
# modules/school_exam_section/service.py

from modules.school_exam_section.repository import ExamRepository, TestRepository
from modules.school_exam_section.schemas import ExamCreate, TestCreate

class ExamService:
    # ... paste from app/services/exam_service.py
    # Fix all imports

class TestService:
    # ... paste from app/services/test_service.py
    # Fix all imports
```

---

### Step 3.5 — Merge `api.py`

```python
# modules/school_exam_section/api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.school_exam_section.service import ExamService, TestService
from modules.school_exam_section.schemas import ExamCreate, TestCreate

router = APIRouter()

# ── Exam routes (from exam_section.py) ──────────────
@router.get("/exams/") ...
@router.post("/exams/") ...

# ── Test routes (from tests.py) ─────────────────────
@router.get("/tests/") ...
@router.post("/tests/") ...
```

### Wire into main.py
```python
from modules.school_exam_section.api import router as school_exam_router
app.include_router(school_exam_router, prefix="/api/v2/school", tags=["v2 - School Exam"])
```

### Verification for school_exam_section
```powershell
uvicorn app.main:app --reload
# Check: http://localhost:8000/docs → "v2 - School Exam" section
# Test: GET /api/v2/school/exams/ → should return 200 (empty list is fine)
```

---

## 📋 MODULE 8: `school_account_section`

### What needs to be merged
```
app/models/account_models.py           ─┐
app/models/school/fee.py               ─┤──→ modules/school_account_section/models.py (MERGE)

app/schemas/account_schemas.py         ─┐
app/schemas/fee.py                     ─┤──→ modules/school_account_section/schemas.py (MERGE)

app/repositories/account_repository.py  ─┐
app/repositories/fee_repository.py      ─┤──→ modules/school_account_section/repository.py
app/repositories/fee_structure_repository.py ┘  (TRIPLE MERGE)

app/services/account_service.py        ─┐
app/services/admin_finance_service.py  ─┤──→ modules/school_account_section/service.py
                             (school parts only!)  (PARTIAL MERGE)

app/api/endpoints/account.py           ─┐
app/api/endpoints/fees.py              ─┤──→ modules/school_account_section/api.py (MERGE)
```

---

### ⚠️ CRITICAL: Splitting `admin_finance_service.py`

`app/services/admin_finance_service.py` serves **BOTH school AND college** accounts. You must:

1. Open `app/services/admin_finance_service.py`
2. Identify which methods deal with school fees vs college fees
3. Copy **only school-related methods** to `modules/school_account_section/service.py`
4. Copy **only college-related methods** to `modules/college_account_section/service.py` (Plan 4)

**Detection script:**
```powershell
# Find methods with 'school' in name:
Select-String -Path "app\services\admin_finance_service.py" -Pattern "def.*school"
# Find methods with 'college' in name:
Select-String -Path "app\services\admin_finance_service.py" -Pattern "def.*college"
```

---

### Step-by-Step for school_account_section

**Step A: Merge models.py**
```python
# modules/school_account_section/models.py
from modules.shared.base import Base
from sqlalchemy import ...

# ── From account_models.py ──────────────────────────
class AccountTransaction(Base): ...

# ── From models/school/fee.py ───────────────────────
class FeeStructure(Base): ...
class FeePayment(Base): ...
```

**Step B: Merge schemas.py**
```python
# modules/school_account_section/schemas.py
# Combine account_schemas.py + fee.py schemas
class AccountTransactionCreate(BaseModel): ...
class FeePaymentCreate(BaseModel): ...
class FeeStructureCreate(BaseModel): ...
```

**Step C: Merge repository.py (3 files)**
```python
# modules/school_account_section/repository.py
from modules.school_account_section.models import AccountTransaction, FeeStructure, FeePayment

class AccountRepository:
    # from account_repository.py

class FeeRepository:
    # from fee_repository.py (school parts)

class FeeStructureRepository:
    # from fee_structure_repository.py
```

**Step D: Partial service.py**
```python
# modules/school_account_section/service.py
from modules.school_account_section.repository import AccountRepository, FeeRepository

class AccountService:
    # from account_service.py

class SchoolFinanceService:
    # SCHOOL-ONLY methods from admin_finance_service.py
```

**Step E: Merge api.py**
```python
# modules/school_account_section/api.py
router = APIRouter()

# Routes from account.py
@router.get("/account/transactions") ...

# Routes from fees.py
@router.get("/fees/") ...
@router.post("/fees/pay") ...
```

### Wire into main.py
```python
from modules.school_account_section.api import router as school_account_router
app.include_router(school_account_router, prefix="/api/v2/school", tags=["v2 - School Account"])
```

---

## 🔧 Merge Verification Script

Run this after each merge to check for common mistakes:

**File: `scripts/verify_module.py`**
```python
"""
Usage: python scripts/verify_module.py school_exam_section
"""
import sys
import ast
from pathlib import Path

module_name = sys.argv[1] if len(sys.argv) > 1 else "school_exam_section"
ROOT = Path(__file__).parent.parent
module_path = ROOT / "modules" / module_name

files_to_check = ["models.py", "schemas.py", "repository.py", "service.py", "api.py"]

issues = []
for f in files_to_check:
    fp = module_path / f
    if not fp.exists():
        issues.append(f"❌ MISSING: {f}")
        continue
    
    content = fp.read_text(encoding="utf-8")
    
    # Check for old imports
    if "from app." in content:
        old_imports = [line.strip() for line in content.split("\n") if "from app." in line]
        for imp in old_imports:
            issues.append(f"❌ OLD IMPORT in {f}: {imp}")
    
    # Check parseable
    try:
        ast.parse(content)
        print(f"✅ Syntax OK: {f}")
    except SyntaxError as e:
        issues.append(f"❌ SYNTAX ERROR in {f}: {e}")

if issues:
    print("\n🚨 Issues found:")
    for i in issues:
        print(f"  {i}")
else:
    print(f"\n✅ Module '{module_name}' looks clean!")
```

```powershell
# Run for each module:
python scripts/verify_module.py school_exam_section
python scripts/verify_module.py school_account_section
```

---

## 📊 Phase 3 Completion Checklist

### school_exam_section
- [ ] `models.py` created by merging `exam_models.py` + `test_models.py`
- [ ] `schemas.py` created from `exam_schemas.py` (+ any test schemas)
- [ ] `repository.py` merged from `exam_repository.py` + `test_repository.py`
- [ ] `service.py` merged from `exam_service.py` + `test_service.py`
- [ ] `api.py` merged from `exam_section.py` + `tests.py` endpoints
- [ ] `verify_module.py school_exam_section` returns zero old imports
- [ ] Routes appear under `/api/v2/school/exams` and `/api/v2/school/tests`

### school_account_section
- [ ] `models.py` merged from `account_models.py` + `school/fee.py`
- [ ] `schemas.py` merged from `account_schemas.py` + `fee.py`
- [ ] `repository.py` merged from 3 source repositories
- [ ] `service.py` includes SCHOOL-ONLY parts of `admin_finance_service.py`
- [ ] `api.py` merged from `account.py` + `fees.py` endpoints
- [ ] `verify_module.py school_account_section` returns zero old imports
- [ ] Routes appear under `/api/v2/school/account` and `/api/v2/school/fees`

---

## 🔜 What Comes Next (Plan 4)

Plan 4 handles all **COLLEGE modules**:
- `college_faculty`, `college_student`, `college_hod`, `college_dean`
- `college_registrar` — needs new service + api (no endpoints existed)
- `college_exam_section`, `college_account_section`, `college_library`
