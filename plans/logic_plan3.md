# Logic Plan 3: Exact Copy Mapping from Backup

**Priority: HIGH**

This plan provides an **exact mapping** of which files to copy from the backup folder to complete the modules structure.

---

## Quick Reference: Complete Module Structure

A complete module should have these files:

| File | Required | Purpose |
|------|----------|---------|
| `__init__.py` | ✅ Required | Module exports |
| `api.py` | ✅ Required | REST API endpoints |
| `router.py` | ✅ Required | Route registration |
| `models.py` | ✅ Required | SQLAlchemy models |
| `schemas.py` | ✅ Required | Pydantic schemas |
| `repository.py` | ✅ Required | Database operations |
| `service.py` | ✅ Required | Business logic |
| `constants.py` | ✅ Required | Module constants |
| `exceptions.py` | ✅ Required | Custom exceptions |
| `utils.py` | ✅ Required | Helper utilities |
| `tests/` | Optional | Unit tests |

---

## Module-by-Module Copy Mapping

### 1. school_notes

**Location:** `modules/school/school_notes/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | 5321 ✅ | - |
| models.py | 2001 ✅ | - |
| repository.py | 3032 ✅ | - |
| schemas.py | 1008 ✅ | - |
| constants.py | 0 ❌ | `backup/utils/constants.py` |
| exceptions.py | 0 ❌ | `backup/utils/exceptions.py` |
| service.py | 0 ❌ | `backup/services/` |
| utils.py | 0 ❌ | `backup/utils/` |

**Action:** Create constants/exceptions from system constants

---

### 2. school_tests

**Location:** `modules/school/school_tests/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | 13356 ✅ | - |
| models.py | 3099 ✅ | - |
| repository.py | 5202 ✅ | - |
| schemas.py | 3381 ✅ | - |
| service.py | 2699 ✅ | - |
| constants.py | 0 ❌ | Create test status constants |
| exceptions.py | 0 ❌ | Create test exceptions |
| utils.py | 0 ❌ | Create timer utilities |

**Action:** Add test-specific constants/exceptions

---

### 3. school_courses

**Location:** `modules/school/school_courses/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | 5935 ✅ | - |
| models.py | 2535 ✅ | - |
| repository.py | 4493 ✅ | - |
| schemas.py | 820 ✅ | - |
| constants.py | 0 ❌ | `backup/core/constants.py` |
| exceptions.py | 0 ❌ | `backup/core/exceptions.py` |
| service.py | 0 ❌ | `backup/services/course_repository.py` |
| utils.py | 0 ❌ | Create course utilities |

**Source Files:**
- `backup/repositories/course_repository.py` - Contains course logic
- `backup/schemas/course.py` - Course schemas
- `backup/core/exceptions.py` - Core exceptions

---

### 4. school_notices

**Location:** `modules/school/school_notices/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | 5601 ✅ | - |
| models.py | 1154 ✅ | - |
| repository.py | 5500 ✅ | - |
| schemas.py | 826 ✅ | - |
| constants.py | 0 ❌ | Create notice constants |
| exceptions.py | 0 ❌ | Create notice exceptions |
| service.py | 0 ❌ | Copy from backup/services |
| utils.py | 0 ❌ | Create notice utilities |

**Source Files:**
- `backup/services/notice_service.py` - Notice service logic
- `backup/repositories/notice_repository.py` - Notice repository
- `backup/schemas/notice.py` - Notice schemas

---

### 5. school_grades

**Location:** `modules/school/school_grades/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | 7275 ✅ | - |
| models.py | 2663 ✅ | - |
| repository.py | 4163 ✅ | - |
| schemas.py | 1492 ✅ | - |
| constants.py | 0 ❌ | Create grade constants |
| exceptions.py | 0 ❌ | Create grade exceptions |
| service.py | 0 ❌ | Copy from backup/services |
| utils.py | 0 ❌ | Create grade utilities |

**Source Files:**
- `backup/services/grade_service.py` - Grade logic
- `backup/repositories/grade_repository.py` - Grade repository

---

### 6. school_groups

**Location:** `modules/school/school_groups/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | ~9700 ✅ | - |
| models.py | 3077 ✅ | - |
| repository.py | 7565 ✅ | - |
| schemas.py | 1903 ✅ | - |
| constants.py | 0 ❌ | Create group constants |
| exceptions.py | 0 ❌ | Create group exceptions |
| service.py | 0 ❌ | Copy from backup/services |
| utils.py | 0 ❌ | Create group utilities |

