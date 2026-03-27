# Comprehensive Migration Plan: All School Modules (19)

## Overview

This document provides individual migration plans for all 19 school modules in the new modular structure.

### Module Mapping: New Structure → Backup Source

| # | New Module (modules/school/) | Backup Source | Status |
|---|------------------------------|---------------|--------|
| 1 | school_teacher | backup/modules/school/teacher/ | ✅ Has source |
| 2 | school_student | backup/modules/school/student/ | ✅ Has source |
| 3 | school_parent | backup/modules/school/parent/ | ✅ Has source |
| 4 | school_authority | backup/modules/school/authority/ | ✅ Has source |
| 5 | school_account_section | backup/modules/school/account_section/ | ✅ Has source |
| 6 | school_library | backup/modules/school/library/ | ✅ Has source |
| 7 | school_exam_section | backup/modules/school/exam_section/ | ✅ Has source |
| 8 | school_attendance | backup/schemas/attendance.py | ⚠️ Schema only |
| 9 | school_courses | backup/schemas/course.py | ⚠️ Schema only |
| 10 | school_grades | backup/schemas/grade.py | ⚠️ Schema only |
| 11 | school_notices | backup/schemas/notice.py | ⚠️ Schema only |
| 12 | school_tests | backup/schemas/exam_schemas.py | ⚠️ Schema only |
| 13 | school_assignments | backup/schemas/assignment.py | ⚠️ Schema only |
| 14 | school_timetable | (new) | 🆕 New |
| 15 | school_dashboard | (new) | 🆕 New |
| 16 | school_groups | backup/schemas/group.py | ⚠️ Schema only |
| 17 | school_chat | (new) | 🆕 New |
| 18 | school_notes | backup/schemas/misc.py | ⚠️ Schema only |
| 19 | school_videos | (new) | 🆕 New |

---

## Module-by-Module Migration Plans

### Module 1: school_teacher

**Location:** `modules/school/school_teacher/`

**Backup Source:** `backup/modules/school/teacher/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | teacher/schemas.py | Add TeacherUpdate, TeacherWithUser |
| repository.py | ⚠️ Basic | teacher/repository.py | Add get_by_employee_id, get_all, update, delete |
| service.py | ⚠️ Basic | teacher/service.py | Add create validation, deactivate |
| router.py | ⚠️ Limited | teacher/api.py | Add POST, PUT, DELETE, deactivate endpoints |

**Required Import Fixes:**
- `backup.models.base.Base` → `modules.shared.base.Base`
- `backup.modules.school.teacher.schemas` → `.schemas`
- `modules.shared.database.get_async_db` → `modules.shared.database.get_db`
- `modules.shared.auth.get_current_user` → `modules.auth.dependencies.get_current_user`

**API Endpoints to Add:**
- `POST /` - Create teacher
- `GET /by-user/{user_id}` - Get by user
- `PUT /{teacher_id}` - Update
- `DELETE /{teacher_id}` - Delete
- `POST /{teacher_id}/deactivate` - Deactivate

---

### Module 2: school_student

**Location:** `modules/school/school_student/`

**Backup Source:** `backup/modules/school/student/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | student/schemas.py | Verify completeness |
| repository.py | ⚠️ Basic | student/repository.py | Add full CRUD |
| service.py | ⚠️ Basic | student/service.py | Add business logic |
| router.py | ⚠️ Limited | student/api.py | Add endpoints |

**Required Import Fixes:**
- `backup.modules.school.student.schemas` → `.schemas`
- `backup.modules.school.student.repository` → `.repository`
- `modules.shared.database.get_async_db` → `modules.shared.database.get_db`

---

### Module 3: school_parent

**Location:** `modules/school/school_parent/`

**Backup Source:** `backup/modules/school/parent/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | parent/schemas.py | Verify completeness |
| repository.py | ⚠️ Basic | parent/repository.py | Add full CRUD |
| service.py | ⚠️ Basic | parent/service.py | Add business logic |
| router.py | ⚠️ Limited | parent/api.py | Add endpoints |

---

### Module 4: school_authority

**Location:** `modules/school/school_authority/`

**Backup Source:** `backup/modules/school/authority/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | authority/schemas.py | Verify completeness |
| repository.py | ⚠️ Basic | authority/repository.py | Add full CRUD |
| service.py | ⚠️ Basic | authority/service.py | Add business logic |
| router.py | ⚠️ Limited | authority/api.py | Add endpoints |

---

### Module 5: school_account_section

**Location:** `modules/school/school_account_section/`

**Backup Source:** `backup/modules/school/account_section/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ✅ Complete | account_section/schemas.py | Keep as-is |
| repository.py | ✅ Complete | account_section/repository.py | Keep as-is |
| service.py | ✅ Complete | account_section/service.py | Keep as-is |
| router.py | ✅ Complete | account_section/api.py | Keep as-is |

**Status:** This module appears complete - verify imports only.

---

### Module 6: school_library

**Location:** `modules/school/school_library/`

**Backup Source:** `backup/modules/school/library/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | library/schemas.py | Verify completeness |
| repository.py | ⚠️ Basic | library/repository.py | Add full CRUD |
| service.py | ⚠️ Basic | library/service.py | Add business logic |
| router.py | ⚠️ Limited | library/api.py | Add endpoints |

