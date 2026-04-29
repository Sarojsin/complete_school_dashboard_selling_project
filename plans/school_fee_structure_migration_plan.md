# Plan: Migrate school_fee_structure Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_fee_structure/)
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
| `backup/models/school/fee.py` | SchoolFeeStructure model with grade_level, academic_year, tuition_fee, etc. |
| `backup/models/models.py` | FeeStructure class (lines ~230-243) |
| `backup/repositories/fee_structure_repository.py` | FeeStructureRepository with create, get, get_all |
| `backup/web/routers/authority.py` | /authority/fees/structure endpoints |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Source:** `backup/models/school/fee.py` (SchoolFeeStructure class)
**Target:** `modules/school/school_fee_structure/models.py`

```python
# Expected structure:
class FeeStructure(Base):
    __tablename__ = "school_fee_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(20), nullable=False)  # Class 1-12
    academic_year = Column(String(20), nullable=False)
    tuition_fee = Column(Float, default=0.0)
    registration_fee = Column(Float, default=0.0)
    library_fee = Column(Float, default=0.0)
    sports_fee = Column(Float, default=0.0)
    lab_fee = Column(Float, default=0.0)
    activity_fee = Column(Float, default=0.0)
    other_charges = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_fee_structure/schemas.py`

```python
# Expected schemas:
class FeeStructureBase(BaseModel):
    grade_level: str
    academic_year: str
    tuition_fee: Optional[float] = 0.0
    registration_fee: Optional[float] = 0.0
    library_fee: Optional[float] = 0.0
    sports_fee: Optional[float] = 0.0
    lab_fee: Optional[float] = 0.0
    activity_fee: Optional[float] = 0.0
    other_charges: Optional[float] = 0.0

class FeeStructureCreate(FeeStructureBase):
    pass

class FeeStructureUpdate(BaseModel):
    tuition_fee: Optional[float] = None
    registration_fee: Optional[float] = None
    # ... other optional fields

class FeeStructureResponse(FeeStructureBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    @property
    def total_fee(self) -> float:
        return sum([
            self.tuition_fee or 0,
            self.registration_fee or 0,
            self.library_fee or 0,
            self.sports_fee or 0,
            self.lab_fee or 0,
            self.activity_fee or 0,
            self.other_charges or 0
        ])
    
    class Config:
        from_attributes = True
```

### Step 3: Create `repository.py`
**Source:** `backup/repositories/fee_structure_repository.py`
**Target:** `modules/school/school_fee_structure/repository.py`

Methods needed:
- `create(structure_data)` - Create new fee structure
- `get(structure_id)` - Get structure by ID
- `get_by_grade(grade_level, academic_year)` - Get by grade and year
- `get_all(filters)` - Get all structures
- `update(structure_id, data)` - Update structure
- `delete(structure_id)` - Delete structure

### Step 4: Create `api.py`
**Source:** `backup/web/routers/authority.py` (fee structure endpoints)
**Target:** `modules/school/school_fee_structure/api.py`

Endpoints needed:
- `POST /` - Create fee structure
- `GET /{id}` - Get fee structure
- `GET /` - List fee structures
- `PUT /{id}` - Update fee structure
- `DELETE /{id}` - Delete fee structure
- `GET /by-grade/{grade_level}` - Get by grade level
- `GET /by-year/{academic_year}` - Get by academic year

### Step 5: Create `router.py`
**Target:** `modules/school/school_fee_structure/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| FeeStructure class | Create with table name "school_fee_structures" |
| Fields | grade_level, academic_year, tuition_fee, registration_fee, library_fee, sports_fee, lab_fee, activity_fee, other_charges |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| FeeStructureBase | grade_level, academic_year, and all fee components |
| FeeStructureCreate | All required fields |
| FeeStructureUpdate | Optional fields for partial update |
| FeeStructureResponse | All fields with total_fee computed property |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create | Insert new fee structure |
| get | Fetch structure by ID |
| get_by_grade | Fetch structure for specific grade/year |
| get_all | List with pagination and filters |
| update | Modify existing structure |
| delete | Remove structure |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| POST / | Add new fee structure |
| GET /{id} | Get structure details |
| GET / | List structures |
| PUT /{id} | Update structure |
| DELETE /{id} | Delete structure |
| GET /by-grade/{grade_level} | Get by grade |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |
| `from backup.repositories.fee_structure_repository import ...` | Create new repository |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules