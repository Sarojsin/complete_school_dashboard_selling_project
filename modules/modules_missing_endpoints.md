# Missing Endpoints - Comparison Report

This document lists endpoints that exist in the backup structure (`backup/backup_endpoint.md`) but are **missing** from the new modules structure (`modules/modules_endpoints.md`).

---

## Summary

| Category | Missing Endpoints Count |
|----------|------------------------|
| Notes Module | 8 |
| Tests Module | 12 |
| Chat Module | 12 |
| Groups Module | 17 |
| Grades Module | 7 |
| Admin Features | 8 |
| Admin Dashboard | 15 |
| Admin Users | 2 |
| Admin Academic | 14 |
| Admin Exams | 10 |
| Admin Finance | 12 |
| Admin Notices | 8 |
| Admin Messages | 4 |
| Admin Media | 8 |
| Admin System | 8 |
| Admin Security | 22 |
| Admin Backup | 12 |
| Admin Reports | 10 |
| Admin Settings | 6 |
| Admin Advanced | 15 |
| WebSocket | 1 |
| Web Routes | ~120+ |
| **Total** | **~320+** |

---

## Detailed Missing Endpoints

### 1. Notes Module

**Prefix:** `/api/notes`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/notes/upload` | Upload note | Missing |
| GET | `/api/notes/teacher/my-notes` | Get my notes | Missing |
| DELETE | `/api/notes/{note_id}` | Delete note | Missing |
| GET | `/api/notes/course/{course_id}` | Get course notes | Missing |
| GET | `/api/notes/{note_id}` | Get note | Missing |
| GET | `/api/notes/{note_id}/download` | Download note | Missing |
| GET | `/api/notes/search/{query}` | Search notes | Missing |
| GET | `/api/notes/recent/all` | Get recent notes | Missing |

---

### 2. Tests Module

**Prefix:** `/api/tests`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/tests/` | Create test | Missing |
| GET | `/api/tests/teacher/my-tests` | Get my tests | Missing |
| GET | `/api/tests/teacher/{test_id}` | Get test for teacher | Missing |
| PUT | `/api/tests/{test_id}` | Update test | Missing |
| DELETE | `/api/tests/{test_id}` | Delete test | Missing |
| GET | `/api/tests/{test_id}/results` | Get test results | Missing |
| GET | `/api/tests/student/available` | Get available tests | Missing |
| GET | `/api/tests/student/{test_id}` | Get test for student | Missing |
| POST | `/api/tests/{test_id}/start` | Start test | Missing |
| POST | `/api/tests/{test_id}/submit` | Submit test | Missing |
| GET | `/api/tests/student/{test_id}/result` | Get test result | Missing |
| GET | `/api/tests/student/my-results` | Get my results | Missing |

---

### 3. Chat Module

**Prefix:** `/api/chat`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/chat/conversations` | Get conversations | Missing |
| GET | `/api/chat/messages/{other_user_id}` | Get messages | Missing |
| POST | `/api/chat/messages/{receiver_id}` | Send message | Missing |
| POST | `/api/chat/mark-read/{sender_id}` | Mark messages read | Missing |
| GET | `/api/chat/unread-count` | Get unread count | Missing |
| GET | `/api/chat/online-users` | Get online users | Missing |
| GET | `/api/chat/search/{query}` | Search users | Missing |
| GET | `/api/chat/contacts/parent` | Get parent contacts | Missing |
| GET | `/api/chat/contacts/teacher` | Get teacher contacts | Missing |
| GET | `/api/chat/search-messages/{query}` | Search messages | Missing |

---

### 4. Groups Module

**Prefix:** `/api/groups`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/groups/` | List groups (HTML) | Missing |
| GET | `/api/groups/create` | Create group page (HTML) | Missing |
| POST | `/api/groups/create` | Create group | Missing |
| GET | `/api/groups/{group_id}` | Group detail (HTML) | Missing |
| GET | `/api/groups/{group_id}/edit` | Edit group page (HTML) | Missing |
| POST | `/api/groups/{group_id}/edit` | Update group | Missing |
| GET | `/api/groups/{group_id}/manage` | Manage members page (HTML) | Missing |
| POST | `/api/groups/{group_id}/members/add` | Add members | Missing |
| POST | `/api/groups/{group_id}/members/{user_id}/remove` | Remove member | Missing |
| GET | `/api/groups/api/{group_id}/members` | Get group members API | Missing |

#### Group Posts