**Source Files:**
- `backup/services/group_service.py` - Group logic
- `backup/services/group_post_service.py` - Post logic
- `backup/repositories/group_repository.py` - Group repository

---

### 7. school_library

**Location:** `modules/school/school_library/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | ✅ | - |
| models.py | ✅ | - |
| repository.py | ✅ | - |
| schemas.py | ✅ | - |
| constants.py | 0 ❌ | Copy from backup/modules |
| exceptions.py | 0 ❌ | Copy from backup |
| service.py | 0 ❌ | Copy from backup/services |
| utils.py | 0 ❌ | Copy from backup/modules |

**Source Files:**
- `backup/modules/school/library/` - Already has full structure
- `backup/services/library_service.py` - Library service

---

### 8. school_assignments

**Location:** `modules/school/school_assignments/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | ✅ | - |
| models.py | ✅ | - |
| repository.py | ✅ | - |
| schemas.py | ✅ | - |
| constants.py | 0 ❌ | Create assignment constants |
| exceptions.py | 0 ❌ | Create assignment exceptions |
| service.py | 0 ❌ | Copy from backup |
| utils.py | 0 ❌ | Create assignment utilities |

**Source Files:**
- `backup/repositories/assignment_repository.py` - Assignment logic
- `backup/api/endpoints/assignments.py` - Assignment endpoints

---

### 9. school_account_section

**Location:** `modules/school/school_account_section/`

| Current File | Size | Needs Copy From |
|-------------|------|---------------|
| api.py | ✅ | - |
| models.py | ✅ | - |
| repository.py | ✅ | - |
| schemas.py | ✅ | - |
| constants.py | 0 ❌ | **COPY** `backup/modules/school/account_section/constants.py` |
| exceptions.py | 0 ❌ | **COPY** `backup/modules/school/account_section/exceptions.py` |
| service.py | 0 ❌ | **COPY** `backup/modules/school/account_section/service.py` |
| utils.py | 0 ❌ | **COPY** `backup/modules/school/account_section/utils.py` |

**⚠️ CRITICAL:** This module has complete backup source - DIRECT COPY recommended!

---

## Summary: Files to Copy

| Module | Priority | Best Source |
|--------|----------|------------|
| school_account_section | HIGH | backup/modules/school/account_section/ (ALL) |
| school_notices | HIGH | backup/services/, backup/repositories/ |
| school_grades | HIGH | backup/services/grade_service.py |
| school_courses | MEDIUM | backup/repositories/course_repository.py |
| school_groups | MEDIUM | backup/services/group_service.py |
| school_library | LOW | backup/modules/school/library/ |
| school_assignments | MEDIUM | backup/repositories/assignment_repository.py |
| school_parent | MEDIUM | backup/modules/school/parent/ |
| school_timetable | LOW | backup/repositories/ |
| school_videos | LOW | backup/repositories/videos_repository.py |

---

## Implementation Command Pattern

```
# For school_account_section (complete copy):
COPY backup/modules/school/account_section/constants.py -> modules/school/school_account_section/constants.py
COPY backup/modules/school/account_section/exceptions.py -> modules/school/school_account_section/exceptions.py
COPY backup/modules/school/account_section/service.py -> modules/school/school_account_section/service.py
COPY backup/modules/school/account_section/utils.py -> modules/school/school_account_section/utils.py

# For other modules (selective copy):
COPY relevant sections from backup/services/*.py -> modules/school/<module>/service.py
COPY relevant sections from backup/utils/*.py -> modules/school/<module>/constants.py
```

---

## Verification Checklist

After copying, verify each module has:

- [ ] constants.py > 100 bytes
- [ ] exceptions.py > 100 bytes
- [ ] service.py > 500 bytes
- [ ] utils.py > 50 bytes (if needed)

---

*Last Updated: 2026-03-29*