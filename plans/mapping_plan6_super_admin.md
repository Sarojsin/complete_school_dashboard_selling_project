# Endpoint Mapping Plan 6: Super Admin & System Modules

## Overview

This document maps all super admin and system endpoints from the monolithic backup to the new modular structure.

---

## Source Files Analyzed

| File | Endpoints Count |
|------|-----------------|
| `backup/api/endpoints/admin_dashboard.py` | 11 endpoints |
| `backup/api/endpoints/admin_users.py` | 12 endpoints |
| `backup/api/endpoints/admin_academic.py` | 11 endpoints |
| `backup/api/endpoints/admin_exams.py` | 9 endpoints |
| `backup/api/endpoints/admin_finance.py` | 10 endpoints |
| `backup/api/endpoints/admin_notices.py` | 8 endpoints |
| `backup/api/endpoints/admin_messages.py` | 3 endpoints |
| `backup/api/endpoints/admin_media.py` | 7 endpoints |
| `backup/api/endpoints/admin_system.py` | 7 endpoints |
| `backup/api/endpoints/admin_security.py` | 20 endpoints |
| `backup/api/endpoints/admin_backup.py` | 10 endpoints |
| `backup/api/endpoints/admin_reports.py` | 9 endpoints |
| `backup/api/endpoints/admin_settings.py` | 17 endpoints |
| `backup/api/endpoints/admin_advanced.py` | 15 endpoints |
| `backup/api/endpoints/admin_features.py` | 14 endpoints |
| **Total** | **~163 endpoints** |

---

## Endpoint Mapping Table

### Admin Dashboard Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/dashboard` | `super_admin` | `/admin/dashboard` | Get dashboard |
| GET | `/api/stats` | `super_admin` | `/admin/stats` | Get system stats |
| GET | `/api/users/count` | `super_admin` | `/admin/users/count` | Get users by role |
| GET | `/api/overview` | `super_admin` | `/admin/overview` | Dashboard overview |
| GET | `/api/features/summary` | `super_admin` | `/admin/features/summary` | Features summary |
| GET | `/api/features/enabled` | `super_admin` | `/admin/features/enabled` | Enabled features |
| GET | `/api/features/disabled` | `super_admin` | `/admin/features/disabled` | Disabled features |
| GET | `/api/analytics/enrollment` | `super_admin` | `/admin/analytics/enrollment` | Enrollment analytics |
| GET | `/api/analytics/fees` | `super_admin` | `/admin/analytics/fees` | Fee analytics |
| GET | `/api/analytics/attendance` | `super_admin` | `/admin/analytics/attendance` | Attendance analytics |
| GET | `/api/analytics/exams` | `super_admin` | `/admin/analytics/exams` | Exam analytics |
| GET | `/api/analytics/summary` | `super_admin` | `/admin/analytics/summary` | Analytics summary |

### Admin Users Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/users` | `super_admin` | `/admin/users/` | Get all users |
| GET | `/api/users/{user_id}` | `super_admin` | `/admin/users/{user_id}` | Get user |
| PATCH | `/api/users/{user_id}/toggle-active` | `super_admin` | `/admin/users/{user_id}/toggle-active` | Toggle active |
| POST | `/api/users/{user_id}/reset-password` | `super_admin` | `/admin/users/{user_id}/reset-password` | Reset password |
| POST | `/api/users/{user_id}/lock` | `super_admin` | `/admin/users/{user_id}/lock` | Lock account |
| POST | `/api/users/{user_id}/force-logout` | `super_admin` | `/admin/users/{user_id}/force-logout` | Force logout |
| GET | `/api/users/{user_id}/login-history` | `super_admin` | `/admin/users/{user_id}/login-history` | Login history |
| POST | `/api/users/{user_id}/change-role` | `super_admin` | `/admin/users/{user_id}/change-role` | Change role |
| GET | `/api/users/stats/by-role` | `super_admin` | `/admin/users/stats/by-role` | User stats |
| GET | `/api/users/students/list` | `super_admin` | `/admin/users/students` | Students list |
| GET | `/api/users/teachers/list` | `super_admin` | `/admin/users/teachers` | Teachers list |
| GET | `/api/users/parents/list` | `super_admin` | `/admin/users/parents` | Parents list |

