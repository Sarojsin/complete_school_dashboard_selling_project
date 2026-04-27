# 👑 ELITE PLAN 7 — Super Admin Module
## Phase: SUPER ADMIN — System-wide control, dashboard, reports, settings, backups
### Goal: Migrate all admin_* files into a single powerful modules/super_admin/

---

## 📌 Pre-Conditions (from Plan 6)
- [ ] ✅ `modules/auth/` is fully working
- [ ] ✅ `UserRole.SUPER_ADMIN` exists in `modules/auth/schemas.py`
- [ ] ✅ `require_super_admin` dependency in `modules/auth/dependencies.py`
- [ ] ✅ App starts clean, auth login endpoint works

---

## 🗂️ Source Files → Super Admin Module Mapping

These `app/api/endpoints/admin_*.py` files all merge into `modules/super_admin/`:

| Old File | Size | Destination |
|----------|------|-----------|
| `admin_dashboard.py` | 5166 | `super_admin/api.py` (dashboard routes) |
| `admin_users.py` | 6647 | `super_admin/api.py` (user management routes) |
| `admin_settings.py` | 12975 | `super_admin/api.py` (settings routes) |
| `admin_features.py` | 13478 | `super_admin/api.py` (feature toggle routes) |
| `admin_reports.py` | 20544 | `super_admin/api.py` (report routes) |
| `admin_security.py` | 15903 | `super_admin/api.py` (security routes) |
| `admin_advanced.py` | 16948 | `super_admin/api.py` (advanced routes) |
| `admin_backup.py` | 10930 | `super_admin/api.py` (backup routes) |
| `admin_academic.py` | 5826 | `super_admin/api.py` (academic admin routes) |
| `admin_finance.py` | 5178 | `super_admin/api.py` (finance overview routes) |
| `admin_exams.py` | 3903 | `super_admin/api.py` (exam oversight routes) |
| `admin_notices.py` | 3538 | `super_admin/api.py` (notice management routes) |
| `admin_messages.py` | 1839 | `super_admin/api.py` (message routes) |
| `admin_media.py` | 8948 | `super_admin/api.py` (media management routes) |
| `admin_system.py` | 2505 | `super_admin/api.py` (system health routes) |

| Old Service File | Destination |
|-----------------|-----------|
| `admin_user_service.py` | `super_admin/service.py` |
| `admin_academic_service.py` | `super_admin/service.py` |
| `admin_backup_service.py` | `super_admin/service.py` |
| `admin_exam_service.py` | `super_admin/service.py` |
| `admin_finance_service.py` | `super_admin/service.py` (system-wide parts) |
| `admin_system_service.py` | `super_admin/service.py` |
| `admin_notice_service.py` | `super_admin/service.py` |
| `admin_message_service.py` | `super_admin/service.py` |
| `feature_service.py` | `super_admin/service.py` |
| `dashboard_service.py` | `super_admin/service.py` |

| Old Repository File | Destination |
|--------------------|-----------|
| `admin_user_repository.py` | `super_admin/repository.py` |
| `admin_finance_repository.py` | `super_admin/repository.py` |
| `admin_academic_repository.py` | `super_admin/repository.py` |
| `admin_exam_repository.py` | `super_admin/repository.py` |
| `admin_backup_repository.py` | `super_admin/repository.py` |
| `admin_notice_repository.py` | `super_admin/repository.py` |
| `admin_message_repository.py` | `super_admin/repository.py` |
| `admin_settings_repository.py` | `super_admin/repository.py` |
| `admin_system_repository.py` | `super_admin/repository.py` |
| `dashboard_repository.py` | `super_admin/repository.py` |
| `feature_repository.py` | `super_admin/repository.py` |

---

## 🏗️ Target Module Structure

```
modules/super_admin/
├── __init__.py
├── models.py          ← SystemLog, AuditLog, SystemSetting, Feature (from admin_models.py)
├── schemas.py         ← All admin request/response schemas (from app/schemas/admin.py + misc.py)
├── repository.py      ← Merged from 11 admin_*_repository.py files
├── service.py         ← Merged from 10 admin_*_service.py files
├── api.py             ← Merged from 15 admin_*.py endpoint files
├── constants.py       ← Admin roles, permission constants
├── exceptions.py      ← AdminNotFoundException, UnauthorizedAdminAction
├── web.py             ← Web routes if Jinja2 dashboard templates needed
└── templates/         ← Admin dashboard HTML (from app/templates/admin/)
```

