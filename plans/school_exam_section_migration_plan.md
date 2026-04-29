# Plan: Migrate school_exam_section Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_exam_section/)
All files are **EMPTY** - needs complete migration from backup.

| File | Current State | Action Required |
|------|---------------|-----------------|
| `models.py` | 🆕 Empty | Create or check existing models |
| `schemas.py` | 🆕 Empty | Copy from backup |
| `repository.py` | 🆕 Empty | Copy from backup |
| `service.py` | 🆕 Empty | Copy from backup |
| `router.py` | 🆕 Empty | Copy from backup (rename api.py) |

### Source from Backup (backup/modules/school/exam_section/)
| File | Contents |
|------|----------|
| `schemas.py` | Exam section schemas |
| `repository.py` | CRUD operations |
| `service.py` | Business logic |
| `api.py` | API endpoints |

---

## Migration Steps

### Step 1: Check/Create Models
- Check for existing exam models in app

### Step 2: Copy All Files from Backup
- Copy all files and fix imports

### Step 3: Fix Imports

| Old (backup) | New (modules) |
|--------------|---------------|
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. Approve this plan → Proceed to implementation
2. Continue to next module