### Admin Academic Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/courses` | `super_admin` | `/admin/courses` | All courses (admin) |
| POST | `/api/courses` | `super_admin` | `/admin/courses` | Create course (admin) |
| PATCH | `/api/courses/{course_id}` | `super_admin` | `/admin/courses/{course_id}` | Update course |
| DELETE | `/api/courses/{course_id}` | `super_admin` | `/admin/courses/{course_id}` | Delete course |
| GET | `/api/departments` | `super_admin` | `/admin/departments` | All departments |
| POST | `/api/departments` | `super_admin` | `/admin/departments` | Create department |
| PATCH | `/api/departments/{dept_id}` | `super_admin` | `/admin/departments/{dept_id}` | Update department |
| DELETE | `/api/departments/{dept_id}` | `super_admin` | `/admin/departments/{dept_id}` | Delete department |
| GET | `/api/timetable` | `super_admin` | `/admin/timetable` | Timetable (admin) |
| GET | `/api/timetable/conflicts` | `super_admin` | `/admin/timetable/conflicts` | Check conflicts |
| GET | `/api/stats` | `super_admin` | `/admin/academic/stats` | Academic stats |

### Admin Exams Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/exam/types` | `super_admin` | `/admin/exam/types` | Exam types |
| GET | `/api/exam/grading-scale` | `super_admin` | `/admin/exam/grading-scale` | Grading scale |
| GET | `/api/exam/results` | `super_admin` | `/admin/exam/results` | Exam results |
| POST | `/api/exam/results/publish` | `super_admin` | `/admin/exam/results/publish` | Publish results |
| POST | `/api/exam/results/unpublish` | `super_admin` | `/admin/exam/results/unpublish` | Unpublish results |
| GET | `/api/exam/notices` | `super_admin` | `/admin/exam/notices` | Exam notices |
| POST | `/api/exam/notices` | `super_admin` | `/admin/exam/notices` | Create exam notice |
| GET | `/api/exam/stats` | `super_admin` | `/admin/exam/stats` | Exam stats |
| GET | `/api/exam/report-card/{student_id}` | `super_admin` | `/admin/exam/report-card/{student_id}` | Report card |

### Admin Finance Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/finance/structures` | `super_admin` | `/admin/finance/structures` | Fee structures |
| POST | `/api/finance/structures` | `super_admin` | `/admin/finance/structures` | Create fee structure |
| PATCH | `/api/finance/structures/{structure_id}` | `super_admin` | `/admin/finance/structures/{structure_id}` | Update structure |
| GET | `/api/finance/records` | `super_admin` | `/admin/finance/records` | Fee records |
| POST | `/api/finance/records/pay` | `super_admin` | `/admin/finance/records/pay` | Record payment |
| POST | `/api/finance/records/refund` | `super_admin` | `/admin/finance/records/refund` | Refund payment |
| POST | `/api/finance/penalty/apply` | `super_admin` | `/admin/finance/penalty/apply` | Apply penalty |
| GET | `/api/finance/reports/summary` | `super_admin` | `/admin/finance/reports/summary` | Financial summary |
| GET | `/api/finance/reports/export` | `super_admin` | `/admin/finance/reports/export` | Export report |
| GET | `/api/finance/invoice/{record_id}` | `super_admin` | `/admin/finance/invoice/{record_id}` | Generate invoice |
| GET | `/api/finance/stats` | `super_admin` | `/admin/finance/stats` | Finance stats |

### Admin Notices Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/notices` | `super_admin` | `/admin/notices` | All notices |
| POST | `/api/notices` | `super_admin` | `/admin/notices` | Create notice |
| PATCH | `/api/notices/{notice_id}` | `super_admin` | `/admin/notices/{notice_id}` | Update notice |
| DELETE | `/api/notices/{notice_id}` | `super_admin` | `/admin/notices/{notice_id}` | Delete notice |
| POST | `/api/notices/{notice_id}/toggle` | `super_admin` | `/admin/notices/{notice_id}/toggle` | Toggle notice |
| POST | `/api/notices/{notice_id}/mark-emergency` | `super_admin` | `/admin/notices/{notice_id}/mark-emergency` | Mark emergency |
| GET | `/api/notices/stats` | `super_admin` | `/admin/notices/stats` | Notice stats |
| GET | `/api/notices/scheduled` | `super_admin` | `/admin/notices/scheduled` | Scheduled notices |