---

## ✅ STEP 1 — Create Folder

```powershell
New-Item -ItemType Directory -Force -Path "modules\super_admin\templates"
New-Item -ItemType Directory -Force -Path "modules\super_admin\tests"
New-Item -ItemType File    -Force -Path "modules\super_admin\__init__.py"
```

---

## ✅ STEP 2 — Build `models.py`

Source: `app/models/admin_models.py` (9628 bytes)

```python
# modules/super_admin/models.py
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum as SAEnum
from sqlalchemy.sql import func

# ── From admin_models.py ────────────────────────────
class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_enabled = Column(Boolean, default=True)
    description = Column(Text)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)            # no FK to keep it independent
    action = Column(String(200))
    details = Column(JSON)
    ip_address = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class SystemBackup(Base):
    __tablename__ = "system_backups"
    id = Column(Integer, primary_key=True)
    filename = Column(String(300))
    size_bytes = Column(Integer)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, server_default=func.now())
```

---

## ✅ STEP 3 — Build `schemas.py`

Source: `app/schemas/admin.py` (418 bytes) + `app/schemas/misc.py` (2775 bytes)

```python
# modules/super_admin/schemas.py
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

class SystemSettingUpdate(BaseModel):
    value: str

class SystemSettingResponse(BaseModel):
    key: str
    value: str
    updated_at: datetime
    class Config: from_attributes = True

class FeatureToggle(BaseModel):
    is_enabled: bool

class FeatureResponse(BaseModel):
    name: str
    is_enabled: bool
    description: Optional[str]
    class Config: from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    created_at: datetime
    class Config: from_attributes = True

class BackupResponse(BaseModel):
    id: int
    filename: str
    size_bytes: int
    status: str
    created_at: datetime
    class Config: from_attributes = True

class DashboardStats(BaseModel):
    total_schools: int
    total_colleges: int
    total_users: int
    total_students: int
    total_teachers: int
    active_sessions: int
    system_health: str

class UserManageResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    class Config: from_attributes = True
```

---

## ✅ STEP 4 — Build `repository.py`

Merge all 11 admin repository files. Structure by domain:

```python
# modules/super_admin/repository.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from modules.super_admin.models import SystemSetting, Feature, AuditLog, SystemBackup
# Import User from shared (or app.models.models until fully migrated)
from app.models.models import User  # Adjust as needed

class UserManagementRepository:
    """From admin_user_repository.py"""
    def __init__(self, db: Session): self.db = db

    def get_all_users(self, skip=0, limit=100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def deactivate_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
        return user

    def count_users_by_role(self):
        return self.db.query(User.role, func.count(User.id)).group_by(User.role).all()

class SettingsRepository:
    """From admin_settings_repository.py"""
    def __init__(self, db: Session): self.db = db

    def get_setting(self, key: str):
        return self.db.query(SystemSetting).filter(SystemSetting.key == key).first()

    def set_setting(self, key: str, value: str):
        setting = self.get_setting(key)
        if setting:
            setting.value = value
        else:
            setting = SystemSetting(key=key, value=value)
            self.db.add(setting)
        self.db.commit()
        return setting

    def get_all_settings(self):
        return self.db.query(SystemSetting).all()

class FeatureRepository:
    """From feature_repository.py"""
    def __init__(self, db: Session): self.db = db

    def get_all_features(self):
        return self.db.query(Feature).all()

    def toggle_feature(self, feature_name: str, enabled: bool):
        feature = self.db.query(Feature).filter(Feature.name == feature_name).first()
        if feature:
            feature.is_enabled = enabled
            self.db.commit()
        return feature

class AuditRepository:
    """From admin_system_repository.py"""
    def __init__(self, db: Session): self.db = db

    def log_action(self, user_id: int, action: str, details: dict = None, ip: str = None):
        log = AuditLog(user_id=user_id, action=action, details=details, ip_address=ip)
        self.db.add(log)
        self.db.commit()
        return log

    def get_recent_logs(self, limit=100):
        return self.db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()

class BackupRepository:
    """From admin_backup_repository.py"""
    def __init__(self, db: Session): self.db = db

    def record_backup(self, filename: str, size: int):
        backup = SystemBackup(filename=filename, size_bytes=size)
        self.db.add(backup)
        self.db.commit()
        return backup

    def get_all_backups(self):
        return self.db.query(SystemBackup).order_by(SystemBackup.created_at.desc()).all()

class DashboardRepository:
    """From dashboard_repository.py"""
    def __init__(self, db: Session): self.db = db

    def get_dashboard_stats(self) -> dict:
        from app.models.models import User  # adjust
        total_users = self.db.query(func.count(User.id)).scalar()
        return {"total_users": total_users}
```