---

### Module 7: school_exam_section

**Location:** `modules/school/school_exam_section/`

**Backup Source:** `backup/modules/school/exam_section/`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | exam_section/models.py | Create from backup |
| schemas.py | 🆕 Empty | exam_section/schemas.py | Copy from backup |
| repository.py | 🆕 Empty | exam_section/repository.py | Copy from backup |
| service.py | 🆕 Empty | exam_section/service.py | Copy from backup |
| router.py | 🆕 Empty | exam_section/api.py | Copy from backup |

---

### Module 8: school_attendance

**Location:** `modules/school/school_attendance/`

**Backup Source:** Schema only in `backup/schemas/attendance.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | attendance.py | Expand from schema |
| repository.py | ⚠️ Basic | - | Create new |
| service.py | ⚠️ Basic | - | Create new |
| router.py | ⚠️ Limited | - | Create endpoints |

**Note:** Will need to create full module from schema + business logic.

---

### Module 9: school_courses

**Location:** `modules/school/school_courses/`

**Backup Source:** Schema only in `backup/schemas/course.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | ✅ Complete | - | Keep as-is |
| schemas.py | ⚠️ Partial | course.py | Expand from schema |
| repository.py | ⚠️ Basic | - | Create new |
| service.py | ⚠️ Basic | - | Create new |
| router.py | ⚠️ Limited | - | Create endpoints |

---

### Module 10: school_grades

**Location:** `modules/school/school_grades/`

**Backup Source:** Schema only in `backup/schemas/grade.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | grade.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 11: school_notices

**Location:** `modules/school/school_notices/`

**Backup Source:** Schema in `backup/schemas/notice.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | notice.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 12: school_tests

**Location:** `modules/school/school_tests/`

**Backup Source:** Schema in `backup/schemas/exam_schemas.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | exam_schemas.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 13: school_assignments

**Location:** `modules/school/school_assignments/`

**Backup Source:** Schema in `backup/schemas/assignment.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | assignment.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 14: school_timetable

**Location:** `modules/school/school_timetable/`

**Backup Source:** None - create new

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | - | Create new |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 15: school_dashboard

**Location:** `modules/school/school_dashboard/`

**Backup Source:** None - create new

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new (may not need) |
| schemas.py | 🆕 Empty | - | Create new |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 16: school_groups

**Location:** `modules/school/school_groups/`

**Backup Source:** Schema in `backup/schemas/group.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | group.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 17: school_chat

**Location:** `modules/school/school_chat/`

**Backup Source:** None - create new

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | - | Create new |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 18: school_notes

**Location:** `modules/school/school_notes/`

**Backup Source:** Schema in `backup/schemas/misc.py`

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | misc.py | Copy from backup |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

### Module 19: school_videos

**Location:** `modules/school/school_videos/`

**Backup Source:** None - create new

| File | Current State | Source | Action |
|------|---------------|--------|--------|
| models.py | 🆕 Empty | - | Create new |
| schemas.py | 🆕 Empty | - | Create new |
| repository.py | 🆕 Empty | - | Create new |
| service.py | 🆕 Empty | - | Create new |
| router.py | 🆕 Empty | - | Create new |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Total Modules | 19 |
| Has Complete Backup Source | 7 |
| Has Partial Backup (schema only) | 7 |
| Need to Create from Scratch | 5 |

### Migration Effort by Category

| Priority | Modules | Action Required |
|----------|---------|-----------------|
| High | school_teacher, school_student, school_parent, school_authority | Enhance with full CRUD |
| Medium | school_account_section, school_library, school_exam_section | Verify + fix imports |
| Low | school_attendance, school_courses, school_grades, school_notices, school_tests, school_assignments | Create module from schema |
| New | school_timetable, school_dashboard, school_chat, school_notes, school_videos | Create completely new |

---

## Execution Order

### Phase 1: Complete Modules (from backup)
1. school_teacher ✅ - Already has detailed plan
2. school_student
3. school_parent
4. school_authority

### Phase 2: Verify and Fix
5. school_account_section
6. school_library
7. school_exam_section

### Phase 3: Create from Schema
8. school_attendance
9. school_courses
10. school_grades
11. school_notices
12. school_tests
13. school_assignments
14. school_groups

### Phase 4: New Modules
15. school_timetable
16. school_dashboard
17. school_chat
18. school_notes
19. school_videos

---

## Common Import Fixes for All Modules

| Old Import | New Import |
|------------|------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from backup.modules.school.<module>.<file>` | `from modules.school.school_<module>.<file>` |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |
| `from backup.schemas.<schema>` | `from modules.school.school_<module>.schemas` |

---

## Next Steps

1. Approve this comprehensive plan
2. Begin Phase 1 with school_teacher module (detailed plan already created)
3. Continue sequentially through all modules
4. Test each module after implementation