### Admin Messages Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/messages/all` | `super_admin` | `/admin/messages` | All messages |
| DELETE | `/api/messages/{message_id}` | `super_admin` | `/admin/messages/{message_id}` | Delete message |
| GET | `/api/messages/analytics` | `super_admin` | `/admin/messages/analytics` | Message analytics |

### Admin Media Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/media/files` | `super_admin` | `/admin/media/files` | All media files |
| POST | `/api/media/{file_id}/approve` | `super_admin` | `/admin/media/{file_id}/approve` | Approve file |
| DELETE | `/api/media/{file_id}` | `super_admin` | `/admin/media/{file_id}` | Delete file |
| GET | `/api/media/storage/usage` | `super_admin` | `/admin/media/storage/usage` | Storage usage |
| GET | `/api/media/storage/by-user` | `super_admin` | `/admin/media/storage/by-user` | Storage by user |
| GET | `/api/media/videos` | `super_admin` | `/admin/media/videos` | All videos |
| GET | `/api/media/notes` | `super_admin` | `/admin/media/notes` | All notes |

### Admin System Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/system/status` | `super_admin` | `/admin/system/status` | Server status |
| GET | `/api/system/database/health` | `super_admin` | `/admin/system/database/health` | Database health |
| GET | `/api/system/users/online` | `super_admin` | `/admin/system/users/online` | Active users |
| GET | `/api/system/performance` | `super_admin` | `/admin/system/performance` | Performance metrics |
| GET | `/api/system/backup/status` | `super_admin` | `/admin/system/backup/status` | Backup status |
| GET | `/api/system/security/status` | `super_admin` | `/admin/system/security/status` | Security status |
| GET | `/api/system/dashboard` | `super_admin` | `/admin/system/dashboard` | System dashboard |

### Admin Security Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/security/audit-logs` | `super_admin` | `/admin/security/audit-logs` | Audit logs |
| GET | `/api/security/audit-logs/{log_id}` | `super_admin` | `/admin/security/audit-logs/{log_id}` | Audit log detail |
| GET | `/api/security/settings` | `super_admin` | `/admin/security/settings` | Security settings |
| PATCH | `/api/security/settings` | `super_admin` | `/admin/security/settings` | Update settings |
| GET | `/api/security/jwt` | `super_admin` | `/admin/security/jwt` | JWT settings |
| PATCH | `/api/security/jwt` | `super_admin` | `/admin/security/jwt` | Update JWT |
| GET | `/api/security/ip-whitelist` | `super_admin` | `/admin/security/ip-whitelist` | IP whitelist |
| POST | `/api/security/ip-whitelist` | `super_admin` | `/admin/security/ip-whitelist` | Add IP |
| DELETE | `/api/security/ip-whitelist/{ip_id}` | `super_admin` | `/admin/security/ip-whitelist/{ip_id}` | Remove IP |
| GET | `/api/security/password-policy` | `super_admin` | `/admin/security/password-policy` | Password policy |
| PATCH | `/api/security/password-policy` | `super_admin` | `/admin/security/password-policy` | Update policy |
| GET | `/api/security/failed-logins` | `super_admin` | `/admin/security/failed-logins` | Failed logins |
| POST | `/api/security/unlock-account/{user_id}` | `super_admin` | `/admin/security/unlock-account/{user_id}` | Unlock account |
| GET | `/api/security/2fa/status` | `super_admin` | `/admin/security/2fa/status` | 2FA status |
| POST | `/api/security/2fa/enable` | `super_admin` | `/admin/security/2fa/enable` | Enable 2FA |
| POST | `/api/security/2fa/disable` | `super_admin` | `/admin/security/2fa/disable` | Disable 2FA |
| GET | `/api/security/sessions` | `super_admin` | `/admin/security/sessions` | Active sessions |
| DELETE | `/api/security/sessions/{session_id}` | `super_admin` | `/admin/security/sessions/{session_id}` | Invalidate session |
| DELETE | `/api/security/sessions/user/{user_id}` | `super_admin` | `/admin/security/sessions/user/{user_id}` | Force logout |
| GET | `/api/security/dashboard` | `super_admin` | `/admin/security/dashboard` | Security dashboard |

