## backup_all_endpoints.md
# Backup Endpoints Documentation

This document contains all endpoints from the backup directory, including duplicates.

---

## Table of Contents
1. [backup/api - API Endpoints](#backupapi---api-endpoints)
2. [backup/web - Web Routes](#backupweb---web-routes)
3. [backup/websocket - WebSocket Endpoints](#backupwebsocket---websocket-endpoints)

---

## backup/api - API Endpoints

### 1. Authentication (backup/api/endpoints/auth.py)
**Prefix:** `/api/auth`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/login-json` | JSON login response |
| POST | `/api/auth/refresh` | Refresh token |
| POST | `/api/auth/signup/student` | Student signup |
| POST | `/api/auth/signup/teacher` | Teacher signup |
| POST | `/api/auth/signup/admin` | Admin signup |
| POST | `/api/auth/signup/authority` | Authority signup |
| POST | `/api/auth/signup/parent` | Parent signup |
| POST | `/api/auth/signup/hod` | HOD signup |
| POST | `/api/auth/signup/exam-section` | Exam section signup |
| POST | `/api/auth/signup/library` | Library signup |
| POST | `/api/auth/signup/account` | Account signup |
| POST | `/api/auth/logout` | User logout |

---

### 2. Students (backup/api/endpoints/students.py)
**Prefix:** `/api/students`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/me` | Get current student profile |
| PUT | `/api/students/me` | Update current student profile |
| GET | `/api/students/dashboard` | Get student dashboard |
| GET | `/api/students/courses` | Get student courses |
| GET | `/api/students/courses/{course_id}` | Get course details |
| GET | `/api/students/assignments` | Get student assignments |
| GET | `/api/students/grades` | Get student grades |
| GET | `/api/students/attendance` | Get student attendance |
| GET | `/api/students/fees` | Get student fees |
| GET | `/api/students/tests` | Get available tests |
| GET | `/api/students/notices` | Get student notices |
| GET | `/api/students/timetable` | Get student timetable |
| GET | `/api/students/notes` | Get student notes |
| GET | `/api/students/videos` | Get student videos |

---

### 3. Teachers (backup/api/endpoints/teachers.py)
**Prefix:** `/api/teachers`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teachers/me` | Get current teacher profile |
| PUT | `/api/teachers/me` | Update current teacher profile |
| GET | `/api/teachers/dashboard` | Get teacher dashboard |
| GET | `/api/teachers/courses` | Get teacher courses |
| GET | `/api/teachers/students` | Get teacher students |
| GET | `/api/teachers/students/{student_id}` | Get student detail |
| GET | `/api/teachers/assignments` | Get teacher assignments |
| GET | `/api/teachers/attendance` | Get teacher attendance |
| GET | `/api/teachers/grades` | Get teacher grades |
| GET | `/api/teachers/tests` | Get teacher tests |
| GET | `/api/teachers/timetable` | Get teacher timetable |

---

### 4. Authority (backup/api/endpoints/authority.py)
**Prefix:** `/api/authority`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/authority/dashboard` | Get authority dashboard |
| GET | `/api/authority/students` | Get all students |
| POST | `/api/authority/students` | Create student |
| PUT | `/api/authority/students/{student_id}` | Update student |
| DELETE | `/api/authority/students/{student_id}` | Delete student |
| GET | `/api/authority/teachers` | Get all teachers |
| POST | `/api/authority/teachers` | Create teacher |
| PUT | `/api/authority/teachers/{teacher_id}` | Update teacher |
| DELETE | `/api/authority/teachers/{teacher_id}` | Delete teacher |
| GET | `/api/authority/analytics/students` | Get student analytics |
| GET | `/api/authority/analytics/attendance` | Get attendance analytics |
| GET | `/api/authority/analytics/performance` | Get performance analytics |
| GET | `/api/authority/courses` | Get all courses |
| GET | `/api/authority/fees` | Get all fees |
| GET | `/api/authority/notices` | Get all notices |
| GET | `/api/authority/analytics` | Get analytics |
| GET | `/api/authority/reports` | Get reports |

---

### 5. Parents (backup/api/endpoints/parents.py)
**Prefix:** `/api/parents`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/parents/dashboard` | Parent dashboard (HTML) |
| GET | `/api/parents/profile` | Parent profile (HTML) |
| GET | `/api/parents/child/{student_id}/attendance` | Child attendance (HTML) |
| GET | `/api/parents/child/{student_id}/grades` | Child grades (HTML) |
| GET | `/api/parents/child/{student_id}/homework` | Child homework (HTML) |
| GET | `/api/parents/notices` | Parent notices (HTML) |
| GET | `/api/parents/chat` | Parent chat (HTML) |

---

### 6. Courses (backup/api/endpoints/courses.py)
**Prefix:** `/api/courses`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | Get all courses |
| GET | `/api/courses/{course_id}` | Get course |
| POST | `/api/courses/` | Create course |
| PUT | `/api/courses/{course_id}` | Update course |
| DELETE | `/api/courses/{course_id}` | Delete course |
| GET | `/api/courses/{course_id}/students` | Get course students |
| GET | `/api/courses/search/{query}` | Search courses |

---

### 7. Assignments (backup/api/endpoints/assignments.py)
**Prefix:** `/api/assignments`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/assignments/` | Create assignment |
| POST | `/api/assignments/{assignment_id}/upload` | Upload assignment file |
| GET | `/api/assignments/teacher/my-assignments` | Get my assignments |
| GET | `/api/assignments/{assignment_id}/submissions` | Get assignment submissions |
| PUT | `/api/assignments/submissions/{submission_id}/grade` | Grade submission |
| PUT | `/api/assignments/{assignment_id}` | Update assignment |
| DELETE | `/api/assignments/{assignment_id}` | Delete assignment |
| GET | `/api/assignments/{assignment_id}` | Get assignment |
| POST | `/api/assignments/{assignment_id}/submit` | Submit assignment |
| GET | `/api/assignments/{assignment_id}/my-submission` | Get my submission |

---

### 8. Attendance (backup/api/endpoints/attendance.py)
**Prefix:** `/api/attendance`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attendance/` | Mark attendance |
| POST | `/api/attendance/bulk` | Mark bulk attendance |
| GET | `/api/attendance/course/{course_id}` | Get course attendance |
| GET | `/api/attendance/course/{course_id}/stats` | Get course attendance stats |
| GET | `/api/attendance/my-attendance` | Get my attendance |
| GET | `/api/attendance/my-attendance/course/{course_id}` | Get my course attendance |

---

### 9. Grades (backup/api/endpoints/grades.py)
**Prefix:** `/api/grades`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/grades/` | Add grade |
| POST | `/api/grades/bulk` | Add bulk grades |
| PUT | `/api/grades/{grade_id}` | Update grade |
| DELETE | `/api/grades/{grade_id}` | Delete grade |
| GET | `/api/grades/course/{course_id}` | Get course grades |
| GET | `/api/grades/course/{course_id}/top-performers` | Get top performers |
| GET | `/api/grades/my-grades` | Get my grades |

---

### 10. Fees (backup/api/endpoints/fees.py)
**Prefix:** `/api/fees`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/fees/` | Create fee record |
| POST | `/api/fees/bulk` | Create bulk fees |
| PUT | `/api/fees/{fee_id}` | Update fee record |
| POST | `/api/fees/{fee_id}/payment` | Record payment |
| DELETE | `/api/fees/{fee_id}` | Delete fee record |
| GET | `/api/fees/summary` | Get all fees summary |
| GET | `/api/fees/overdue` | Get all overdue fees |
| GET | `/api/fees/student/{student_id}` | Get student fees |
| GET | `/api/fees/type/{fee_type}` | Get fees by type |
| GET | `/api/fees/my-fees` | Get my fees |
| GET | `/api/fees/my-fees/pending` | Get my pending fees |
| GET | `/api/fees/my-fees/overdue` | Get my overdue fees |
| GET | `/api/fees/my-fees/payment-history` | Get my payment history |

---

### 11. Notices (backup/api/endpoints/notices.py)
**Prefix:** `/api/notices`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/notices/` | Create notice |
| POST | `/api/notices/{notice_id}/upload` | Upload notice file |
| PUT | `/api/notices/{notice_id}` | Update notice |
| DELETE | `/api/notices/{notice_id}` | Delete notice |
| GET | `/api/notices/all` | Get all notices (admin) |
| GET | `/api/notices/` | Get notices |
| GET | `/api/notices/urgent` | Get urgent notices |
| GET | `/api/notices/recent` | Get recent notices |
| GET | `/api/notices/{notice_id}` | Get notice |
| GET | `/api/notices/search/{query}` | Search notices |

---

### 12. Notes (backup/api/endpoints/notes.py)
**Prefix:** `/api/notes`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/notes/upload` | Upload note |
| GET | `/api/notes/teacher/my-notes` | Get my notes |
| DELETE | `/api/notes/{note_id}` | Delete note |
| GET | `/api/notes/course/{course_id}` | Get course notes |
| GET | `/api/notes/{note_id}` | Get note |
| GET | `/api/notes/{note_id}/download` | Download note |
| GET | `/api/notes/search/{query}` | Search notes |
| GET | `/api/notes/recent/all` | Get recent notes |

---

### 13. Videos (backup/api/endpoints/videos.py)
**Prefix:** `/api/videos`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/videos/upload` | Upload video |
| GET | `/api/videos/teacher/my-videos` | Get my videos |
| GET | `/api/videos/{video_id}` | Get video |
| DELETE | `/api/videos/{video_id}` | Delete video |
| GET | `/api/videos/course/{course_id}` | Get course videos |
| GET | `/api/videos/{video_id}/stream` | Stream video |
| GET | `/api/videos/search/{query}` | Search videos |
| GET | `/api/videos/recent/all` | Get recent videos |

---

### 14. Tests (backup/api/endpoints/tests.py)
**Prefix:** `/api/tests`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tests/` | Create test |
| GET | `/api/tests/teacher/my-tests` | Get my tests |
| GET | `/api/tests/teacher/{test_id}` | Get test for teacher |
| PUT | `/api/tests/{test_id}` | Update test |
| DELETE | `/api/tests/{test_id}` | Delete test |
| GET | `/api/tests/{test_id}/results` | Get test results |
| GET | `/api/tests/student/available` | Get available tests |
| GET | `/api/tests/student/{test_id}` | Get test for student |
| POST | `/api/tests/{test_id}/start` | Start test |
| POST | `/api/tests/{test_id}/submit` | Submit test |
| GET | `/api/tests/student/{test_id}/result` | Get test result |
| GET | `/api/tests/student/my-results` | Get my results |

---

### 15. Chat (backup/api/endpoints/chat.py)
**Prefix:** `/api/chat`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/conversations` | Get conversations |
| GET | `/api/chat/messages/{other_user_id}` | Get messages |
| POST | `/api/chat/messages/{receiver_id}` | Send message |
| POST | `/api/chat/mark-read/{sender_id}` | Mark messages read |
| GET | `/api/chat/unread-count` | Get unread count |
| GET | `/api/chat/online-users` | Get online users |
| GET | `/api/chat/search/{query}` | Search users |
| GET | `/api/chat/contacts/parent` | Get parent contacts |
| GET | `/api/chat/contacts/teacher` | Get teacher contacts |
| GET | `/api/chat/search-messages/{query}` | Search messages |

---

### 16. Groups (backup/api/endpoints/groups.py)
**Prefix:** `/api/groups`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/groups/` | List groups (HTML) |
| GET | `/api/groups/create` | Create group page (HTML) |
| POST | `/api/groups/create` | Create group |
| GET | `/api/groups/{group_id}` | Group detail (HTML) |
| GET | `/api/groups/{group_id}/edit` | Edit group page (HTML) |
| POST | `/api/groups/{group_id}/edit` | Update group |
| GET | `/api/groups/{group_id}/manage` | Manage members page (HTML) |
| POST | `/api/groups/{group_id}/members/add` | Add members |
| POST | `/api/groups/{group_id}/members/{user_id}/remove` | Remove member |
| GET | `/api/groups/api/{group_id}/members` | Get group members API |

---

### 17. Group Posts (backup/api/endpoints/group_posts.py)
**Prefix:** `/api/group-posts`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/group-posts/` | List posts (HTML) |
| GET | `/api/group-posts/create` | Create post page (HTML) |
| POST | `/api/group-posts/create` | Create post |
| GET | `/api/group-posts/{post_id}` | View post (HTML) |
| POST | `/api/group-posts/{post_id}/delete` | Delete post |
| GET | `/api/group-posts/api/posts` | Get posts API |

---

### 18. HOD (backup/api/endpoints/hod.py)
**Prefix:** (No prefix - included directly)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/hod/dashboard` | Get HOD dashboard |
| GET | `/hod/departments` | Get all departments |

---

### 19. Exam Section (backup/api/endpoints/exam_section.py)
**Prefix:** (No prefix - included directly)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/exam-section/results` | Publish exam result |
| GET | `/exam-section/results` | Get all results |
| GET | `/exam-section/results/student/{student_id}` | Get student results |

---

### 20. Library (backup/api/endpoints/library.py)
**Prefix:** (No prefix - included directly)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/library/loans` | Issue book |
| POST | `/library/loans/{loan_id}/return` | Return book |
| GET | `/library/loans` | Get all loans |
| GET | `/library/loans/student/{student_id}` | Get student loans |

---

### 21. Account (backup/api/endpoints/account.py)
**Prefix:** (No prefix - included directly)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/account/payments` | Record teacher payment |
| GET | `/account/payments` | Get all payments |
| GET | `/account/payments/teacher/{teacher_id}` | Get teacher payments |
| GET | `/account/stats` | Get account stats |

---

### 22. Admin Features (backup/api/endpoints/admin_features.py)
**Prefix:** `/api/admin`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin` | Get all features |
| GET | `/api/admin/categories` | Get feature categories |
| GET | `/api/admin/category/{category}` | Get features by category |
| POST | `/api/admin` | Create feature |
| GET | `/api/admin/{feature_code}` | Get feature |
| PUT | `/api/admin/{feature_code}` | Update feature |
| DELETE | `/api/admin/{feature_code}` | Delete feature |
| POST | `/api/admin/{feature_code}/toggle` | Toggle feature |
| GET | `/api/admin/{feature_code}/permissions` | Get feature permissions |
| PUT | `/api/admin/{feature_code}/permissions` | Update role permissions |
| POST | `/api/admin/{feature_code}/permissions` | Batch update permissions |
| GET | `/api/admin/audit-logs` | Get audit logs |
| GET | `/api/admin/audit-logs/feature/{feature_code}` | Get feature audit logs |

---

### 23. Admin Dashboard (backup/api/endpoints/admin_dashboard.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Get dashboard |
| GET | `/api/stats` | Get system stats |
| GET | `/api/users/count` | Get users by role |
| GET | `/api/overview` | Get dashboard overview |
| GET | `/api/features/summary` | Get features summary |
| GET | `/api/features/enabled` | Get enabled features |
| GET | `/api/features/disabled` | Get disabled features |
| GET | `/api/analytics/enrollment` | Get enrollment analytics |
| GET | `/api/analytics/fees` | Get fee analytics |
| GET | `/api/analytics/attendance` | Get attendance analytics |
| GET | `/api/analytics/exams` | Get exam analytics |
| GET | `/api/analytics/summary` | Get analytics summary |

---

### 24. Admin Users (backup/api/endpoints/admin_users.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| GET | `/api/users/{user_id}` | Get user |
| PATCH | `/api/users/{user_id}/toggle-active` | Toggle user active |
| POST | `/api/users/{user_id}/reset-password` | Reset user password |
| POST | `/api/users/{user_id}/lock` | Lock user account |
| POST | `/api/users/{user_id}/force-logout` | Force logout user |
| GET | `/api/users/{user_id}/login-history` | Get user login history |
| POST | `/api/users/{user_id}/change-role` | Change user role |
| GET | `/api/users/stats/by-role` | Get user stats by role |
| GET | `/api/users/students/list` | Get students list |
| GET | `/api/users/teachers/list` | Get teachers list |
| GET | `/api/users/parents/list` | Get parents list |

---

### 25. Admin Academic (backup/api/endpoints/admin_academic.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses` | Get all courses (admin) |
| POST | `/api/courses` | Create course (admin) |
| PATCH | `/api/courses/{course_id}` | Update course (admin) |
| DELETE | `/api/courses/{course_id}` | Delete course (admin) |
| GET | `/api/departments` | Get all departments (admin) |
| POST | `/api/departments` | Create department (admin) |
| PATCH | `/api/departments/{dept_id}` | Update department (admin) |
| DELETE | `/api/departments/{dept_id}` | Delete department (admin) |
| GET | `/api/timetable` | Get timetable (admin) |
| GET | `/api/timetable/conflicts` | Check timetable conflicts |
| GET | `/api/stats` | Get academic stats |

---

### 26. Admin Exams (backup/api/endpoints/admin_exams.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exam/types` | Get exam types |
| GET | `/api/exam/grading-scale` | Get grading scale |
| GET | `/api/exam/results` | Get exam results |
| POST | `/api/exam/results/publish` | Publish results |
| POST | `/api/exam/results/unpublish` | Unpublish results |
| GET | `/api/exam/notices` | Get exam notices |
| POST | `/api/exam/notices` | Create exam notice |
| GET | `/api/exam/stats` | Get exam stats |
| GET | `/api/exam/report-card/{student_id}` | Generate report card |

---

### 27. Admin Finance (backup/api/endpoints/admin_finance.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/finance/structures` | Get fee structures |
| POST | `/api/finance/structures` | Create fee structure |
| PATCH | `/api/finance/structures/{structure_id}` | Update fee structure |
| GET | `/api/finance/records` | Get fee records |
| POST | `/api/finance/records/pay` | Record payment |
| POST | `/api/finance/records/refund` | Refund payment |
| POST | `/api/finance/penalty/apply` | Apply late penalty |
| GET | `/api/finance/reports/summary` | Get financial summary |
| GET | `/api/finance/reports/export` | Export financial report |
| GET | `/api/finance/invoice/{record_id}` | Generate invoice |
| GET | `/api/finance/stats` | Get finance stats |

---

### 28. Admin Notices (backup/api/endpoints/admin_notices.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notices` | Get all notices |
| POST | `/api/notices` | Create notice |
| PATCH | `/api/notices/{notice_id}` | Update notice |
| DELETE | `/api/notices/{notice_id}` | Delete notice |
| POST | `/api/notices/{notice_id}/toggle` | Toggle notice |
| POST | `/api/notices/{notice_id}/mark-emergency` | Toggle emergency |
| GET | `/api/notices/stats` | Get notice stats |
| GET | `/api/notices/scheduled` | Get scheduled notices |

---

### 29. Admin Messages (backup/api/endpoints/admin_messages.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages/all` | Get all messages |
| DELETE | `/api/messages/{message_id}` | Delete message |
| GET | `/api/messages/analytics` | Get message analytics |

---

### 30. Admin Media (backup/api/endpoints/admin_media.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/media/files` | Get all media files |
| POST | `/api/media/{file_id}/approve` | Approve media file |
| DELETE | `/api/media/{file_id}` | Delete media file |
| GET | `/api/media/storage/usage` | Get storage usage |
| GET | `/api/media/storage/by-user` | Get storage by user |
| GET | `/api/media/videos` | Get all videos |
| GET | `/api/media/notes` | Get all notes |

---

### 31. Admin System (backup/api/endpoints/admin_system.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/system/status` | Get server status |
| GET | `/api/system/database/health` | Get database health |
| GET | `/api/system/users/online` | Get active users |
| GET | `/api/system/performance` | Get performance metrics |
| GET | `/api/system/backup/status` | Get backup status |
| GET | `/api/system/security/status` | Get security status |
| GET | `/api/system/dashboard` | Get system dashboard |

---

### 32. Admin Security (backup/api/endpoints/admin_security.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/security/audit-logs` | Get audit logs |
| GET | `/api/security/audit-logs/{log_id}` | Get audit log detail |
| GET | `/api/security/settings` | Get security settings |
| PATCH | `/api/security/settings` | Update security settings |
| GET | `/api/security/jwt` | Get JWT settings |
| PATCH | `/api/security/jwt` | Update JWT settings |
| GET | `/api/security/ip-whitelist` | Get IP whitelist |
| POST | `/api/security/ip-whitelist` | Add IP to whitelist |
| DELETE | `/api/security/ip-whitelist/{ip_id}` | Remove IP from whitelist |
| GET | `/api/security/password-policy` | Get password policy |
| PATCH | `/api/security/password-policy` | Update password policy |
| GET | `/api/security/failed-logins` | Get failed logins |
| POST | `/api/security/unlock-account/{user_id}` | Unlock user account |
| GET | `/api/security/2fa/status` | Get 2FA status |
| POST | `/api/security/2fa/enable` | Enable 2FA |
| POST | `/api/security/2fa/disable` | Disable 2FA |
| GET | `/api/security/sessions` | Get active sessions |
| DELETE | `/api/security/sessions/{session_id}` | Invalidate session |
| DELETE | `/api/security/sessions/user/{user_id}` | Force logout user |
| GET | `/api/security/dashboard` | Get security dashboard |

---

### 33. Admin Backup (backup/api/endpoints/admin_backup.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/backup/create` | Create backup |
| GET | `/api/backup/list` | List backups |
| GET | `/api/backup/{backup_id}/download` | Download backup |
| POST | `/api/backup/{backup_id}/restore` | Restore backup |
| DELETE | `/api/backup/{backup_id}` | Delete backup |
| GET | `/api/backup/schedule` | Get backup schedule |
| PATCH | `/api/backup/schedule` | Update backup schedule |
| GET | `/api/backup/status` | Get backup status |
| POST | `/api/backup/export` | Export data |
| POST | `/api/backup/import` | Import data |

---

### 34. Admin Reports (backup/api/endpoints/admin_reports.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/attendance/students` | Get student attendance report |
| GET | `/api/reports/fees/due` | Get fee due report |
| GET | `/api/reports/teachers/performance` | Get teacher performance report |
| GET | `/api/reports/exams/performance` | Get exam performance report |
| GET | `/api/reports/library/overdue` | Get library overdue report |
| GET | `/api/reports/finance/summary` | Get financial report |
| GET | `/api/reports/export/csv` | Export report CSV |
| GET | `/api/reports/export/pdf` | Export report PDF |
| GET | `/api/reports/comprehensive` | Get comprehensive report |

---

### 35. Admin Settings (backup/api/endpoints/admin_settings.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/settings/general` | Get general settings |
| PATCH | `/api/settings/general` | Update general settings |
| POST | `/api/settings/logo` | Upload school logo |
| GET | `/api/settings/academic` | Get academic settings |
| PATCH | `/api/settings/academic` | Update academic settings |
| GET | `/api/settings/localization` | Get localization settings |
| PATCH | `/api/settings/localization` | Update localization settings |
| GET | `/api/settings/smtp` | Get SMTP settings |
| PATCH | `/api/settings/smtp` | Update SMTP settings |
| POST | `/api/settings/smtp/test` | Test SMTP settings |
| GET | `/api/settings/payment` | Get payment settings |
| PATCH | `/api/settings/payment` | Update payment settings |
| GET | `/api/settings/notifications` | Get notification settings |
| PATCH | `/api/settings/notifications` | Update notification settings |
| GET | `/api/settings/features` | Get feature settings |
| PATCH | `/api/settings/features` | Update feature settings |
| GET | `/api/settings/all` | Get all settings |

---

### 36. Admin Advanced (backup/api/endpoints/admin_advanced.py)
**Prefix:** `/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ai/performance-prediction` | Get performance predictions |
| GET | `/api/ai/at-risk-students` | Get at-risk students |
| GET | `/api/alerts/attendance` | Get attendance alerts |
| GET | `/api/alerts/fees` | Get fee alerts |
| GET | `/api/alerts/performance` | Get performance alerts |
| GET | `/api/notifications/automations` | Get notification automations |
| POST | `/api/notifications/automations` | Create notification automation |
| PATCH | `/api/notifications/automations/{automation_id}` | Update notification automation |
| POST | `/api/broadcast/sms` | Send SMS broadcast |
| POST | `/api/broadcast/email` | Send email broadcast |
| GET | `/api/broadcast/history` | Get broadcast history |
| GET | `/api/multi-school/schools` | Get schools |
| POST | `/api/multi-school/schools` | Create school |
| GET | `/api/analytics/dashboard` | Get advanced analytics |

---

### 37. WebSocket Chat (backup/api/endpoints/websocket_chat.py)
**Prefix:** (WebSocket)

| Method | Endpoint | Description |
|--------|----------|-------------|
| WS | `/api/ws/chat` | WebSocket chat endpoint |

---

### 38. API v1 - School (backup/api/v1/school/*)

#### School Authorities (backup/api/v1/school/authorities.py)
**Prefix:** `/api/v1/school`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/school/dashboard` | Get dashboard |
| GET | `/api/v1/school/students` | Get all students |
| POST | `/api/v1/school/students` | Create student |
| PUT | `/api/v1/school/students/{student_id}` | Update student |
| DELETE | `/api/v1/school/students/{student_id}` | Delete student |
| GET | `/api/v1/school/teachers` | Get all teachers |
| POST | `/api/v1/school/teachers` | Create teacher |
| PUT | `/api/v1/school/teachers/{teacher_id}` | Update teacher |
| DELETE | `/api/v1/school/teachers/{teacher_id}` | Delete teacher |
| GET | `/api/v1/school/analytics/students` | Get student analytics |
| GET | `/api/v1/school/analytics/attendance` | Get attendance analytics |
| GET | `/api/v1/school/analytics/performance` | Get performance analytics |
| GET | `/api/v1/school/courses` | Get all courses |
| GET | `/api/v1/school/fees` | Get all fees |
| GET | `/api/v1/school/notices` | Get all notices |
| GET | `/api/v1/school/analytics` | Get analytics |
| GET | `/api/v1/school/reports` | Get reports |

#### School Students (backup/api/v1/school/students.py)
**Prefix:** `/api/v1/school`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/school/students/me` | Get my profile |
| PUT | `/api/v1/school/students/me` | Update my profile |
| GET | `/api/v1/school/students/dashboard` | Get dashboard |
| GET | `/api/v1/school/students/courses` | Get my courses |
| GET | `/api/v1/school/students/courses/{course_id}` | Get course details |
| GET | `/api/v1/school/students/assignments` | Get my assignments |
| GET | `/api/v1/school/students/grades` | Get my grades |
| GET | `/api/v1/school/students/attendance` | Get my attendance |
| GET | `/api/v1/school/students/fees` | Get my fees |
| GET | `/api/v1/school/students/tests` | Get available tests |
| GET | `/api/v1/school/students/notices` | Get my notices |
| GET | `/api/v1/school/students/timetable` | Get my timetable |
| GET | `/api/v1/school/students/notes` | Get my notes |
| GET | `/api/v1/school/students/videos` | Get my videos |

#### School Teachers (backup/api/v1/school/teachers.py)
**Prefix:** `/api/v1/school`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/school/teachers/me` | Get my profile |
| PUT | `/api/v1/school/teachers/me` | Update my profile |
| GET | `/api/v1/school/teachers/dashboard` | Get dashboard |
| GET | `/api/v1/school/teachers/courses` | Get my courses |
| GET | `/api/v1/school/teachers/students` | Get my students |
| GET | `/api/v1/school/teachers/students/{student_id}` | Get student detail |
| GET | `/api/v1/school/teachers/assignments` | Get my assignments |
| GET | `/api/v1/school/teachers/attendance` | Get my attendance |
| GET | `/api/v1/school/teachers/grades` | Get my grades |
| GET | `/api/v1/school/teachers/tests` | Get my tests |
| GET | `/api/v1/school/teachers/timetable` | Get my timetable |

#### School Parents (backup/api/v1/school/parents.py)
**Prefix:** `/api/v1/school`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/school/parents/dashboard` | Parent dashboard (HTML) |
| GET | `/api/v1/school/parents/profile` | Parent profile (HTML) |
| GET | `/api/v1/school/parents/child/{student_id}/attendance` | Child attendance (HTML) |
| GET | `/api/v1/school/parents/child/{student_id}/grades` | Child grades (HTML) |
| GET | `/api/v1/school/parents/child/{student_id}/homework` | Child homework (HTML) |
| GET | `/api/v1/school/parents/notices` | Parent notices (HTML) |
| GET | `/api/v1/school/parents/chat` | Parent chat (HTML) |

---

### 39. API v1 - College (backup/api/v1/college/*)

#### College Students (backup/api/v1/college/students.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/students/me` | Get my profile |
| PUT | `/api/v1/college/students/me` | Update my profile |
| GET | `/api/v1/college/students/` | List students |
| GET | `/api/v1/college/students/{student_id}` | Get student |
| POST | `/api/v1/college/students/` | Create student |
| DELETE | `/api/v1/college/students/{student_id}` | Delete student |

#### College Faculty (backup/api/v1/college/faculty.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/faculty/me` | Get my profile |
| PUT | `/api/v1/college/faculty/me` | Update my profile |
| GET | `/api/v1/college/faculty/` | List faculty |
| GET | `/api/v1/college/faculty/{faculty_id}` | Get faculty |
| POST | `/api/v1/college/faculty/` | Create faculty |
| DELETE | `/api/v1/college/faculty/{faculty_id}` | Delete faculty |

#### College Departments (backup/api/v1/college/departments.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/departments` | Get departments |
| GET | `/api/v1/college/departments/{department_id}` | Get department |
| POST | `/api/v1/college/departments` | Create department |
| PATCH | `/api/v1/college/departments/{department_id}` | Update department |
| DELETE | `/api/v1/college/departments/{department_id}` | Delete department |

#### College Courses (backup/api/v1/college/courses.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/courses` | Get courses |
| GET | `/api/v1/college/courses/{course_id}` | Get course |
| POST | `/api/v1/college/courses` | Create course |
| PATCH | `/api/v1/college/courses/{course_id}` | Update course |
| DELETE | `/api/v1/college/courses/{course_id}` | Delete course |

#### College Enrollments (backup/api/v1/college/enrollments.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/enrollments` | Get enrollments |
| GET | `/api/v1/college/enrollments/{enrollment_id}` | Get enrollment |
| POST | `/api/v1/college/enrollments` | Enroll student |
| PATCH | `/api/v1/college/enrollments/{enrollment_id}` | Update enrollment |
| DELETE | `/api/v1/college/enrollments/{enrollment_id}` | Drop course |

#### College Hostels (backup/api/v1/college/hostels.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/hostels` | List hostels |
| GET | `/api/v1/college/hostels/{hostel_id}` | Get hostel |
| POST | `/api/v1/college/hostels` | Create hostel |
| GET | `/api/v1/college/hostels/{hostel_id}/rooms` | List rooms |
| POST | `/api/v1/college/hostels/{hostel_id}/rooms` | Create room |
| POST | `/api/v1/college/hostels/allocate` | Allocate room |
| GET | `/api/v1/college/hostels/student/{student_id}/allocation` | Get student allocation |
| POST | `/api/v1/college/hostels/vacate` | Vacate room |
| GET | `/api/v1/college/hostels/complaints` | List complaints |
| POST | `/api/v1/college/hostels/complaints` | Create complaint |
| PUT | `/api/v1/college/hostels/complaints/{complaint_id}/resolve` | Resolve complaint |

#### College Labs (backup/api/v1/college/labs.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/labs` | List labs |
| GET | `/api/v1/college/labs/{lab_id}` | Get lab |
| POST | `/api/v1/college/labs` | Create lab |
| GET | `/api/v1/college/labs/{lab_id}/equipment` | List equipment |
| POST | `/api/v1/college/labs/{lab_id}/equipment` | Add equipment |
| PUT | `/api/v1/college/labs/equipment/{equipment_id}` | Update equipment |
| GET | `/api/v1/college/labs/{lab_id}/schedules` | List schedules |
| POST | `/api/v1/college/labs/{lab_id}/schedules` | Create schedule |

#### College Placements (backup/api/v1/college/placements.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/placements/companies` | List companies |
| GET | `/api/v1/college/placements/companies/{company_id}` | Get company |
| POST | `/api/v1/college/placements/companies` | Create company |
| GET | `/api/v1/college/placements/jobs` | List jobs |
| GET | `/api/v1/college/placements/jobs/{job_id}` | Get job |
| POST | `/api/v1/college/placements/jobs` | Create job |
| POST | `/api/v1/college/placements/apply` | Apply for job |
| GET | `/api/v1/college/placements/applications/student/{student_id}` | Get student applications |
| GET | `/api/v1/college/placements/applications/job/{job_id}` | Get job applications |
| PUT | `/api/v1/college/placements/applications/{application_id}/status` | Update application status |

#### College Research (backup/api/v1/college/research.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/research/projects` | List projects |
| GET | `/api/v1/college/research/projects/{project_id}` | Get project |
| POST | `/api/v1/college/research/projects` | Create project |
| GET | `/api/v1/college/research/publications` | List publications |
| GET | `/api/v1/college/research/publications/{publication_id}` | Get publication |
| POST | `/api/v1/college/research/publications` | Create publication |
| GET | `/api/v1/college/research/patents` | List patents |

#### College Programs (backup/api/v1/college/programs.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/programs/` | List programs |
| GET | `/api/v1/college/programs/{program_id}` | Get program |

#### College Semesters (backup/api/v1/college/semesters.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/semesters/` | List semesters |
| GET | `/api/v1/college/semesters/{semester_id}` | Get semester |

#### College Auth (backup/api/v1/college/auth.py)
**Prefix:** `/api/v1/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/college/auth/students` | List students |

---

## backup/web - Web Routes

### 1. Common Routes (backup/web/routers/common.py)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page (HTML) |
| GET | `/logout` | Logout |
| GET | `/login` | Login page (HTML) |
| GET | `/signup` | Signup page (HTML) |
| GET | `/signup/student` | Student signup page (HTML) |
| GET | `/signup/teacher` | Teacher signup page (HTML) |
| GET | `/signup/authority` | Authority signup page (HTML) |
| GET | `/signup/parent` | Parent signup page (HTML) |
| GET | `/signup/hod` | HOD signup page (HTML) |
| GET | `/signup/exam-section` | Exam section signup page (HTML) |
| GET | `/signup/library` | Library signup page (HTML) |
| GET | `/signup/account` | Account signup page (HTML) |
| GET | `/signup/admin` | Admin signup page (HTML) |
| POST | `/signup/admin` | Admin signup handler |
| GET | `/register` | Register page (HTML) |
| GET | `/register/student` | Register student page (HTML) |
| GET | `/register/teacher` | Register teacher page (HTML) |
| GET | `/register/parent` | Register parent page (HTML) |

---

### 2. Student Web Routes (backup/web/routers/student.py)
**Prefix:** `/student`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/student/dashboard` | Student dashboard |
| GET | `/student/profile` | Student profile |
| POST | `/student/profile` | Update student profile |
| GET | `/student/courses` | Student courses |
| GET | `/student/assignments` | Student assignments |
| GET | `/student/fees` | Student fees |
| GET | `/student/assignments/{assignment_id}` | Assignment detail |
| POST | `/student/assignments/{assignment_id}/submit` | Submit assignment |
| GET | `/student/tests` | Test list |
| GET | `/student/tests/{test_id}/start` | Take test |
| POST | `/student/tests/{test_id}/submit` | Submit test |
| GET | `/student/tests/{test_id}/result` | Test result |
| GET | `/student/notices` | Student notices |
| GET | `/student/timetable` | Student timetable |
| GET | `/student/notes` | Student notes |
| GET | `/student/videos` | Student videos |
| GET | `/student/forum` | Student forum |
| GET | `/student/messages` | Student messages |
| POST | `/student/messages/{message_id}/read` | Mark message read |
| GET | `/student/teachers` | Student teachers |
| POST | `/student/teachers/{teacher_id}/contact` | Contact teacher |
| GET | `/student/groups` | Student groups |
| GET | `/student/grades` | Student grades |
| GET | `/student/attendance` | Student attendance |
| POST | `/student/mark-video-watched/{video_id}` | Mark video watched |
| GET | `/student/groups/{group_id}` | Group detail |
| POST | `/student/groups/join` | Join group |
| GET | `/student/groups/{group_id}/posts` | Group posts |
| GET | `/student/groups/{group_id}/posts/{post_id}` | View post |
| GET | `/student/exam-results` | Exam results |
| GET | `/student/library` | Student library |

---

### 3. Teacher Web Routes (backup/web/routers/teacher.py)
**Prefix:** `/teacher`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/teacher/dashboard` | Teacher dashboard |
| GET | `/teacher/profile` | Teacher profile |
| POST | `/teacher/profile` | Update teacher profile |
| GET | `/teacher/students` | Teacher students |
| GET | `/teacher/students/{student_id}` | Student detail |
| GET | `/teacher/students/{student_id}/grades` | Student grades |
| POST | `/teacher/students/{student_id}/contact` | Contact student |
| GET | `/teacher/messages` | Teacher messages |
| POST | `/teacher/messages/{message_id}/read` | Mark message read |
| GET | `/teacher/assignments` | Teacher assignments |
| GET | `/teacher/assignments/{id}/edit` | Edit assignment |
| POST | `/teacher/assignments/{id}/edit` | Edit assignment post |
| GET | `/teacher/assignments/create` | Create assignment |
| POST | `/teacher/assignments/create` | Create assignment post |
| GET | `/teacher/assignments/{id}/submissions` | View submissions |
| POST | `/teacher/assignments/submissions/{submission_id}/grade` | Grade submission |
| DELETE | `/teacher/assignments/delete/{id}` | Delete assignment |
| GET | `/teacher/notes/upload` | Upload notes |
| POST | `/teacher/notes/upload` | Upload notes post |
| GET | `/teacher/courses/{id}` | Course detail |
| GET | `/teacher/courses/{id}/students` | Course students |
| GET | `/teacher/attendance/take` | Take attendance |
| POST | `/teacher/attendance/save` | Save attendance |
| GET | `/teacher/attendance` | Attendance list |
| GET | `/teacher/attendance/view/{id}` | View attendance |
| GET | `/teacher/grades` | Teacher grades |
| GET | `/teacher/grades/add` | Add grades |
| POST | `/teacher/grades/add` | Add grades post |
| GET | `/teacher/attendance/{id}/edit` | Edit attendance |
| GET | `/teacher/tests` | Teacher tests |
| GET | `/teacher/tests/create` | Create test |
| GET | `/teacher/tests/{id}/results` | Test results |
| GET | `/teacher/tests/{id}/edit` | Edit test |
| POST | `/teacher/tests/create` | Create test post |
| DELETE | `/teacher/tests/delete/{id}` | Delete test |
| GET | `/teacher/videos/upload` | Upload videos |
| POST | `/teacher/videos/upload` | Upload videos post |
| GET | `/teacher/courses` | Teacher courses |
| GET | `/teacher/notices/create` | Create notice |
| POST | `/teacher/notices/create` | Create notice post |
| GET | `/teacher/groups` | Teacher groups |
| GET | `/teacher/groups/{group_id}` | Group detail |
| GET | `/teacher/groups/{group_id}/posts/create` | Create post form |
| POST | `/teacher/groups/{group_id}/posts/create` | Create post |
| GET | `/teacher/groups/{group_id}/edit` | Edit group form |
| POST | `/teacher/groups/{group_id}/edit` | Edit group |
| GET | `/teacher/groups/{group_id}/posts` | Group posts |
| GET | `/teacher/groups/{group_id}/posts/{post_id}` | View post |
| POST | `/teacher/groups/{group_id}/posts/{post_id}/delete` | Delete post |
| GET | `/teacher/chat` | Teacher chat |
| GET | `/teacher/timetable` | Teacher timetable |
| POST | `/teacher/timetable` | Timetable post |

---

### 4. Parent Web Routes (backup/web/routers/parent.py)
**Prefix:** `/parent`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/parent/dashboard` | Parent dashboard |
| GET | `/parent/child/{id}/attendance` | Child attendance |
| GET | `/parent/child/{id}/grades` | Child grades |
| GET | `/parent/child/{id}/homework` | Child homework |
| GET | `/parent/chat` | Parent chat |
| GET | `/parent/notices` | Parent notices |
| GET | `/parent/profile` | Parent profile |

---

### 5. Authority Web Routes (backup/web/routers/authority.py)
**Prefix:** `/authority`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authority/dashboard` | Authority dashboard |
| GET | `/authority/students` | Authority students |
| GET | `/authority/teachers` | Authority teachers |
| GET | `/authority/courses` | Authority courses |
| GET | `/authority/fees` | Authority fees |
| GET | `/authority/notices` | Authority notices |
| GET | `/authority/analytics` | Authority analytics |
| GET | `/authority/students/add` | Add student form |
| POST | `/authority/students/add` | Add student |
| GET | `/authority/students/{id}` | Student detail |
| GET | `/authority/students/{id}/edit` | Edit student form |
| POST | `/authority/students/{id}/edit` | Edit student |
| POST | `/authority/students/{id}/delete` | Delete student |
| GET | `/authority/teachers/add` | Add teacher form |
| POST | `/authority/teachers/add` | Add teacher |
| GET | `/authority/teachers/{id}` | Teacher detail |
| GET | `/authority/teachers/{id}/edit` | Edit teacher form |
| POST | `/authority/teachers/{id}/edit` | Edit teacher |
| POST | `/authority/teachers/{id}/delete` | Delete teacher |
| GET | `/authority/courses/add` | Add course form |
| POST | `/authority/courses/add` | Add course |
| GET | `/authority/courses/{id}` | Course detail |
| POST | `/authority/courses/{id}/enroll` | Enroll student |
| POST | `/authority/courses/{id}/unenroll` | Unenroll student |
| GET | `/authority/courses/{id}/edit` | Edit course form |
| POST | `/authority/courses/{id}/edit` | Edit course |
| POST | `/authority/courses/{id}/delete` | Delete course |
| GET | `/authority/notices/create` | Create notice form |
| POST | `/authority/notices/create` | Create notice |
| GET | `/authority/notices/{id}` | View notice |
| GET | `/authority/notices/{id}/edit` | Edit notice form |
| POST | `/authority/notices/{id}/edit` | Edit notice |
| GET | `/authority/fees/add` | Add fee form |
| POST | `/authority/fees/add` | Add fee |
| GET | `/authority/fees/structure` | Fee structure |
| GET | `/authority/groups` | Authority groups |
| GET | `/authority/groups/create` | Create group form |
| POST | `/authority/groups/create` | Create group |
| GET | `/authority/groups/{group_id}/manage` | Manage group |
| POST | `/authority/groups/{group_id}/delete` | Delete group |
| POST | `/authority/groups/{group_id}/add-member` | Add group member |
| POST | `/authority/groups/{group_id}/remove-member` | Remove group member |
| GET | `/authority/groups/{group_id}/posts` | Group posts |
| GET | `/authority/groups/{group_id}/posts/create` | Create post form |
| POST | `/authority/groups/{group_id}/posts/create` | Create post |
| GET | `/authority/groups/{group_id}/posts/{post_id}` | View post |
| POST | `/authority/groups/{group_id}/posts/{post_id}/delete` | Delete post |
| GET | `/authority/reports` | Authority reports |
| GET | `/authority/departments` | Authority departments |
| POST | `/authority/departments/add` | Add department |
| POST | `/authority/departments/{id}/edit` | Edit department |
| POST | `/authority/departments/{id}/delete` | Delete department |

---

### 6. Authority CRUD (backup/web/authority_crud.py)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authority/students/add` | Add student form |
| POST | `/authority/students/add` | Add student |
| GET | `/authority/students/{id}` | Student detail |
| GET | `/authority/students/{id}/edit` | Edit student form |
| POST | `/authority/students/{id}/edit` | Edit student |
| POST | `/authority/students/{id}/delete` | Delete student |
| GET | `/authority/teachers/add` | Add teacher form |
| POST | `/authority/teachers/add` | Add teacher |
| GET | `/authority/teachers/{id}` | Teacher detail |
| GET | `/authority/teachers/{id}/edit` | Edit teacher form |
| POST | `/authority/teachers/{id}/edit` | Edit teacher |
| POST | `/authority/teachers/{id}/delete` | Delete teacher |
| GET | `/authority/courses/add` | Add course form |
| POST | `/authority/courses/add` | Add course |
| GET | `/authority/courses/{id}` | Course detail |
| GET | `/authority/courses/{id}/edit` | Edit course form |
| POST | `/authority/courses/{id}/edit` | Edit course |
| GET | `/authority/notices/create` | Create notice form |
| POST | `/authority/notices/create` | Create notice |
| GET | `/authority/notices/{id}` | View notice |
| GET | `/authority/notices/{id}/edit` | Edit notice form |
| POST | `/authority/notices/{id}/edit` | Edit notice |

---

### 7. Admin Web Routes (backup/web/routers/admin.py)
**Prefix:** `/admin`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Admin dashboard |
| GET | `/admin/features` | Admin features |
| GET | `/admin/features/{feature_code}` | Feature detail |
| GET | `/admin/audit` | Audit logs |
| GET | `/admin/settings` | Admin settings |
| GET | `/admin/users` | Admin users |
| GET | `/admin/academic` | Admin academic |
| GET | `/admin/finance` | Admin finance |
| GET | `/admin/system` | Admin system |
| GET | `/admin/security` | Admin security |
| GET | `/admin/backup` | Admin backup |
| GET | `/admin/reports` | Admin reports |
| GET | `/admin/notices` | Admin notices |
| GET | `/admin/communication` | Admin communication |
| GET | `/admin/media` | Admin media |
| GET | `/admin/advanced` | Admin advanced |

---

### 8. HOD Web Routes (backup/web/routers/hod.py)
**Prefix:** `/hod`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/hod/dashboard` | HOD dashboard |
| GET | `/hod/teachers` | HOD teachers |
| GET | `/hod/students` | HOD students |
| GET | `/hod/students/{student_id}/performance` | Student performance |
| GET | `/hod/reports` | HOD reports |
| GET | `/hod/profile` | HOD profile |

---

### 9. Exam Section Web Routes (backup/web/routers/exam_section.py)
**Prefix:** `/exam-section`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exam-section/dashboard` | Exam dashboard |
| GET | `/exam-section/post-result` | Post result page |
| POST | `/exam-section/post-result` | Post result action |
| GET | `/exam-section/results` | All results |
| GET | `/exam-section/grade-sheet/{student_id}` | Grade sheet |
| GET | `/exam-section/notices` | Exam notices |
| GET | `/exam-section/notices/create` | Create notice page |
| POST | `/exam-section/notices/create` | Create notice action |
| GET | `/exam-section/profile` | Exam profile |

---

### 10. Library Web Routes (backup/web/routers/library.py)
**Prefix:** `/library`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/library/dashboard` | Library dashboard |
| GET | `/library/issue-book` | Issue book page |
| POST | `/library/issue-book` | Issue book action |
| GET | `/library/return-book` | Return book page |
| POST | `/library/return-book/{loan_id}` | Return book action |
| GET | `/library/overdue` | Overdue books |
| GET | `/library/history/{student_id}` | Student history |
| GET | `/library/books` | Book catalog |
| GET | `/library/books/add` | Add book page |
| POST | `/library/books/add` | Add book action |
| GET | `/library/profile` | Library profile |

---

### 11. Account Web Routes (backup/web/routers/account.py)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/account/dashboard` | Account dashboard |
| GET | `/account/record-payment` | Record payment page |
| POST | `/account/record-payment` | Record payment action |
| GET | `/account/fees` | Fees list |
| GET | `/account/fees/record` | Record fee page |
| POST | `/account/fees/record` | Record fee action |
| GET | `/account/payments` | Payments history |
| GET | `/account/reports` | Financial reports |
| GET | `/account/profile` | Account profile |

---

### 12. Groups Web Routes (backup/web/routers/groups.py)
**Prefix:** `/groups`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/groups` | Groups list |
| GET | `/groups/create` | Create group redirect |
| GET | `/groups/{group_id}` | Group detail |
| GET | `/groups/{group_id}/posts/create` | Create post form |
| GET | `/groups/{group_id}/posts` | Group posts redirect |
| GET | `/groups/{group_id}/edit` | Edit group redirect |

---

### 13. Group Posts Web Routes (backup/web/routers/group_posts.py)
**Prefix:** (inherits from groups)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/group-posts/` | List posts (HTML) |
| GET | `/group-posts/create` | Create post page (HTML) |
| POST | `/group-posts/create` | Create post |
| GET | `/group-posts/{post_id}` | View post (HTML) |
| POST | `/group-posts/{post_id}/delete` | Delete post |
| GET | `/group-posts/api/posts` | Get posts API |

---

## backup/websocket - WebSocket Endpoints

### 1. WebSocket Router (backup/websocket/router.py)

| Method | Endpoint | Description |
|--------|----------|-------------|
| WS | `/ws/chat` | WebSocket chat endpoint |

---

## Summary

| Category | Total Endpoints |
|----------|-----------------|
| backup/api | ~300+ endpoints |
| backup/web | ~200+ endpoints |
| backup/websocket | 1 endpoint |
| **Total** | **~500+ endpoints** |

---

*This document was generated automatically from the backup directory source files.*
