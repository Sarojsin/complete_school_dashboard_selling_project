# Plan: Migrate school_library Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_library/)
All files are **EMPTY** - needs complete migration from backup.

| File | Current State | Action Required |
|------|---------------|-----------------|
| `models.py` | 🆕 Empty | Check if models exist elsewhere |
| `schemas.py` | 🆕 Empty | Copy from backup |
| `repository.py` | 🆕 Empty | Copy from backup |
| `service.py` | 🆕 Empty | Copy from backup |
| `router.py` | 🆕 Empty | Copy from backup (rename api.py) |

### Source from Backup (backup/modules/school/library/)
| File | Contents |
|------|----------|
| `schemas.py` | Library schemas (Book, Issue, etc.) |
| `repository.py` | Full CRUD operations for library |
| `service.py` | Business logic for library |
| `api.py` | API endpoints |
| `constants.py` | Module constants |
| `exceptions.py` | Custom exceptions |
| `utils.py` | Utility functions |

**Note:** No models.py in backup - models may be in main app/models/

---

## Migration Steps

### Step 1: Check/Create Models
- Check main app for library models
- If needed, create models.py or use shared models

### Step 2: Copy All Files from Backup
- `schemas.py` → Copy from backup
- `repository.py` → Copy from backup
- `service.py` → Copy from backup
- `api.py` → Copy and rename to `router.py`

### Step 3: Fix Imports

| Old (backup) | New (modules) |
|--------------|---------------|
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. Approve this plan → Proceed to implementation in Code mode
2. Continue to next module