### Admin Backup Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| POST | `/api/backup/create` | `super_admin` | `/admin/backup/create` | Create backup |
| GET | `/api/backup/list` | `super_admin` | `/admin/backup/list` | List backups |
| GET | `/api/backup/{backup_id}/download` | `super_admin` | `/admin/backup/{backup_id}/download` | Download backup |
| POST | `/api/backup/{backup_id}/restore` | `super_admin` | `/admin/backup/{backup_id}/restore` | Restore backup |
| DELETE | `/api/backup/{backup_id}` | `super_admin` | `/admin/backup/{backup_id}` | Delete backup |
| GET | `/api/backup/schedule` | `super_admin` | `/admin/backup/schedule` | Get schedule |
| PATCH | `/api/backup/schedule` | `super_admin` | `/admin/backup/schedule` | Update schedule |
| GET | `/api/backup/status` | `super_admin` | `/admin/backup/status` | Backup status |
| POST | `/api/backup/export` | `super_admin` | `/admin/backup/export` | Export data |
| POST | `/api/backup/import` | `super_admin` | `/admin/backup/import` | Import data |

### Admin Reports Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/reports/attendance/students` | `super_admin` | `/admin/reports/attendance/students` | Student attendance |
| GET | `/api/reports/fees/due` | `super_admin` | `/admin/reports/fees/due` | Fee due report |
| GET | `/api/reports/teachers/performance` | `super_admin` | `/admin/reports/teachers/performance` | Teacher performance |
| GET | `/api/reports/exams/performance` | `super_admin` | `/admin/reports/exams/performance` | Exam performance |
| GET | `/api/reports/library/overdue` | `super_admin` | `/admin/reports/library/overdue` | Library overdue |
| GET | `/api/reports/finance/summary` | `super_admin` | `/admin/reports/finance/summary` | Financial report |
| GET | `/api/reports/export/csv` | `super_admin` | `/admin/reports/export/csv` | Export CSV |
| GET | `/api/reports/export/pdf` | `super_admin` | `/admin/reports/export/pdf` | Export PDF |
| GET | `/api/reports/comprehensive` | `super_admin` | `/admin/reports/comprehensive` | Comprehensive report |

### Admin Settings Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/settings/general` | `super_admin` | `/admin/settings/general` | General settings |
| PATCH | `/api/settings/general` | `super_admin` | `/admin/settings/general` | Update general |
| POST | `/api/settings/logo` | `super_admin` | `/admin/settings/logo` | Upload logo |
| GET | `/api/settings/academic` | `super_admin` | `/admin/settings/academic` | Academic settings |
| PATCH | `/api/settings/academic` | `super_admin` | `/admin/settings/academic` | Update academic |
| GET | `/api/settings/localization` | `super_admin` | `/admin/settings/localization` | Localization |
| PATCH | `/api/settings/localization` | `super_admin` | `/admin/settings/localization` | Update localization |
| GET | `/api/settings/smtp` | `super_admin` | `/admin/settings/smtp` | SMTP settings |
| PATCH | `/api/settings/smtp` | `super_admin` | `/admin/settings/smtp` | Update SMTP |
| POST | `/api/settings/smtp/test` | `super_admin` | `/admin/settings/smtp/test` | Test SMTP |
| GET | `/api/settings/payment` | `super_admin` | `/admin/settings/payment` | Payment settings |
| PATCH | `/api/settings/payment` | `super_admin` | `/admin/settings/payment` | Update payment |
| GET | `/api/settings/notifications` | `super_admin` | `/admin/settings/notifications` | Notification settings |
| PATCH | `/api/settings/notifications` | `super_admin` | `/admin/settings/notifications` | Update notifications |
| GET | `/api/settings/features` | `super_admin` | `/admin/settings/features` | Feature settings |
| PATCH | `/api/settings/features` | `super_admin` | `/admin/settings/features` | Update features |
| GET | `/api/settings/all` | `super_admin` | `/admin/settings/all` | All settings |

