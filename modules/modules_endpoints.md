# New Structure Modules Endpoints

This document contains all API endpoints from the new modular structure (modules directory).

---

## Table of Contents
1. [Authentication Module](#authentication-module)
2. [Super Admin Module](#super-admin-module)
3. [School Modules](#school-modules)
4. [College Modules](#college-modules)

---

## Authentication Module

**Prefix:** `/api/auth`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/login | User login (OAuth2 form) |
| POST | /api/auth/login-json | User login (JSON body) |
| POST | /api/auth/refresh | Refresh access token |
| POST | /api/auth/signup/student | Register new student |
| POST | /api/auth/signup/teacher | Register new teacher |
| POST | /api/auth/signup/admin | Register new admin |
| POST | /api/auth/signup/authority | Register new authority |
| POST | /api/auth/signup/parent | Register new parent |
| POST | /api/auth/signup/hod | Register new HOD |
| POST | /api/auth/signup/exam-section | Register new exam section |
| POST | /api/auth/signup/library | Register new library manager |
| POST | /api/auth/signup/account | Register new account section |
| POST | /api/auth/logout | Logout user |

---

## Super Admin Module

**Prefix:** `/api/admin`

### Dashboard & User Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/dashboard | Get dashboard statistics |
| GET | /api/admin/users/stats/by-role | Get user statistics by role |
| GET | /api/admin/users/students/list | Get students list |
| GET | /api/admin/users/teachers/list | Get teachers list |
| GET | /api/admin/users/parents/list | Get parents list |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/users | List all users |
| GET | /api/admin/users/{user_id} | Get user by ID |
| PATCH | /api/admin/users/{user_id}/toggle-active | Toggle user active status |
| PUT | /api/admin/users/{user_id}/deactivate | Deactivate user |
| GET | /api/admin/users-by-role | Get user count by role |
| POST | /api/admin/users/{user_id}/reset-password | Reset user password |
| POST | /api/admin/users/{user_id}/lock | Lock user account |
| POST | /api/admin/users/{user_id}/force-logout | Force logout user |
| GET | /api/admin/users/{user_id}/login-history | Get user login history |
| POST | /api/admin/users/{user_id}/change-role | Change user role |

### Settings Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/settings | List all system settings |
| GET | /api/admin/settings/{key} | Get specific setting |
| PUT | /api/admin/settings/{key} | Update system setting |
| GET | /api/admin/settings/general | Get general settings |
| PATCH | /api/admin/settings/general | Update general settings |
| GET | /api/admin/settings/academic | Get academic settings |
| PATCH | /api/admin/settings/academic | Update academic settings |
| GET | /api/admin/settings/localization | Get localization settings |
| PATCH | /api/admin/settings/localization | Update localization settings |
| GET | /api/admin/settings/smtp | Get SMTP settings |
| PATCH | /api/admin/settings/smtp | Update SMTP settings |
| POST | /api/admin/settings/smtp/test | Test SMTP settings |
| GET | /api/admin/settings/payment | Get payment settings |
| PATCH | /api/admin/settings/payment | Update payment settings |
| GET | /api/admin/settings/notifications | Get notification settings |
| PATCH | /api/admin/settings/notifications | Update notification settings |
| GET | /api/admin/settings/features | Get feature toggles |
| PATCH | /api/admin/settings/features | Update feature toggles |

### Features Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/features | List all features |
| PUT | /api/admin/features/{name}/toggle | Toggle feature |
| GET | /api/admin/system-features | List system features |
| GET | /api/admin/system-features/categories | Get feature categories |
| GET | /api/admin/system-features/{feature_code} | Get feature by code |
| POST | /api/admin/system-features | Create system feature |
| PUT | /api/admin/system-features/{feature_code} | Update system feature |
| DELETE | /api/admin/system-features/{feature_code} | Delete system feature |
| GET | /api/admin/system-features/{feature_code}/permissions | Get feature permissions |
| PUT | /api/admin/system-features/{feature_code}/permissions | Update feature permissions |

### Security Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/security/settings | Get security settings |
| PATCH | /api/admin/security/settings | Update security settings |
| GET | /api/admin/security/jwt | Get JWT settings |
| PATCH | /api/admin/security/jwt | Update JWT settings |
| GET | /api/admin/security/ip-whitelist | Get IP whitelist |

### Audit & Backups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/audit-logs | Get audit logs |
| GET | /api/admin/backups | List all backups |
| POST | /api/admin/backups | Create new backup |

---

## School Modules

### School Authority

**Prefix:** `/api/authorities`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/authorities/ | List all authorities |
| GET | /api/authorities/me | Get current authority profile |
| GET | /api/authorities/{authority_id} | Get authority by ID |
| POST | /api/authorities/ | Create new authority |
| PATCH | /api/authorities/{authority_id} | Update authority |
| DELETE | /api/authorities/{authority_id} | Delete authority |
| GET | /api/authorities/dashboard | Get authority dashboard |
| GET | /api/authorities/students | Get all students |
| GET | /api/authorities/teachers | Get all teachers |
| GET | /api/authorities/courses | Get all courses |
| GET | /api/authorities/fees | Get all fee records |
| GET | /api/authorities/notices | Get all notices |
| GET | /api/authorities/analytics/students | Get student analytics |
| GET | /api/authorities/analytics/attendance | Get attendance analytics |
| GET | /api/authorities/analytics/performance | Get performance analytics |
| GET | /api/authorities/reports | Get reports |

---

### School Teacher

**Prefix:** `/api/teachers`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/teachers/ | Create new teacher |
| GET | /api/teachers/{teacher_id} | Get teacher by ID |
| GET | /api/teachers/by-user/{user_id} | Get teacher by user ID |
| GET | /api/teachers/ | List all teachers |
| PUT | /api/teachers/{teacher_id} | Update teacher |
| DELETE | /api/teachers/{teacher_id} | Delete teacher |
| POST | /api/teachers/{teacher_id}/deactivate | Deactivate teacher |
| GET | /api/teachers/me | Get current teacher profile |
| PUT | /api/teachers/me | Update current teacher profile |
| GET | /api/teachers/dashboard | Get teacher dashboard |
| GET | /api/teachers/my-courses | Get teacher courses |
| GET | /api/teachers/my-students | Get teacher students |
| GET | /api/teachers/my-assignments | Get teacher assignments |
| GET | /api/teachers/my-tests | Get teacher tests |
| GET | /api/teachers/my-attendance | Get teacher attendance |
| GET | /api/teachers/my-timetable | Get teacher timetable |

---

### School Student

**Prefix:** `/api/students`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/students/ | Create new student |
| GET | /api/students/ | List all students |
| GET | /api/students/me | Get current student profile |
| PATCH | /api/students/me | Update current student profile |
| GET | /api/students/dashboard | Get student dashboard |
| GET | /api/students/{student_id} | Get student by ID |
| PUT | /api/students/{student_id} | Update student |
| DELETE | /api/students/{student_id} | Delete student |
| GET | /api/students/my-courses | Get student courses |
| GET | /api/students/my-assignments | Get student assignments |
| GET | /api/students/my-grades | Get student grades |
| GET | /api/students/my-attendance | Get student attendance |
| GET | /api/students/my-fees | Get student fees |
| GET | /api/students/my-tests | Get student tests |
| GET | /api/students/my-notices | Get student notices |
| GET | /api/students/my-timetable | Get student timetable |
| GET | /api/students/my-notes | Get student notes |
| GET | /api/students/my-videos | Get student videos |

---

### School Parent

**Prefix:** `/api/parents`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/parents/ | Create new parent |
| GET | /api/parents/{parent_id} | Get parent by ID |
| GET | /api/parents/ | List all parents |
| GET | /api/parents/me | Get current parent profile |
| PUT | /api/parents/{parent_id} | Update parent |
| DELETE | /api/parents/{parent_id} | Delete parent |
| GET | /api/parents/dashboard | Get parent dashboard |
| GET | /api/parents/child/{student_id}/attendance | Get child attendance |
| GET | /api/parents/child/{student_id}/grades | Get child grades |
| GET | /api/parents/child/{student_id}/homework | Get child homework |
| GET | /api/parents/notices | Get notices for parent |
| GET | /api/parents/chat | Get chat contacts |

---

### School Exam Section

**Prefix:** `/api/exams`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/exams | Create new exam schedule |
| GET | /api/exams/{exam_id} | Get exam by ID |
| GET | /api/exams | Get all exams |
| PUT | /api/exams/{exam_id} | Update exam |
| DELETE | /api/exams/{exam_id} | Delete exam |
| POST | /api/exams/grades | Create new grade |
| GET | /api/exams/grades/{grade_id} | Get grade by ID |
| GET | /api/exams/grades | Get all grades |
| PUT | /api/exams/grades/{grade_id} | Update grade |
| DELETE | /api/exams/grades/{grade_id} | Delete grade |

---

### School Library

**Prefix:** `/api/library`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/library/books | Create new book |
| GET | /api/library/books/{book_id} | Get book by ID |
| GET | /api/library/books | List books |
| PUT | /api/library/books/{book_id} | Update book |
| DELETE | /api/library/books/{book_id} | Delete book |
| POST | /api/library/loans | Issue book |
| GET | /api/library/loans/{loan_id}/return | Return book |
| GET | /api/library/loans/student/{student_id} | Get student loans |
| GET | /api/library/loans/overdue | Get overdue loans |
| GET | /api/library/summary | Get library summary |

---

### School Notices

**Prefix:** `/api/notices`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/notices/ | Create new notice |
| POST | /api/notices/{notice_id}/upload | Upload notice file |
| PUT | /api/notices/{notice_id} | Update notice |
| DELETE | /api/notices/{notice_id} | Delete notice |
| GET | /api/notices/ | Get notices |
| GET | /api/notices/urgent | Get urgent notices |
| GET | /api/notices/recent | Get recent notices |
| GET | /api/notices/{notice_id} | Get notice by ID |
| GET | /api/notices/search/ | Search notices |

---

### School Courses

**Prefix:** `/api/courses`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/courses/ | Get all courses |
| GET | /api/courses/{course_id} | Get course by ID |
| POST | /api/courses/ | Create new course |
| PUT | /api/courses/{course_id} | Update course |
| DELETE | /api/courses/{course_id} | Delete course |
| GET | /api/courses/{course_id}/students | Get course students |
| GET | /api/courses/search/{query} | Search courses |
| GET | /api/courses/teacher/my | Get teacher courses |

---

### School Attendance

**Prefix:** `/api/attendance`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/attendance/dashboard | Get attendance dashboard |
| GET | /api/attendance/records | Get attendance records |
| GET | /api/attendance/student/{student_id}/summary | Get student attendance summary |
| POST | /api/attendance/mark | Mark attendance |
| POST | /api/attendance/bulk | Bulk mark attendance |
| GET | /api/attendance/course/{course_id} | Get course attendance |
| GET | /api/attendance/course/{course_id}/stats | Get course attendance stats |
| GET | /api/attendance/student/my | Get my attendance |
| GET | /api/attendance/student/my/course/{course_id} | Get my course attendance |

---

### School Account Section

**Prefix:** `/api/account`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/account/fees | Create new fee record |
| GET | /api/account/fees/{fee_id} | Get fee by ID |
| GET | /api/account/fees | List fees |
| PUT | /api/account/fees/{fee_id} | Update fee |
| DELETE | /api/account/fees/{fee_id} | Delete fee |
| POST | /api/account/fees/{fee_id}/payment | Process payment |
| POST | /api/account/fees/bulk | Bulk create fees |
| POST | /api/account/expenses | Create new expense |
| GET | /api/account/expenses/{expense_id} | Get expense by ID |
| GET | /api/account/expenses | List expenses |
| PUT | /api/account/expenses/{expense_id} | Update expense |
| DELETE | /api/account/expenses/{expense_id} | Delete expense |
| GET | /api/account/summary | Get financial summary |

---

### School Assignments

**Prefix:** `/api/assignments`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/assignments/ | Create new assignment |
| GET | /api/assignments/{assignment_id} | Get assignment by ID |
| PUT | /api/assignments/{assignment_id} | Update assignment |
| DELETE | /api/assignments/{assignment_id} | Delete assignment |
| POST | /api/assignments/{assignment_id}/upload | Upload assignment file |
| POST | /api/assignments/{assignment_id}/submit | Submit assignment |
| GET | /api/assignments/{assignment_id}/submissions | Get assignment submissions |
| GET | /api/assignments/{assignment_id}/my-submission | Get my submission |
| PUT | /api/assignments/submissions/{submission_id}/grade | Grade submission |
| GET | /api/assignments/teacher/my-assignments | Get teacher assignments |

---

### School Timetable

**Prefix:** `/api/timetable`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/timetable/entries | Get all timetable entries |
| GET | /api/timetable/entries/{entry_id} | Get timetable entry by ID |
| POST | /api/timetable/entries | Create timetable entry |
| PUT | /api/timetable/entries/{entry_id} | Update timetable entry |
| DELETE | /api/timetable/entries/{entry_id} | Delete timetable entry |

---

### School Videos

**Prefix:** `/api/videos`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/videos/upload | Upload video |
| GET | /api/videos/teacher/my-videos | Get teacher videos |
| GET | /api/videos/{video_id} | Get video by ID |
| DELETE | /api/videos/{video_id} | Delete video |
| GET | /api/videos/course/{course_id} | Get course videos |
| GET | /api/videos/{video_id}/stream | Stream video |
| GET | /api/videos/search/{query} | Search videos |
| GET | /api/videos/recent/all | Get recent videos |

---

## College Modules

### College Courses

**Prefix:** `/api/college`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/courses | Create new course |
| GET | /api/college/courses | List courses |
| GET | /api/college/courses/{course_id} | Get course by ID |
| PATCH | /api/college/courses/{course_id} | Update course |
| DELETE | /api/college/courses/{course_id} | Delete course |
| POST | /api/college/departments | Create new department |
| GET | /api/college/departments | List departments |
| GET | /api/college/departments/{department_id} | Get department by ID |
| PATCH | /api/college/departments/{department_id} | Update department |
| DELETE | /api/college/departments/{department_id} | Delete department |
| POST | /api/college/programs | Create new program |
| GET | /api/college/programs | List programs |
| GET | /api/college/programs/{program_id} | Get program by ID |
| GET | /api/college/semesters | List semesters |
| GET | /api/college/semesters/{semester_id} | Get semester by ID |
| POST | /api/college/enrollments | Enroll student in course |
| GET | /api/college/enrollments | List enrollments |
| GET | /api/college/enrollments/{enrollment_id} | Get enrollment by ID |
| PATCH | /api/college/enrollments/{enrollment_id} | Update enrollment |
| DELETE | /api/college/enrollments/{enrollment_id} | Drop course |

---

### College Faculty

**Prefix:** `/api/college/faculty`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/faculty/ | Create new faculty member |
| GET | /api/college/faculty/ | List all faculty |
| GET | /api/college/faculty/me | Get current faculty profile |
| PATCH | /api/college/faculty/me | Update current faculty profile |
| GET | /api/college/faculty/{faculty_id} | Get faculty by ID |
| PUT | /api/college/faculty/{faculty_id} | Update faculty |
| DELETE | /api/college/faculty/{faculty_id} | Delete faculty |
| GET | /api/college/faculty/dashboard | Get faculty dashboard |
| GET | /api/college/faculty/my-courses | Get faculty courses |
| GET | /api/college/faculty/my-students | Get faculty students |

---

### College Hostel

**Prefix:** `/api/college/hostels`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/hostels/ | Create new hostel |
| GET | /api/college/hostels/ | List hostels |
| GET | /api/college/hostels/{hostel_id} | Get hostel by ID |
| PATCH | /api/college/hostels/{hostel_id} | Update hostel |
| POST | /api/college/hostels/{hostel_id}/rooms | Create new room |
| GET | /api/college/hostels/{hostel_id}/rooms | List rooms in hostel |
| POST | /api/college/hostels/allocate | Allocate room to student |
| GET | /api/college/hostels/student/{student_id}/allocation | Get student allocation |
| POST | /api/college/hostels/vacate | Vacate hostel room |
| POST | /api/college/hostels/complaints | Create complaint |
| GET | /api/college/hostels/complaints | List complaints |
| PUT | /api/college/hostels/complaints/{complaint_id}/resolve | Resolve complaint |

---

### College Lab

**Prefix:** `/api/college/labs`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/labs/ | Create new lab |
| GET | /api/college/labs/ | List labs |
| GET | /api/college/labs/{lab_id} | Get lab by ID |
| POST | /api/college/labs/{lab_id}/equipment | Add equipment to lab |
| GET | /api/college/labs/{lab_id}/equipment | List lab equipment |
| POST | /api/college/labs/{lab_id}/schedules | Create lab schedule |
| GET | /api/college/labs/{lab_id}/schedules | List lab schedules |

---

### College Placement

**Prefix:** `/api/college/placements`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/placements/companies | Create new company |
| GET | /api/college/placements/companies | List companies |
| GET | /api/college/placements/companies/{company_id} | Get company by ID |
| POST | /api/college/placements/jobs | Create new job |
| GET | /api/college/placements/jobs | List jobs |
| GET | /api/college/placements/jobs/{job_id} | Get job by ID |
| POST | /api/college/placements/apply | Apply for job |
| GET | /api/college/placements/applications/student/{student_id} | Get student applications |
| GET | /api/college/placements/applications/job/{job_id} | Get job applications |
| PATCH | /api/college/placements/applications/{application_id}/status | Update application status |

---

### College Research

**Prefix:** `/api/college/research`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/research/projects | Create research project |
| GET | /api/college/research/projects | List research projects |
| GET | /api/college/research/projects/{project_id} | Get project by ID |
| POST | /api/college/research/publications | Create publication |
| GET | /api/college/research/publications | List publications |
| GET | /api/college/research/publications/{pub_id} | Get publication by ID |
| POST | /api/college/research/patents | Create patent |
| GET | /api/college/research/patents | List patents |

---

### College Student

**Prefix:** `/api/college/students`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/college/students/ | Create new college student |
| GET | /api/college/students/ | List all college students |
| GET | /api/college/students/me | Get current student profile |
| PATCH | /api/college/students/me | Update current student profile |
| GET | /api/college/students/{student_id} | Get student by ID |
| PUT | /api/college/students/{student_id} | Update student |
| DELETE | /api/college/students/{student_id} | Delete student |
| GET | /api/college/students/dashboard | Get student dashboard |
| GET | /api/college/students/my-courses | Get student courses |
| GET | /api/college/students/my-enrollments | Get student enrollments |
| GET | /api/college/students/my-grades | Get student grades |
| GET | /api/college/students/my-hostel | Get student hostel allocation |

---

### College Dean

**Prefix:** `/api/dean`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/dean/dashboard | Get dean dashboard |
| GET | /api/dean/departments | Get all departments |
| GET | /api/dean/departments/{dept_id} | Get department details |
| GET | /api/dean/programs | Get all programs |
| GET | /api/dean/faculty | Get all faculty |
| GET | /api/dean/students | Get all college students |

---

### College Exam Section

**Prefix:** `/api/exam-section`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/exam-section/dashboard | Get exam section dashboard |
| GET | /api/exam-section/results | Get exam results |

---

### College HOD

**Prefix:** `/api/hod`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/hod/dashboard | Get HOD dashboard |
| GET | /api/hod/department/{dept_id} | Get department details |
| GET | /api/hod/faculty?department_id={id} | Get department faculty |
| GET | /api/hod/courses?department_id={id} | Get department courses |

---

### College Registrar

**Prefix:** `/api/registrar`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/registrar/dashboard | Get registrar dashboard |
| GET | /api/registrar/students | Get all students |
| GET | /api/registrar/students/{student_id} | Get student details |
| GET | /api/registrar/enrollments | Get student enrollments |

---

### College Account Section

**Prefix:** `/api/college/account`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/college/account/dashboard | Get account dashboard |
| GET | /api/college/account/fee-structures | Get fee structures |
| GET | /api/college/account/fee-records | Get fee records |

---

## Summary

| Module Category | Total Endpoints |
|-----------------|------------------|
| Authentication | 13 |
| Super Admin | ~50+ |
| School Modules | ~100+ |
| College Modules | ~80+ |
| **Total** | **~250+** |

---

*Last Updated: 2026-03-29*
*Generated from module analysis*