---

## ✅ STEP 5 — Build `service.py`

```python
# modules/super_admin/service.py
from sqlalchemy.orm import Session
from modules.super_admin.repository import (
    UserManagementRepository, SettingsRepository,
    FeatureRepository, AuditRepository, BackupRepository, DashboardRepository
)
from modules.super_admin.schemas import DashboardStats
from modules.admin_backup_service import AdminBackupService  # move/inline as needed
import subprocess, os

class SuperAdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo    = UserManagementRepository(db)
        self.setting_repo = SettingsRepository(db)
        self.feature_repo = FeatureRepository(db)
        self.audit_repo   = AuditRepository(db)
        self.backup_repo  = BackupRepository(db)
        self.dashboard_repo = DashboardRepository(db)

    # ── Dashboard ─────────────────────────────────────
    def get_dashboard_stats(self) -> DashboardStats:
        raw = self.dashboard_repo.get_dashboard_stats()
        return DashboardStats(**raw, total_schools=0, total_colleges=0,
                              total_students=0, total_teachers=0,
                              active_sessions=0, system_health="healthy")

    # ── User Management ───────────────────────────────
    def list_all_users(self, skip=0, limit=100):
        return self.user_repo.get_all_users(skip, limit)

    def deactivate_user(self, user_id: int, admin_id: int):
        result = self.user_repo.deactivate_user(user_id)
        self.audit_repo.log_action(admin_id, f"DEACTIVATE_USER:{user_id}")
        return result

    # ── Settings ──────────────────────────────────────
    def update_setting(self, key: str, value: str, admin_id: int):
        result = self.setting_repo.set_setting(key, value)
        self.audit_repo.log_action(admin_id, f"UPDATE_SETTING:{key}", {"value": value})
        return result

    def get_all_settings(self):
        return self.setting_repo.get_all_settings()

    # ── Features ──────────────────────────────────────
    def toggle_feature(self, name: str, enabled: bool, admin_id: int):
        result = self.feature_repo.toggle_feature(name, enabled)
        self.audit_repo.log_action(admin_id, f"TOGGLE_FEATURE:{name}", {"enabled": enabled})
        return result

    # ── Audit Logs ────────────────────────────────────
    def get_audit_logs(self, limit=100):
        return self.audit_repo.get_recent_logs(limit)

    # ── Backups ───────────────────────────────────────
    def create_backup(self, admin_id: int):
        # Logic from admin_backup_service.py
        filename = f"backup_{admin_id}.sql"
        self.backup_repo.record_backup(filename, 0)
        self.audit_repo.log_action(admin_id, "CREATE_BACKUP")
        return {"filename": filename, "status": "initiated"}

    def get_all_backups(self):
        return self.backup_repo.get_all_backups()
```

---

## ✅ STEP 6 — Build `api.py` (Organized by Domain)

