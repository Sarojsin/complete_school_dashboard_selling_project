# Missing Endpoints Migration Plan - Priority 7: Admin Advanced Modules

**Plan 7: Admin Advanced Features**

This plan covers remaining admin modules: Security, Settings, Backup, Reports, Media, System, Messages, Notices.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Admin Security | 21 endpoints | LOW |
| Admin Settings | 18 endpoints | LOW |
| Admin Backup | 11 endpoints | LOW |
| Admin Reports | 9 endpoints | LOW |
| Admin Media | 7 endpoints | LOW |
| Admin System | 7 endpoints | LOW |
| Admin Messages | 3 endpoints | LOW |
| Admin Notices | 8 endpoints | LOW |

---

## 1. Admin Security Module

**Target Location:** `modules/super_admin/security/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/security/audit-logs` | Get audit logs | backup/api/endpoints/admin_security.py |
| GET | `/api/security/audit-logs/{log_id}` | Get audit log detail | backup/api/endpoints/admin_security.py |
| GET | `/api/security/settings` | Get security settings | backup/api/endpoints/admin_security.py |
| PATCH | `/api/security/settings` | Update security settings | backup/api/endpoints/admin_security.py |
| GET | `/api/security/jwt` | Get JWT settings | backup/api/endpoints/admin_security.py |
| PATCH | `/api/security/jwt` | Update JWT settings | backup/api/endpoints/admin_security.py |
| GET | `/api/security/ip-whitelist` | Get IP whitelist | backup/api/endpoints/admin_security.py |
| POST | `/api/security/ip-whitelist` | Add IP to whitelist | backup/api/endpoints/admin_security.py |
| DELETE | `/api/security/ip-whitelist/{ip_id}` | Remove IP from whitelist | backup/api/endpoints/admin_security.py |
| GET | `/api/security/password-policy` | Get password policy | backup/api/endpoints/admin_security.py |
| PATCH | `/api/security/password-policy` | Update password policy | backup/api/endpoints/admin_security.py |
| GET | `/api/security/failed-logins` | Get failed logins | backup/api/endpoints/admin_security.py |
| POST | `/api/security/unlock-account/{user_id}` | Unlock user account | backup/api/endpoints/admin_security.py |
| GET | `/api/security/2fa/status` | Get 2FA status | backup/api/endpoints/admin_security.py |
| POST | `/api/security/2fa/enable` | Enable 2FA | backup/api/endpoints/admin_security.py |
| POST | `/api/security/2fa/disable` | Disable 2FA | backup/api/endpoints/admin_security.py |
| GET | `/api/security/sessions` | Get active sessions | backup/api/endpoints/admin_security.py |
| DELETE | `/api/security/sessions/{session_id}` | Invalidate session | backup/api/endpoints/admin_security.py |
| DELETE | `/api/security/sessions/user/{user_id}` | Force logout user | backup/api/endpoints/admin_security.py |
| GET | `/api/security/dashboard` | Get security dashboard | backup/api/endpoints/admin_security.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/security/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Implement API endpoints**

---

## 2. Admin Settings Module

**Target Location:** `modules/super_admin/settings/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/settings/general` | Get general settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/general` | Update general settings | backup/api/endpoints/admin_settings.py |
| POST | `/api/settings/logo` | Upload school logo | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/academic` | Get academic settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/academic` | Update academic settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/localization` | Get localization settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/localization` | Update localization settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/smtp` | Get SMTP settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/smtp` | Update SMTP settings | backup/api/endpoints/admin_settings.py |
| POST | `/api/settings/smtp/test` | Test SMTP settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/payment` | Get payment settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/payment` | Update payment settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/notifications` | Get notification settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/notifications` | Update notification settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/features` | Get feature settings | backup/api/endpoints/admin_settings.py |
| PATCH | `/api/settings/features` | Update feature settings | backup/api/endpoints/admin_settings.py |
| GET | `/api/settings/all` | Get all settings | backup/api/endpoints/admin_settings.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/settings/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Implement API endpoints**

