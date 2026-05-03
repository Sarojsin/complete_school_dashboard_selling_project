# Duplicate Endpoints Analysis - backup_endpoint.md

This document identifies duplicate and repeated endpoints found in the backup structure (`backup/backup_endpoint.md`).

---

## Summary

| Category | Unique Endpoints | Duplicate Occurrences | Total References |
|----------|-----------------|---------------------|------------------|
| Authentication | 14 | 15 | 29 |
| Students | 15 | 30+ | 45+ |
| Teachers | 12 | 20+ | 32+ |
| Authority | 17 | 20+ | 37+ |
| Parents | 7 | 10+ | 17+ |
| Courses | 7 | 10+ | 17+ |
| Notices | 11 | 15+ | 26+ |
| Library | 4 | 10+ | 14+ |
| Admin | 150+ | 50+ | 200+ |
| **TOTAL** | **~237** | **~170** | **~407** |

---

## Detailed Duplicate Endpoints

### 1. Authentication Endpoints

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| POST | `/api/auth/login` | auth.py, api/v1/college/auth.py | 2 |
| POST | `/api/auth/login-json` | auth.py, api/v1/college/auth.py | 2 |
| POST | `/api/auth/refresh` | auth.py | 1 |
| POST | `/api/auth/signup/student` | auth.py, api/v1/school/students.py | 2 |
| POST | `/api/auth/signup/teacher` | auth.py | 1 |
| POST | `/api/auth/signup/admin` | auth.py | 1 |
| POST | `/api/auth/signup/authority` | auth.py | 1 |
| POST | `/api/auth/signup/parent` | auth.py | 1 |
| POST | `/api/auth/signup/hod` | auth.py | 1 |
| POST | `/api/auth/signup/exam-section` | auth.py | 1 |
| POST | `/api/auth/signup/library` | auth.py | 1 |
| POST | `/api/auth/signup/account` | auth.py | 1 |
| POST | `/api/auth/logout` | auth.py | 1 |

---

### 2. Student Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/students/me` | students.py, v1/school/students.py, v1/college/students.py | 3 |
| PUT | `/api/students/me` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/dashboard` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/courses` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/courses/{course_id}` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/assignments` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/grades` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/attendance` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/fees` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/tests` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/notices` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/timetable` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/notes` | students.py, v1/school/students.py | 2 |
| GET | `/api/students/videos` | students.py, v1/school/students.py | 2 |

---

### 3. Teacher Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/teachers/me` | teachers.py, v1/school/teachers.py | 2 |
| PUT | `/api/teachers/me` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/dashboard` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/courses` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/students` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/students/{student_id}` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/assignments` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/attendance` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/grades` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/tests` | teachers.py, v1/school/teachers.py | 2 |
| GET | `/api/teachers/timetable` | teachers.py, v1/school/teachers.py | 2 |

---

### 4. Authority Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/authority/dashboard` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/students` | authority.py, v1/school/authorities.py | 2 |
| POST | `/api/authority/students` | authority.py, v1/school/authorities.py | 2 |
| PUT | `/api/authority/students/{student_id}` | authority.py, v1/school/authorities.py | 2 |
| DELETE | `/api/authority/students/{student_id}` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/teachers` | authority.py, v1/school/authorities.py | 2 |
| POST | `/api/authority/teachers` | authority.py, v1/school/authorities.py | 2 |
| PUT | `/api/authority/teachers/{teacher_id}` | authority.py, v1/school/authorities.py | 2 |
| DELETE | `/api/authority/teachers/{teacher_id}` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/analytics/students` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/analytics/attendance` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/analytics/performance` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/courses` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/fees` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/notices` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/analytics` | authority.py, v1/school/authorities.py | 2 |
| GET | `/api/authority/reports` | authority.py, v1/school/authorities.py | 2 |

---

### 5. Parent Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/parents/dashboard` | parents.py, v1/school/parents.py | 2 |
| GET | `/api/parents/child/{student_id}/attendance` | parents.py, v1/school/parents.py | 2 |
| GET | `/api/parents/child/{student_id}/grades` | parents.py, v1/school/parents.py | 2 |
| GET | `/api/parents/child/{student_id}/homework` | parents.py, v1/school/parents.py | 2 |
| GET | `/api/parents/notices` | parents.py, v1/school/parents.py | 2 |
| GET | `/api/parents/chat` | parents.py, v1/school/parents.py | 2 |

---

### 6. Courses Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/courses/` | courses.py, admin_academic.py, v1/college/courses.py | 3 |
| GET | `/api/courses/{course_id}` | courses.py, admin_academic.py, v1/college/courses.py | 3 |
| POST | `/api/courses/` | courses.py, admin_academic.py | 2 |
| PUT | `/api/courses/{course_id}` | courses.py, admin_academic.py | 2 |
| DELETE | `/api/courses/{course_id}` | courses.py, admin_academic.py | 2 |
| GET | `/api/courses/{course_id}/students` | courses.py | 1 |
| GET | `/api/courses/search/{query}` | courses.py | 1 |

---

### 7. Notices Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| POST | `/api/notices/` | notices.py, admin_notices.py | 2 |
| PUT | `/api/notices/{notice_id}` | notices.py, admin_notices.py | 2 |
| DELETE | `/api/notices/{notice_id}` | notices.py, admin_notices.py | 2 |
| GET | `/api/notices/` | notices.py, admin_notices.py | 2 |
| GET | `/api/notices/urgent` | notices.py | 1 |
| GET | `/api/notices/recent` | notices.py | 1 |
| GET | `/api/notices/{notice_id}` | notices.py, admin_notices.py | 2 |
| GET | `/api/notices/search/{query}` | notices.py | 1 |
| POST | `/api/notices/{notice_id}/upload` | notices.py | 1 |