**Prefix:** `/api/group-posts`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/group-posts/` | List posts (HTML) | Missing |
| GET | `/api/group-posts/create` | Create post page (HTML) | Missing |
| POST | `/api/group-posts/create` | Create post | Missing |
| GET | `/api/group-posts/{post_id}` | View post (HTML) | Missing |
| POST | `/api/group-posts/{post_id}/delete` | Delete post | Missing |
| GET | `/api/group-posts/api/posts` | Get posts API | Missing |

---

### 5. Grades Module

**Prefix:** `/api/grades`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/grades/` | Add grade | Missing |
| POST | `/api/grades/bulk` | Add bulk grades | Missing |
| PUT | `/api/grades/{grade_id}` | Update grade | Missing |
| DELETE | `/api/grades/{grade_id}` | Delete grade | Missing |
| GET | `/api/grades/course/{course_id}` | Get course grades | Missing |
| GET | `/api/grades/course/{course_id}/top-performers` | Get top performers | Missing |
| GET | `/api/grades/my-grades` | Get my grades | Missing |

---

### 6. Admin Features Module (Extended)

**Prefix:** `/api/admin`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/admin/categories` | Get feature categories | Missing |
| GET | `/api/admin/category/{category}` | Get features by category | Missing |
| POST | `/api/admin` | Create feature | Missing |
| POST | `/api/admin/{feature_code}/toggle` | Toggle feature | Missing |
| GET | `/api/admin/audit-logs/feature/{feature_code}` | Get feature audit logs | Missing |
| POST | `/api/admin/{feature_code}/permissions` | Batch update permissions | Missing |

---

### 7. Admin Dashboard

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/dashboard` | Get dashboard | Missing |
| GET | `/api/stats` | Get system stats | Missing |
| GET | `/api/users/count` | Get users by role | Missing |
| GET | `/api/overview` | Get dashboard overview | Missing |
| GET | `/api/features/summary` | Get features summary | Missing |
| GET | `/api/features/enabled` | Get enabled features | Missing |
| GET | `/api/features/disabled` | Get disabled features | Missing |
| GET | `/api/analytics/enrollment` | Get enrollment analytics | Missing |
| GET | `/api/analytics/fees` | Get fee analytics | Missing |
| GET | `/api/analytics/attendance` | Get attendance analytics | Missing |
| GET | `/api/analytics/exams` | Get exam analytics | Missing |
| GET | `/api/analytics/summary` | Get analytics summary | Missing |

---

### 8. Admin Users (Additional)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/users` | Get all users | Missing |
| GET | `/api/users/{user_id}` | Get user | Missing |

---

### 9. Admin Academic

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/courses` | Get all courses (admin) | Missing |
| POST | `/api/courses` | Create course (admin) | Missing |
| PATCH | `/api/courses/{course_id}` | Update course (admin) | Missing |
| DELETE | `/api/courses/{course_id}` | Delete course (admin) | Missing |
| GET | `/api/departments` | Get all departments (admin) | Missing |
| POST | `/api/departments` | Create department (admin) | Missing |
| PATCH | `/api/departments/{dept_id}` | Update department (admin) | Missing |
| DELETE | `/api/departments/{dept_id}` | Delete department (admin) | Missing |
| GET | `/api/timetable` | Get timetable (admin) | Missing |
| GET | `/api/timetable/conflicts` | Check timetable conflicts | Missing |
| GET | `/api/stats` | Get academic stats | Missing |

---

### 10. Admin Exams

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/exam/types` | Get exam types | Missing |
| GET | `/api/exam/grading-scale` | Get grading scale | Missing |
| GET | `/api/exam/results` | Get exam results | Missing |
| POST | `/api/exam/results/publish` | Publish results | Missing |
| POST | `/api/exam/results/unpublish` | Unpublish results | Missing |
| GET | `/api/exam/notices` | Get exam notices | Missing |
| POST | `/api/exam/notices` | Create exam notice | Missing |
| GET | `/api/exam/stats` | Get exam stats | Missing |
| GET | `/api/exam/report-card/{student_id}` | Generate report card | Missing |

---

### 11. Admin Finance

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/finance/structures` | Get fee structures | Missing |
| POST | `/api/finance/structures` | Create fee structure | Missing |
| PATCH | `/api/finance/structures/{structure_id}` | Update fee structure | Missing |
| GET | `/api/finance/records` | Get fee records | Missing |
| POST | `/api/finance/records/pay` | Record payment | Missing |
| POST | `/api/finance/records/refund` | Refund payment | Missing |
| POST | `/api/finance/penalty/apply` | Apply late penalty | Missing |
| GET | `/api/finance/reports/summary` | Get financial summary | Missing |
| GET | `/api/finance/reports/export` | Export financial report | Missing |
| GET | `/api/finance/invoice/{record_id}` | Generate invoice | Missing |
| GET | `/api/finance/stats` | Get finance stats | Missing |

---

### 12. Admin Notices (Extended)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/notices` | Get all notices | Missing |
| POST | `/api/notices` | Create notice | Missing |
| PATCH | `/api/notices/{notice_id}` | Update notice | Missing |
| DELETE | `/api/notices/{notice_id}` | Delete notice | Missing |
| POST | `/api/notices/{notice_id}/toggle` | Toggle notice | Missing |
| POST | `/api/notices/{notice_id}/mark-emergency` | Toggle emergency | Missing |
| GET | `/api/notices/stats` | Get notice stats | Missing |
| GET | `/api/notices/scheduled` | Get scheduled notices | Missing |