### Admin Advanced Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/ai/performance-prediction` | `super_admin` | `/admin/ai/performance-prediction` | Performance predictions |
| GET | `/api/ai/at-risk-students` | `super_admin` | `/admin/ai/at-risk-students` | At-risk students |
| GET | `/api/alerts/attendance` | `super_admin` | `/admin/alerts/attendance` | Attendance alerts |
| GET | `/api/alerts/fees` | `super_admin` | `/admin/alerts/fees` | Fee alerts |
| GET | `/api/alerts/performance` | `super_admin` | `/admin/alerts/performance` | Performance alerts |
| GET | `/api/notifications/automations` | `super_admin` | `/admin/notifications/automations` | Automations |
| POST | `/api/notifications/automations` | `super_admin` | `/admin/notifications/automations` | Create automation |
| PATCH | `/api/notifications/automations/{automation_id}` | `super_admin` | `/admin/notifications/automations/{automation_id}` | Update automation |
| POST | `/api/broadcast/sms` | `super_admin` | `/admin/broadcast/sms` | Send SMS |
| POST | `/api/broadcast/email` | `super_admin` | `/admin/broadcast/email` | Send email |
| GET | `/api/broadcast/history` | `super_admin` | `/admin/broadcast/history` | Broadcast history |
| GET | `/api/multi-school/schools` | `super_admin` | `/admin/multi-school/schools` | Schools |
| POST | `/api/multi-school/schools` | `super_admin` | `/admin/multi-school/schools` | Create school |
| GET | `/api/analytics/dashboard` | `super_admin` | `/admin/analytics/dashboard` | Advanced analytics |

### Admin Features Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/api/admin` | `super_admin` | `/admin/features` | All features |
| GET | `/api/admin/categories` | `super_admin` | `/admin/features/categories` | Feature categories |
| GET | `/api/admin/category/{category}` | `super_admin` | `/admin/features/category/{category}` | Features by category |
| POST | `/api/admin` | `super_admin` | `/admin/features` | Create feature |
| GET | `/api/admin/{feature_code}` | `super_admin` | `/admin/features/{feature_code}` | Get feature |
| PUT | `/api/admin/{feature_code}` | `super_admin` | `/admin/features/{feature_code}` | Update feature |
| DELETE | `/api/admin/{feature_code}` | `super_admin` | `/admin/features/{feature_code}` | Delete feature |
| POST | `/api/admin/{feature_code}/toggle` | `super_admin` | `/admin/features/{feature_code}/toggle` | Toggle feature |
| GET | `/api/admin/{feature_code}/permissions` | `super_admin` | `/admin/features/{feature_code}/permissions` | Feature permissions |
| PUT | `/api/admin/{feature_code}/permissions` | `super_admin` | `/admin/features/{feature_code}/permissions` | Update permissions |
| POST | `/api/admin/{feature_code}/permissions` | `super_admin` | `/admin/features/{feature_code}/permissions` | Batch update |
| GET | `/api/admin/audit-logs` | `super_admin` | `/admin/features/audit-logs` | Feature audit logs |
| GET | `/api/admin/audit-logs/feature/{feature_code}` | `super_admin` | `/admin/features/audit-logs/feature/{feature_code}` | Feature audit |

---

## Module Status Summary

| Module | Endpoints | Status | Priority |
|--------|-----------|--------|----------|
| `super_admin` | ~163 | ⚠️ Partial | High |

---

## Action Items

### super_admin
- [ ] Add dashboard endpoints
- [ ] Add user management (CRUD, role change, lock, reset password)
- [ ] Add academic management (courses, departments, timetable)
- [ ] Add exam management (types, grading, results, notices)
- [ ] Add finance management (structures, records, payments, penalties)
- [ ] Add notices management
- [ ] Add messages management
- [ ] Add media management
- [ ] Add system monitoring (status, database, performance)
- [ ] Add security management (audit logs, settings, IP whitelist, 2FA, sessions)
- [ ] Add backup management (create, restore, schedule)
- [ ] Add reports generation
- [ ] Add settings management (general, academic, SMTP, payment, notifications)
- [ ] Add advanced features (AI predictions, alerts, broadcasts, multi-school)
- [ ] Add feature management (toggle, permissions)
