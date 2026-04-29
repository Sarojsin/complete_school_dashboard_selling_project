# Plan: Create school_attendance Module

## Current State Analysis

### Existing Module (modules/school/school_attendance/)
Files exist but may need updates.

| File | Current State | Issues |
|------|---------------|--------|
| `models.py` | ✅ Exists | May need to verify |
| `schemas.py` | ⚠️ Partial | May be incomplete |
| `repository.py` | ⚠️ Basic | Need full CRUD |
| `service.py` | ⚠️ Basic | Need business logic |
| `router.py` | ⚠️ Limited | Need all endpoints |

### Source (backup/schemas/attendance.py)
Only schema available - need to create full module.

---

## Migration Steps

### Step 1: Use existing models if available
- Check existing models.py for attendance structure

### Step 2: Create/Update Schemas
- Source from backup/schemas/attendance.py

### Step 3: Create Full Module
- Create repository with full CRUD
- Create service with business logic  
- Create router with all endpoints

### Step 4: Fix Imports

| Old (backup) | New (modules) |
|--------------|---------------|
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. Approve this plan → Proceed to implementation
2. Continue to next module