---

### 13. Admin Messages

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/messages/all` | Get all messages | Missing |
| DELETE | `/api/messages/{message_id}` | Delete message | Missing |
| GET | `/api/messages/analytics` | Get message analytics | Missing |

---

### 14. Admin Media

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/media/files` | Get all media files | Missing |
| POST | `/api/media/{file_id}/approve` | Approve media file | Missing |
| DELETE | `/api/media/{file_id}` | Delete media file | Missing |
| GET | `/api/media/storage/usage` | Get storage usage | Missing |
| GET | `/api/media/storage/by-user` | Get storage by user | Missing |
| GET | `/api/media/videos` | Get all videos | Missing |
| GET | `/api/media/notes` | Get all notes | Missing |

---

### 15. Admin System

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/system/status` | Get server status | Missing |
| GET | `/api/system/database/health` | Get database health | Missing |
| GET | `/api/system/users/online` | Get active users | Missing |
| GET | `/api/system/performance` | Get performance metrics | Missing |
| GET | `/api/system/backup/status` | Get backup status | Missing |
| GET | `/api/system/security/status` | Get security status | Missing |
| GET | `/api/system/dashboard` | Get system dashboard | Missing |

---

### 16. Admin Security (Extended)

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/security/audit-logs` | Get audit logs | Missing |
| GET | `/api/security/audit-logs/{log_id}` | Get audit log detail | Missing |
| GET | `/api/security/settings` | Get security settings | Missing |
| PATCH | `/api/security/settings` | Update security settings | Missing |
| GET | `/api/security/jwt` | Get JWT settings | Missing |
| PATCH | `/api/security/jwt` | Update JWT settings | Missing |
| GET | `/api/security/ip-whitelist` | Get IP whitelist | Missing |
| POST | `/api/security/ip-whitelist` | Add IP to whitelist | Missing |
| DELETE | `/api/security/ip-whitelist/{ip_id}` | Remove IP from whitelist | Missing |
| GET | `/api/security/password-policy` | Get password policy | Missing |
| PATCH | `/api/security/password-policy` | Update password policy | Missing |
| GET | `/api/security/failed-logins` | Get failed logins | Missing |
| POST | `/api/security/unlock-account/{user_id}` | Unlock user account | Missing |
| GET | `/api/security/2fa/status` | Get 2FA status | Missing |
| POST | `/api/security/2fa/enable` | Enable 2FA | Missing |
| POST | `/api/security/2fa/disable` | Disable 2FA | Missing |
| GET | `/api/security/sessions` | Get active sessions | Missing |
| DELETE | `/api/security/sessions/{session_id}` | Invalidate session | Missing |
| DELETE | `/api/security/sessions/user/{user_id}` | Force logout user | Missing |
| GET | `/api/security/dashboard` | Get security dashboard | Missing |

---

### 17. Admin Backup

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/backup/create` | Create backup | Missing |
| GET | `/api/backup/list` | List backups | Missing |
| GET | `/api/backup/{backup_id}/download` | Download backup | Missing |
| POST | `/api/backup/{backup_id}/restore` | Restore backup | Missing |
| DELETE | `/api/backup/{backup_id}` | Delete backup | Missing |
| GET | `/api/backup/schedule` | Get backup schedule | Missing |
| PATCH | `/api/backup/schedule` | Update backup schedule | Missing |
| GET | `/api/backup/status` | Get backup status | Missing |
| POST | `/api/backup/export` | Export data | Missing |
| POST | `/api/backup/import` | Import data | Missing |

---

### 18. Admin Reports

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/reports/attendance/students` | Get student attendance report | Missing |
| GET | `/api/reports/fees/due` | Get fee due report | Missing |
| GET | `/api/reports/teachers/performance` | Get teacher performance report | Missing |
| GET | `/api/reports/exams/performance` | Get exam performance report | Missing |
| GET | `/api/reports/library/overdue` | Get library overdue report | Missing |
| GET | `/api/reports/finance/summary` | Get financial report | Missing |
| GET | `/api/reports/export/csv` | Export report CSV | Missing |
| GET | `/api/reports/export/pdf` | Export report PDF | Missing |
| GET | `/api/reports/comprehensive` | Get comprehensive report | Missing |