---

### 8. Library Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| POST | `/library/loans` | library.py, v1/college/hostels.py (similar) | 2 |
| POST | `/library/loans/{loan_id}/return` | library.py | 1 |
| GET | `/library/loans/student/{student_id}` | library.py | 1 |

---

### 9. Admin Endpoints (HIGHLY DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/dashboard` | admin_dashboard.py | 1 |
| GET | `/api/stats` | admin_dashboard.py, admin_academic.py | 2 |
| GET | `/api/users` | admin_users.py | 1 |
| GET | `/api/users/{user_id}` | admin_users.py | 1 |
| GET | `/api/courses` | admin_academic.py, v1/college/courses.py | 2 |
| POST | `/api/courses` | admin_academic.py, v1/college/courses.py | 2 |
| GET | `/api/departments` | admin_academic.py, v1/college/departments.py | 2 |
| POST | `/api/departments` | admin_academic.py | 1 |
| GET | `/api/exam/types` | admin_exams.py | 1 |
| GET | `/api/exam/results` | admin_exams.py | 1 |
| GET | `/api/finance/structures` | admin_finance.py | 1 |
| POST | `/api/finance/structures` | admin_finance.py | 1 |
| GET | `/api/finance/records` | admin_finance.py | 1 |
| GET | `/api/notices` | admin_notices.py, notices.py | 2 |
| POST | `/api/notices` | admin_notices.py, notices.py | 2 |
| GET | `/api/security/audit-logs` | admin_security.py | 1 |
| GET | `/api/settings/general` | admin_settings.py | 1 |
| PATCH | `/api/settings/general` | admin_settings.py | 1 |
| GET | `/api/backup/list` | admin_backup.py | 1 |
| POST | `/api/backup/create` | admin_backup.py | 1 |
| GET | `/api/reports/attendance/students` | admin_reports.py | 1 |

---

### 10. College Endpoints (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/api/v1/college/students/me` | v1/college/students.py | 1 |
| GET | `/api/v1/college/students/` | v1/college/students.py | 1 |
| GET | `/api/v1/college/faculty/me` | v1/college/faculty.py | 1 |
| GET | `/api/v1/college/faculty/` | v1/college/faculty.py | 1 |
| GET | `/api/v1/college/departments` | v1/college/departments.py | 1 |
| GET | `/api/v1/college/courses` | v1/college/courses.py | 1 |
| GET | `/api/v1/college/enrollments` | v1/college/enrollments.py | 1 |
| GET | `/api/v1/college/hostels` | v1/college/hostels.py | 1 |
| GET | `/api/v1/college/labs` | v1/college/labs.py | 1 |
| GET | `/api/v1/college/placements/companies` | v1/college/placements.py | 1 |
| GET | `/api/v1/college/research/projects` | v1/college/research.py | 1 |

---

### 11. HOD & Exam Section (DUPLICATED)

| Method | Endpoint | Appears In | Count |
|--------|----------|------------|-------|
| GET | `/hod/dashboard` | hod.py | 1 |
| GET | `/exam-section/results` | exam_section.py, exam_section.py (web) | 2 |
| POST | `/exam-section/results` | exam_section.py | 1 |

---

## Duplicate Analysis by Source File

### Files with Most Duplicates

| Source File | Endpoints | Duplicate With |
|-------------|-----------|----------------|
| backup/api/endpoints/students.py | 15 | v1/school/students.py |
| backup/api/endpoints/teachers.py | 12 | v1/school/teachers.py |
| backup/api/endpoints/authority.py | 17 | v1/school/authorities.py |
| backup/api/endpoints/parents.py | 7 | v1/school/parents.py |
| backup/api/endpoints/courses.py | 7 | admin_academic.py |
| backup/api/endpoints/notices.py | 11 | admin_notices.py |
| backup/api/v1/school/* | 50+ | backup/api/endpoints/* |

---

## Recommendations

### 1. Consolidate Authentication
- Keep one authentication module
- Remove duplicates from v1/college/auth.py

### 2. Unify Student/Teacher Routes
- Consolidate `students.py`, `teachers.py` with v1 versions
- Keep one source of truth for each role

### 3. Merge Authority Routes
- Combine `authority.py` with `v1/school/authorities.py`
- Use consistent naming convention

### 4. Admin Endpoint Cleanup
- Many admin endpoints overlap
- Consider using query parameters for filtering

### 5. College API Consolidation
- The v1/college endpoints duplicate v1/school patterns
- Consider a single college API structure

---

## Files with Duplicate Content

| Original File | Duplicate File |
|---------------|---------------|
| backup/api/endpoints/students.py | backup/api/v1/school/students.py |
| backup/api/endpoints/teachers.py | backup/api/v1/school/teachers.py |
| backup/api/endpoints/authority.py | backup/api/v1/school/authorities.py |
| backup/api/endpoints/parents.py | backup/api/v1/school/parents.py |
| backup/api/endpoints/courses.py | backup/api/v1/college/courses.py |
| backup/api/endpoints/notices.py | backup/api/endpoints/admin_notices.py |
| backup/api/endpoints/library.py | backup/api/v1/college/hostels.py |

---

*Analysis completed: 2026-03-26*