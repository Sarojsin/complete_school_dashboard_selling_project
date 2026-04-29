# Plan: Create school_courses Module

## Current State Analysis

### Existing Module (modules/school/school_courses/)
Files exist - need to verify completeness.

| File | Current State | Action |
|------|---------------|--------|
| `models.py` | ✅ Exists | Verify |
| `schemas.py` | ⚠️ Partial | Enhance |
| `repository.py` | ⚠️ Basic | Enhance |
| `service.py` | ⚠️ Basic | Enhance |
| `router.py` | ⚠️ Limited | Enhance |

### Source (backup/schemas/course.py)
Schema available - need to create full module.

---

## Migration Steps

### Step 1: Use existing models
- Check existing models.py

### Step 2: Enhance Module
- Create/enhance schemas from backup/schemas/course.py
- Add repository CRUD methods
- Add service business logic
- Add router endpoints

### Step 3: Fix Imports
| Old | New |
|-----|-----|
| `get_async_db` | `get_db` |
| `get_current_user` | `get_current_user` |

---

## Next Steps
1. Proceed to implementation
2. Continue to school_assignments