---

### 19. Admin Settings (Additional)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/settings/logo` | Upload school logo | Missing |
| GET | `/api/settings/all` | Get all settings | Missing |

---

### 20. Admin Advanced

**Prefix:** `/api`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/ai/performance-prediction` | Get performance predictions | Missing |
| GET | `/api/ai/at-risk-students` | Get at-risk students | Missing |
| GET | `/api/alerts/attendance` | Get attendance alerts | Missing |
| GET | `/api/alerts/fees` | Get fee alerts | Missing |
| GET | `/api/alerts/performance` | Get performance alerts | Missing |
| GET | `/api/notifications/automations` | Get notification automations | Missing |
| POST | `/api/notifications/automations` | Create notification automation | Missing |
| PATCH | `/api/notifications/automations/{automation_id}` | Update notification automation | Missing |
| POST | `/api/broadcast/sms` | Send SMS broadcast | Missing |
| POST | `/api/broadcast/email` | Send email broadcast | Missing |
| GET | `/api/broadcast/history` | Get broadcast history | Missing |
| GET | `/api/multi-school/schools` | Get schools | Missing |
| POST | `/api/multi-school/schools` | Create school | Missing |
| GET | `/api/analytics/dashboard` | Get advanced analytics | Missing |

---

### 21. WebSocket Chat

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| WS | `/api/ws/chat` | WebSocket chat endpoint | Missing |

---

### 22. Web Routes (HTML Pages)

All web routes from backup/web are missing:
- Common routes (login, signup pages)
- Student web routes
- Teacher web routes
- Authority web routes
- Parent web routes
- Admin web routes
- Library web routes
- And many more...

---

## Endpoints NOW IMPLEMENTED (Moved to modules)

The following endpoints from backup are now implemented in the new modules structure:

### Authentication ✓
- All auth endpoints now in `modules/auth/router.py`

### School Modules ✓
- Authority endpoints now in `modules/school/school_authority/router.py`
- Teacher endpoints now in `modules/school/school_teacher/router.py`
- Student endpoints now in `modules/school/school_student/router.py`
- Parent endpoints now in `modules/school/school_parent/router.py`
- Exam endpoints now in `modules/school/school_exam_section/router.py`
- Library endpoints now in `modules/school/school_library/router.py`
- Notices endpoints now in `modules/school/school_notices/api.py`
- Courses endpoints now in `modules/school/school_courses/api.py`
- Attendance endpoints now in `modules/school/school_attendance/api.py`
- Account endpoints now in `modules/school/school_account_section/router.py`
- Assignments endpoints now in `modules/school/school_assignments/api.py`
- Timetable endpoints now in `modules/school/school_timetable/api.py`
- Videos endpoints now in `modules/school/school_videos/api.py`

### College Modules ✓
- Courses endpoints now in `modules/college/college_courses/router.py`
- Faculty endpoints now in `modules/college/college_faculty/router.py`
- Hostel endpoints now in `modules/college/college_hostel/router.py`
- Lab endpoints now in `modules/college/college_lab/router.py`
- Placement endpoints now in `modules/college/college_placement/router.py`
- Research endpoints now in `modules/college/college_research/router.py`
- Student endpoints now in `modules/college/college_student/router.py`
- Dean endpoints now in `modules/college/college_dean/api.py`
- Exam Section endpoints now in `modules/college/college_exam_section/api.py`
- HOD endpoints now in `modules/college/college_hod/api.py`
- Registrar endpoints now in `modules/college/college_registrar/api.py`
- Account endpoints now in `modules/college/college_account_section/api.py`

### Super Admin ✓
- All admin endpoints now in `modules/super_admin/api.py`

---

## Recommendations

To fully migrate from backup to modules, the following modules need to be created:

1. **Notes Module** - Create `modules/school/school_notes/`
2. **Tests Module** - Create `modules/school/school_tests/`
3. **Chat Module** - Create `modules/school/school_chat/`
4. **Groups Module** - Create `modules/school/school_groups/`
5. **Grades Module** - Create `modules/school/school_grades/`
6. **Admin Dashboard** - Extend `modules/super_admin/`
7. **WebSocket** - Create `modules/websocket/`
8. **Web Routes** - Create HTML template-based routes

---

*Last Updated: 2026-03-29*
*Generated from comparison of backup_endpoint.md and modules_endpoints.md*
