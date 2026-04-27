# Logic Plan 2: Missing Service Layer & Core Logic

**Priority: HIGH**

This plan documents modules that are **MISSING service layer code** (service.py), and also highlights modules where the core logic in models, repository, and schemas needs enhancement.

---

## Summary: Modules Missing Service Logic

| Module | service.py Status | Need | Priority |
|--------|-----------------|------|----------|
| school_notes | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_courses | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_notices | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_grades | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_groups | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_library | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_assignments | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_account_section | EMPTY (0 bytes) | NEEDS service layer | HIGH |
| school_parent | EMPTY (0 bytes) | NEEDS service layer | MEDIUM |
| school_timetable | EMPTY (0 bytes) | NEEDS service layer | MEDIUM |
| school_videos | EMPTY (0 bytes) | NEEDS service layer | MEDIUM |
| school_classes | EMPTY (0 bytes) | NEEDS service layer | MEDIUM |
| school_subjects | EMPTY (0 bytes) | NEEDS service layer | MEDIUM |

---

## Modules with Complete Service (Reference)

### 1. school_attendance ✅

| File | Size |
|------|------|
| api.py | 11892 bytes |
| models.py | 1964 bytes |
| repository.py | 7754 bytes |
| schemas.py | 3077 bytes |
| service.py | 5545 bytes |
| constants.py | 1907 bytes |
| exceptions.py | 2638 bytes |
| utils.py | 3058 bytes |

### 2. school_tests ✅

| File | Size |
|------|------|
| api.py | 13356 bytes |
| models.py | 3099 bytes |
| repository.py | 5202 bytes |
| schemas.py | 3381 bytes |
| service.py | 2699 bytes |
| constants.py | 0 bytes ❌ |
| exceptions.py | 0 bytes ❌ |
| utils.py | 0 bytes ❌ |

### 3. school_chat ✅

| File | Size |
|------|------|
| api.py | 7076 bytes |
| models.py | 1071 bytes |
| repository.py | 5715 bytes |
| schemas.py | 887 bytes |
| service.py | 0 bytes ❌ |
| constants.py | 0 bytes ❌ |
| exceptions.py | 0 bytes ❌ |

---

## What the Service Layer Should Contain

### Example: school_attendance Service (Reference)

From `modules/school/school_attendance/service.py` (5545 bytes):

```python
# Should contain:
- Business logic for attendance calculations
- Batch attendance processing
- Attendance report generation
- Validation and verification logic
- Integration with other modules (courses, students)
```

### What Most Modules Need

| Module | Service Needs |
|--------|--------------|
| school_notes | Note management, file handling, search logic |
| school_courses | Course enrollment, capacity management |
| school_notices | Notice distribution, targeting logic |
| school_grades | Grade calculations, bulk operations |
| school_groups | Member management, post moderation |
| school_library | Book issue/return, overdue management |
| school_assignments | Submission handling, grading workflow |
| school_account_section | Payment processing, fee calculations |

---

## Key Backup Files to Reference

### Service Layer Sources

| Source File | Module |
|-------------|--------|
| `backup/services/attendance_service.py` | school_attendance |
| `backup/services/grade_service.py` | school_grades |
| `backup/services/notice_service.py` | school_notices |
| `backup/services/group_service.py` | school_groups |
| `backup/services/library_service.py` | school_library |
| `backup/services/test_service.py` | school_tests |
| `backup/services/account_service.py` | school_account_section |

---

## Implementation Strategy

### Option 1: Copy from backup (Fastest)

Copy the service.py files from backup/modules/school/ to modules/school/

**Pros:** Quick, proven logic  
**Cons:** May need adaptation for new structure

### Option 2: Adapt from working modules

Use school_attendance/service.py as template and adapt

**Pros:** Consistent with existing code  
**Cons:** More work to customize

### Option 3: Create from scratch

Write new service layer for each module

**Pros:** Clean implementation  
**Cons:** Most time consuming

---

## Priority Order

### Phase 1: Core Academic Modules (HIGH)

| Module | Source to Copy From |
|--------|-------------------|
| school_account_section | `backup/services/account_service.py` |
| school_grades | `backup/services/grade_service.py` |
| school_notices | `backup/services/admin_notice_service.py` |
| school_library | `backup/services/library_service.py` |
| school_courses | `backup/services/course_repository.py` (logic) |

### Phase 2: Engagement Modules (MEDIUM)

| Module | Source to Copy From |
|--------|-------------------|
| school_tests | `backup/services/test_service.py` |
| school_groups | `backup/services/group_service.py` |
| school_assignments | `backup/services/assignment_repository.py` |
| school_notes | `backup/repositories/notes_repository.py` |

### Phase 3: Support Modules (LOW)

| Module | Source to Copy From |
|--------|-------------------|
| school_parent | `backup/services/parent_service.py` |
| school_videos | `backup/repositories/videos_repository.py` |
| school_timetable | `backup/repositories/` |

---

## Files to Create/Update Per Module

For each module, the service.py should contain:

1. **CRUD operations** - Database interactions beyond repository
2. **Business logic** - Grade calculations, fee processing
3. **Validation** - Complex validation beyond schemas
4. **Integration** - Cross-module operations
5. **Utilities** - Common helper functions

---

*Last Updated: 2026-03-29*