---

## 3. Admin Backup Module

**Target Location:** `modules/super_admin/backup/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/backup/create` | Create backup | backup/api/endpoints/admin_backup.py |
| GET | `/api/backup/list` | List backups | backup/api/endpoints/admin_backup.py |
| GET | `/api/backup/{backup_id}/download` | Download backup | backup/api/endpoints/admin_backup.py |
| POST | `/api/backup/{backup_id}/restore` | Restore backup | backup/api/endpoints/admin_backup.py |
| DELETE | `/api/backup/{backup_id}` | Delete backup | backup/api/endpoints/admin_backup.py |
| GET | `/api/backup/schedule` | Get backup schedule | backup/api/endpoints/admin_backup.py |
| PATCH | `/api/backup/schedule` | Update backup schedule | backup/api/endpoints/admin_backup.py |
| GET | `/api/backup/status` | Get backup status | backup/api/endpoints/admin_backup.py |
| POST | `/api/backup/export` | Export data | backup/api/endpoints/admin_backup.py |
| POST | `/api/backup/import` | Import data | backup/api/endpoints/admin_backup.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/backup/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Implement API endpoints**

---

## 4. Admin Reports Module

**Target Location:** `modules/super_admin/reports/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/reports/attendance/students` | Get student attendance report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/fees/due` | Get fee due report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/teachers/performance` | Get teacher performance report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/exams/performance` | Get exam performance report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/library/overdue` | Get library overdue report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/finance/summary` | Get financial report | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/export/csv` | Export report CSV | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/export/pdf` | Export report PDF | backup/api/endpoints/admin_reports.py |
| GET | `/api/reports/comprehensive` | Get comprehensive report | backup/api/endpoints/admin_reports.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/reports/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Implement API endpoints**

---

## 5. Remaining Admin Modules

### Admin Media (7 endpoints)
- **Location:** `modules/super_admin/media/`
- **Source:** backup/api/endpoints/admin_media.py

### Admin System (7 endpoints)
- **Location:** `modules/super_admin/system/`
- **Source:** backup/api/endpoints/admin_system.py

### Admin Messages (3 endpoints)
- **Location:** `modules/super_admin/messages/`
- **Source:** backup/api/endpoints/admin_messages.py

### Admin Notices (8 endpoints)
- **Location:** `modules/super_admin/notices/`
- **Source:** backup/api/endpoints/admin_notices.py

---

## Migration Strategy

### Step 1: Create All Module Structures
```
modules/super_admin/
├── security/
├── settings/
├── backup/
├── reports/
├── media/
├── system/
├── messages/
└── notices/
```

### Step 2: Implement Endpoints
- Follow pattern from previous admin modules
- Ensure consistent error handling

### Step 3: Integration
- Register all routes in main.py
- Test end-to-end functionality

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Admin Security | 3-4 days | 1 day |
| Admin Settings | 2-3 days | 1 day |
| Admin Backup | 2 days | 0.5 day |
| Admin Reports | 2-3 days | 1 day |
| Admin Media | 1-2 days | 0.5 day |
| Admin System | 1-2 days | 0.5 day |
| Admin Messages | 0.5 day | 0.25 day |
| Admin Notices | 1 day | 0.5 day |
| **Total** | **12.5-17.5 days** | **5.25 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/admin_security.py`
- `backup/api/endpoints/admin_settings.py`
- `backup/api/endpoints/admin_backup.py`
- `backup/api/endpoints/admin_reports.py`
- `backup/api/endpoints/admin_media.py`
- `backup/api/endpoints/admin_system.py`
- `backup/api/endpoints/admin_messages.py`
- `backup/api/endpoints/admin_notices.py`

---

## Integration Notes

1. **Admin Security:** Requires integration with authentication system
2. **Admin Settings:** Need to handle sensitive data securely
3. **Admin Backup:** Need file storage integration
4. **Admin Reports:** Need PDF/CSV generation libraries

---

*Plan created: 2026-03-26*
