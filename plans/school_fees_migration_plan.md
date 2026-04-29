# Plan: Migrate school_fees Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_fees/)
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
| `backup/models/models.py` | FeeRecord class with student_id, fee_type, amount, paid_amount, due_date |
| `backup/models/school/fee.py` | SchoolFeeStructure, SchoolFeeRecord models |
| `backup/schemas/fee.py` | FeeRecordBase, FeeRecordCreate, FeeRecordUpdate, FeeRecordResponse |
| `backup/repositories/fee_repository.py` | FeeRepository with create, get, get_all, create_payment |
| `backup/web/routers/authority.py` | /authority/fees endpoints |
| `backup/modules/school/account_section/` | Account section with fee operations |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/models.py` (FeeRecord class lines ~268-284)
**Target:** `modules/school/school_fees/models.py`

```python
# Expected structure:
class FeeRecord(Base):
    __tablename__ = "school_fee_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    fee_type = Column(String(100), nullable=False)  # tuition, library, sports, etc.
    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    due_date = Column(Date)
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(50), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    payment_status = Column(String(20), default="pending")  # pending, paid, overdue
    remarks = Column(Text, nullable=True)
    
    # Relationships
    student = relationship("SchoolStudent", back_populates="school_fees")
```

### Step 2: Create `schemas.py`
**Source:** `backup/schemas/fee.py`
**Target:** `modules/school/school_fees/schemas.py`

```python
# Expected schemas:
class FeeRecordBase(BaseModel):
    student_id: int
    fee_type: str
    amount: float
    due_date: Optional[date] = None

class FeeRecordCreate(FeeRecordBase):
    pass

class FeeRecordUpdate(BaseModel):
    amount: Optional[float] = None
    paid_amount: Optional[float] = None
    payment_status: Optional[str] = None
    remarks: Optional[str] = None

class FeeRecordResponse(FeeRecordBase):
    id: int
    paid_amount: float
    payment_date: Optional[date] = None
    payment_status: str
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/fee_repository.py`
**Target:** `modules/school/school_fees/repository.py`

Methods needed:
- `create(fee_data)` - Create new fee record
- `get(fee_id)` - Get fee by ID
- `get_by_student(student_id)` - Get fees by student
- `get_all(filters)` - Get all fees with filters
- `update(fee_id, data)` - Update fee
- `delete(fee_id)` - Delete fee
- `create_payment(fee_id, amount, payment_date)` - Record payment
- `update_payment_status(fee_id, status)` - Update status

### Step 4: Create `api.py`
**Source:** `backup/api/endpoints/fees.py` or authority endpoints
**Target:** `modules/school/school_fees/api.py`

Endpoints needed:
- `POST /` - Create fee record
- `GET /{id}` - Get fee record
- `GET /` - List fee records (with filters: student_id, payment_status)
- `PUT /{id}` - Update fee record
- `DELETE /{id}` - Delete fee record
- `POST /{id}/payment` - Record payment
- `GET /student/{student_id}` - Get student fees
- `GET /summary` - Get fee summary

### Step 5: Create `router.py`
**Target:** `modules/school/school_fees/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| FeeRecord class | Create with table name "school_fee_records" |
| Fields | student_id, fee_type, amount, paid_amount, due_date, payment_date, payment_method, transaction_id, payment_status, remarks |
| Relationships | Add student relationship |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| FeeRecordBase | student_id, fee_type, amount, due_date |
| FeeRecordCreate | All required fields |
| FeeRecordUpdate | Optional fields for partial update |
| FeeRecordResponse | All fields including id, payment_status |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create | Insert new fee record |
| get | Fetch fee by ID |
| get_by_student | Fetch fees for a student |
| get_all | List with pagination and filters |
| update | Modify existing fee |
| delete | Remove fee record |
| create_payment | Record payment for fee |
| update_payment_status | Update payment status |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST / | Add new fee record |
| GET /{id} | Get fee details |
| GET / | List fees |
| PUT /{id} | Update fee |
| DELETE /{id} | Delete fee |
| POST /{id}/payment | Record payment |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.schemas.fee import ...` | `from .schemas import ...` |
| `from backup.repositories.fee_repository import ...` | Create new repository |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules