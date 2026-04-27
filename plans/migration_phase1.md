# Migration Phase 1: Setup Shared Infrastructure

**Duration:** 1-2 days  
**Goal:** Create shared folder structure and move common components

---

## Overview

Phase 1 sets up the foundation for the new structure by creating shared directories and moving common components (auth, middleware, utils) to a shared location.

---

## Current State

```
app/
├── api/endpoints/
├── core/
├── dependencies/         # ← Will move to shared/
├── middleware/         # ← Will move to shared/
├── models/
├── repositories/
├── schemas/
├── services/
├── templates/
└── web/
```

---

## Target State After Phase 1

```
app/
├── core/                  # Keep as is (config, database)
├── shared/               # ← NEW: Shared components
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── jwt.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── feature_check.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── api/
├── models/
├── repositories/
├── schemas/
├── services/
├── templates/
└── web/
```

---

## Step-by-Step Tasks

### Step 1: Create Shared Directory Structure

Create the following folders:
```
app/shared/
app/shared/auth/
app/shared/middleware/
app/shared/utils/
```

### Step 2: Move Authentication Components

**File: `app/dependencies/auth.py`**
- Move to → `app/shared/auth/dependencies.py`

**Create new file: `app/shared/auth/jwt.py`**
```python
# JWT handling functions
# Extract from existing code and organize
```

**Create: `app/shared/auth/__init__.py`**
```python
from .dependencies import get_current_user
from .jwt import create_access_token, verify_token

__all__ = ["get_current_user", "create_access_token", "verify_token"]
```

### Step 3: Move Middleware Components

**File: `app/middleware/security.py`**
- Move to → `app/shared/middleware/security.py`

**File: `app/middleware/feature_check.py`**
- Move to → `app/shared/middleware/feature_check.py`

**File: `app/middleware/csrf.py`**
- Move to → `app/shared/middleware/csrf.py`

**Create: `app/shared/middleware/__init__.py`**
```python
from .security import SecurityHeadersMiddleware
from .feature_check import require_feature, Features
from .csrf import CSRFMiddleware

__all__ = [
    "SecurityHeadersMiddleware",
    "require_feature", 
    "Features",
    "CSRFMiddleware"
]
```

### Step 4: Create Utils (if needed)

**Create: `app/shared/utils/helpers.py`**
```python
# Common helper functions used across modules
```

**Create: `app/shared/utils/__init__.py`**
```python
from .helpers import *

__all__ = []
```

### Step 5: Update Imports in main.py

**File: `app/main.py`**

Change imports from:
```python
from app.dependencies.auth import get_current_user
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.feature_check import require_feature
```

To:
```python
from app.shared.auth import get_current_user
from app.shared.middleware import SecurityHeadersMiddleware, require_feature
```

### Step 6: Update All Other Files

Update imports in all files that use these components:
- `app/api/endpoints/auth.py`
- `app/api/endpoints/students.py`
- `app/api/endpoints/teachers.py`
- `app/api/endpoints/authority.py`
- All other endpoint files
- All repository files
- All service files

---

## Files to Create

| File | Purpose |
|------|---------|
| `app/shared/__init__.py` | Package init |
| `app/shared/auth/__init__.py` | Auth package init |
| `app/shared/auth/dependencies.py` | Auth dependencies (move from dependencies/) |
| `app/shared/auth/jwt.py` | JWT functions |
| `app/shared/middleware/__init__.py` | Middleware package init |
| `app/shared/utils/__init__.py` | Utils package init |
| `app/shared/utils/helpers.py` | Common helpers |

---

## Files to Move

| Current Location | New Location |
|-----------------|---------------|
| `app/dependencies/auth.py` | `app/shared/auth/dependencies.py` |
| `app/middleware/security.py` | `app/shared/middleware/security.py` |
| `app/middleware/feature_check.py` | `app/shared/middleware/feature_check.py` |
| `app/middleware/csrf.py` | `app/shared/middleware/csrf.py` |

---

## Files to Modify

| File | Change |
|------|--------|
| `app/main.py` | Update imports |
| `app/api/endpoints/auth.py` | Update import path |
| `app/api/endpoints/students.py` | Update import path |
| `app/api/endpoints/teachers.py` | Update import path |
| `app/api/endpoints/authority.py` | Update import path |
| All other endpoint files | Update import paths |
| All repository files | Update import paths |

---

## Verification Checklist

- [ ] `app/shared/` directory created
- [ ] `app/shared/auth/` with all files
- [ ] `app/shared/middleware/` with all files
- [ ] `app/shared/utils/` created
- [ ] `app/main.py` imports updated
- [ ] All endpoint files imports updated
- [ ] All repository imports updated
- [ ] Application runs without errors
- [ ] Login/logout works

---

## Testing Commands

```bash
# Test imports
python -c "from app.shared.auth import get_current_user"
python -c "from app.shared.middleware import SecurityHeadersMiddleware"

# Test application
python run.py
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Import errors | Check PYTHONPATH or use relative imports |
| Circular imports | Keep shared dependencies minimal |
| Missing files | Verify all files moved correctly |

---

## Next Phase

After Phase 1 → Go to [Phase 2: Restructure Models](migration_phase2.md)

---

*End of Phase 1*