```python
# modules/super_admin/api.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.auth.dependencies import require_super_admin
from modules.super_admin.service import SuperAdminService
from modules.super_admin.schemas import (
    SystemSettingUpdate, FeatureToggle, DashboardStats
)

router = APIRouter()
ADMIN_DEP = [Depends(require_super_admin)]

# ── Dashboard ─────────────────────────────────────────
@router.get("/dashboard", dependencies=ADMIN_DEP, response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    return SuperAdminService(db).get_dashboard_stats()

# ── User Management ───────────────────────────────────
@router.get("/users", dependencies=ADMIN_DEP)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SuperAdminService(db).list_all_users(skip, limit)

@router.put("/users/{user_id}/deactivate", dependencies=ADMIN_DEP)
def deactivate_user(user_id: int, current_user=Depends(require_super_admin), db: Session = Depends(get_db)):
    return SuperAdminService(db).deactivate_user(user_id, current_user.id)

# ── Settings ──────────────────────────────────────────
@router.get("/settings", dependencies=ADMIN_DEP)
def list_settings(db: Session = Depends(get_db)):
    return SuperAdminService(db).get_all_settings()

@router.put("/settings/{key}", dependencies=ADMIN_DEP)
def update_setting(key: str, data: SystemSettingUpdate, current_user=Depends(require_super_admin), db: Session = Depends(get_db)):
    return SuperAdminService(db).update_setting(key, data.value, current_user.id)

# ── Features ──────────────────────────────────────────
@router.get("/features", dependencies=ADMIN_DEP)
def list_features(db: Session = Depends(get_db)):
    return SuperAdminService(db).feature_repo.get_all_features()

@router.put("/features/{name}/toggle", dependencies=ADMIN_DEP)
def toggle_feature(name: str, data: FeatureToggle, current_user=Depends(require_super_admin), db: Session = Depends(get_db)):
    return SuperAdminService(db).toggle_feature(name, data.is_enabled, current_user.id)

# ── Audit Logs ────────────────────────────────────────
@router.get("/audit-logs", dependencies=ADMIN_DEP)
def audit_logs(limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return SuperAdminService(db).get_audit_logs(limit)

# ── Backups ───────────────────────────────────────────
@router.get("/backups", dependencies=ADMIN_DEP)
def list_backups(db: Session = Depends(get_db)):
    return SuperAdminService(db).get_all_backups()

@router.post("/backups", dependencies=ADMIN_DEP)
def create_backup(current_user=Depends(require_super_admin), db: Session = Depends(get_db)):
    return SuperAdminService(db).create_backup(current_user.id)

# ── Schools & Colleges Overview ───────────────────────
@router.get("/schools", dependencies=ADMIN_DEP)
def list_schools(db: Session = Depends(get_db)):
    """System-wide list of all school authorities"""
    # Calls school_authority service
    from modules.school_authority.repository import AuthorityRepository
    return AuthorityRepository(db).get_all()

@router.get("/colleges", dependencies=ADMIN_DEP)
def list_colleges(db: Session = Depends(get_db)):
    """System-wide list of all college faculty/HODs"""
    from modules.college_hod.repository import HodRepository
    return HodRepository(db).get_all()
```

---

## ✅ STEP 7 — Add `constants.py`

```python
# modules/super_admin/constants.py

SUPER_ADMIN_ROLE = "super_admin"

# Feature names
FEATURE_CHAT = "chat"
FEATURE_GROUPS = "groups"
FEATURE_ASSIGNMENTS = "assignments"
FEATURE_LIBRARY = "library"
FEATURE_ATTENDANCE = "attendance"
FEATURE_REPORTS = "reports"
FEATURE_BACKUPS = "backups"

# Audit action types
ACTION_CREATE_USER = "CREATE_USER"
ACTION_DEACTIVATE_USER = "DEACTIVATE_USER"
ACTION_UPDATE_SETTING = "UPDATE_SETTING"
ACTION_TOGGLE_FEATURE = "TOGGLE_FEATURE"
ACTION_CREATE_BACKUP = "CREATE_BACKUP"
ACTION_DELETE_USER = "DELETE_USER"
```

---

## ✅ STEP 8 — Wire into app/main.py

```python
from modules.super_admin.api import router as super_admin_router
app.include_router(super_admin_router, prefix="/api/v1/admin", tags=["👑 Super Admin"])
```

---

## 📊 Phase 7 Completion Checklist

- [ ] `modules/super_admin/` folder with all 8 files created
- [ ] `models.py` — SystemSetting, Feature, AuditLog, SystemBackup created
- [ ] `schemas.py` — DashboardStats, UserManageResponse, etc. defined
- [ ] `repository.py` — All 5 repository classes operational
- [ ] `service.py` — SuperAdminService with all domains working
- [ ] `api.py` — All routes protected with `require_super_admin`
- [ ] `GET /api/v1/admin/dashboard` works with super admin JWT
- [ ] `GET /api/v1/admin/users` returns list of all users
- [ ] `GET /api/v1/admin/audit-logs` returns recent actions
- [ ] `GET /api/v1/admin/settings` returns system settings
- [ ] `POST /api/v1/admin/backups` initiates a backup
- [ ] Non-super-admin user gets 403 on all /admin/ routes
- [ ] All audit-sensitive actions create an AuditLog entry
