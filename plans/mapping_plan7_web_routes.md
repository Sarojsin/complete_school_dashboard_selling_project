# Endpoint Mapping Plan 7: Web Routes & Remaining Endpoints

## Overview

This document maps all web routes and remaining endpoints from the monolithic backup to the new modular structure.

---

## Source Files Analyzed

| File | Endpoints Count |
|------|-----------------|
| `backup/web/routers/common.py` | 18 endpoints |
| `backup/web/routers/student.py` | 32 endpoints |
| `backup/web/routers/teacher.py` | 51 endpoints |
| `backup/api/endpoints/websocket_chat.py` | 1 endpoint |
| **Total** | **~102 endpoints** |

---

## Endpoint Mapping Table

### Common Web Routes

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/` | `web_common` | `/` | Home page (HTML) |
| GET | `/logout` | `auth` | `/auth/logout` | Logout |
| GET | `/login` | `auth` | `/auth/login-page` | Login page (HTML) |
| GET | `/signup` | `auth` | `/auth/signup-page` | Signup page (HTML) |
| GET | `/signup/student` | `auth` | `/auth/signup/student-page` | Student signup (HTML) |
| GET | `/signup/teacher` | `auth` | `/auth/signup/teacher-page` | Teacher signup (HTML) |
| GET | `/signup/authority` | `auth` | `/auth/signup/authority-page` | Authority signup (HTML) |
| GET | `/signup/parent` | `auth` | `/auth/signup/parent-page` | Parent signup (HTML) |
| GET | `/signup/hod` | `auth` | `/auth/signup/hod-page` | HOD signup (HTML) |
| GET | `/signup/exam-section` | `auth` | `/auth/signup/exam-section-page` | Exam section signup (HTML) |
| GET | `/signup/library` | `auth` | `/auth/signup/library-page` | Library signup (HTML) |
| GET | `/signup/account` | `auth` | `/auth/signup/account-page` | Account signup (HTML) |
| GET | `/signup/admin` | `auth` | `/auth/signup/admin-page` | Admin signup (HTML) |
| POST | `/signup/admin` | `auth` | `/auth/signup/admin` | Admin signup handler |
| GET | `/register` | `auth` | `/auth/register-page` | Register page (HTML) |
| GET | `/register/student` | `auth` | `/auth/register/student-page` | Register student (HTML) |
| GET | `/register/teacher` | `auth` | `/auth/register/teacher-page` | Register teacher (HTML) |
| GET | `/register/parent` | `auth` | `/auth/register/parent-page` | Register parent (HTML) |

### Student Web Routes

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/student/dashboard` | `school_student` | `/student/dashboard` | Student dashboard |
| GET | `/student/profile` | `school_student` | `/student/profile` | Student profile |
| POST | `/student/profile` | `school_student` | `/student/profile` | Update profile |
| GET | `/student/courses` | `school_courses` | `/student/courses` | Student courses |
| GET | `/student/assignments` | `school_assignments` | `/student/assignments` | Student assignments |
| GET | `/student/fees` | `school_account_section` | `/student/fees` | Student fees |
| GET | `/student/assignments/{assignment_id}` | `school_assignments` | `/student/assignments/{assignment_id}` | Assignment detail |
| POST | `/student/assignments/{assignment_id}/submit` | `school_assignments` | `/student/assignments/{assignment_id}/submit` | Submit assignment |
| GET | `/student/tests` | `school_tests` | `/student/tests` | Test list |
| GET | `/student/tests/{test_id}/start` | `school_tests` | `/student/tests/{test_id}/start` | Take test |
| POST | `/student/tests/{test_id}/submit` | `school_tests` | `/student/tests/{test_id}/submit` | Submit test |
| GET | `/student/tests/{test_id}/result` | `school_tests` | `/student/tests/{test_id}/result` | Test result |
| GET | `/student/notices` | `school_notices` | `/student/notices` | Student notices |
| GET | `/student/timetable` | `school_timetable` | `/student/timetable` | Student timetable |
| GET | `/student/notes` | `school_notes` | `/student/notes` | Student notes |
| GET | `/student/videos` | `school_videos` | `/student/videos` | Student videos |
| GET | `/student/forum` | `school_groups` | `/student/forum` | Student forum |
| GET | `/student/messages` | `school_chat` | `/student/messages` | Student messages |
| POST | `/student/messages/{message_id}/read` | `school_chat` | `/student/messages/{message_id}/read` | Mark read |
| GET | `/student/teachers` | `school_teacher` | `/student/teachers` | Student teachers |
| POST | `/student/teachers/{teacher_id}/contact` | `school_chat` | `/student/teachers/{teacher_id}/contact` | Contact teacher |
| GET | `/student/groups` | `school_groups` | `/student/groups` | Student groups |
| GET | `/student/grades` | `school_grades` | `/student/grades` | Student grades |
| GET | `/student/attendance` | `school_attendance` | `/student/attendance` | Student attendance |
| POST | `/student/mark-video-watched/{video_id}` | `school_videos` | `/student/mark-video-watched/{video_id}` | Mark watched |
| GET | `/student/groups/{group_id}` | `school_groups` | `/student/groups/{group_id}` | Group detail |
| POST | `/student/groups/join` | `school_groups` | `/student/groups/join` | Join group |
| GET | `/student/groups/{group_id}/posts` | `school_groups` | `/student/groups/{group_id}/posts` | Group posts |
| GET | `/student/groups/{group_id}/posts/{post_id}` | `school_groups` | `/student/groups/{group_id}/posts/{post_id}` | View post |
| GET | `/student/exam-results` | `school_exam_section` | `/student/exam-results` | Exam results |
| GET | `/student/library` | `school_library` | `/student/library` | Student library |

### Teacher Web Routes

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| GET | `/teacher/dashboard` | `school_teacher` | `/teacher/dashboard` | Teacher dashboard |
| GET | `/teacher/profile` | `school_teacher` | `/teacher/profile` | Teacher profile |
| POST | `/teacher/profile` | `school_teacher` | `/teacher/profile` | Update profile |
| GET | `/teacher/students` | `school_student` | `/teacher/students` | Teacher students |
| GET | `/teacher/students/{student_id}` | `school_student` | `/teacher/students/{student_id}` | Student detail |
| GET | `/teacher/students/{student_id}/grades` | `school_grades` | `/teacher/students/{student_id}/grades` | Student grades |
| POST | `/teacher/students/{student_id}/contact` | `school_chat` | `/teacher/students/{student_id}/contact` | Contact student |
| GET | `/teacher/messages` | `school_chat` | `/teacher/messages` | Teacher messages |
| POST | `/teacher/messages/{message_id}/read` | `school_chat` | `/teacher/messages/{message_id}/read` | Mark read |
| GET | `/teacher/assignments` | `school_assignments` | `/teacher/assignments` | Teacher assignments |
| GET | `/teacher/assignments/{id}/edit` | `school_assignments` | `/teacher/assignments/{id}/edit` | Edit assignment |
| POST | `/teacher/assignments/{id}/edit` | `school_assignments` | `/teacher/assignments/{id}/edit` | Edit assignment post |
| GET | `/teacher/assignments/create` | `school_assignments` | `/teacher/assignments/create` | Create assignment |
| POST | `/teacher/assignments/create` | `school_assignments` | `/teacher/assignments/create` | Create assignment post |
| GET | `/teacher/assignments/{id}/submissions` | `school_assignments` | `/teacher/assignments/{id}/submissions` | View submissions |
| POST | `/teacher/assignments/submissions/{submission_id}/grade` | `school_assignments` | `/teacher/assignments/submissions/{submission_id}/grade` | Grade submission |
| DELETE | `/teacher/assignments/delete/{id}` | `school_assignments` | `/teacher/assignments/delete/{id}` | Delete assignment |
| GET | `/teacher/notes/upload` | `school_notes` | `/teacher/notes/upload` | Upload notes |
| POST | `/teacher/notes/upload` | `school_notes` | `/teacher/notes/upload` | Upload notes post |
| GET | `/teacher/courses/{id}` | `school_courses` | `/teacher/courses/{id}` | Course detail |
| GET | `/teacher/courses/{id}/students` | `school_courses` | `/teacher/courses/{id}/students` | Course students |
| GET | `/teacher/attendance/take` | `school_attendance` | `/teacher/attendance/take` | Take attendance |
| POST | `/teacher/attendance/save` | `school_attendance` | `/teacher/attendance/save` | Save attendance |
| GET | `/teacher/attendance` | `school_attendance` | `/teacher/attendance` | Attendance list |
| GET | `/teacher/attendance/view/{id}` | `school_attendance` | `/teacher/attendance/view/{id}` | View attendance |
| GET | `/teacher/grades` | `school_grades` | `/teacher/grades` | Teacher grades |
| GET | `/teacher/grades/add` | `school_grades` | `/teacher/grades/add` | Add grades |
| POST | `/teacher/grades/add` | `school_grades` | `/teacher/grades/add` | Add grades post |
| GET | `/teacher/attendance/{id}/edit` | `school_attendance` | `/teacher/attendance/{id}/edit` | Edit attendance |
| GET | `/teacher/tests` | `school_tests` | `/teacher/tests` | Teacher tests |
| GET | `/teacher/tests/create` | `school_tests` | `/teacher/tests/create` | Create test |
| GET | `/teacher/tests/{id}/results` | `school_tests` | `/teacher/tests/{id}/results` | Test results |
| GET | `/teacher/tests/{id}/edit` | `school_tests` | `/teacher/tests/{id}/edit` | Edit test |
| POST | `/teacher/tests/create` | `school_tests` | `/teacher/tests/create` | Create test post |
| DELETE | `/teacher/tests/delete/{id}` | `school_tests` | `/teacher/tests/delete/{id}` | Delete test |
| GET | `/teacher/videos/upload` | `school_videos` | `/teacher/videos/upload` | Upload videos |
| POST | `/teacher/videos/upload` | `school_videos` | `/teacher/videos/upload` | Upload videos post |
| GET | `/teacher/courses` | `school_courses` | `/teacher/courses` | Teacher courses |
| GET | `/teacher/notices/create` | `school_notices` | `/teacher/notices/create` | Create notice |
| POST | `/teacher/notices/create` | `school_notices` | `/teacher/notices/create` | Create notice post |
| GET | `/teacher/groups` | `school_groups` | `/teacher/groups` | Teacher groups |
| GET | `/teacher/groups/{group_id}` | `school_groups` | `/teacher/groups/{group_id}` | Group detail |
| GET | `/teacher/groups/{group_id}/posts/create` | `school_groups` | `/teacher/groups/{group_id}/posts/create` | Create post form |
| POST | `/teacher/groups/{group_id}/posts/create` | `school_groups` | `/teacher/groups/{group_id}/posts/create` | Create post |
| GET | `/teacher/groups/{group_id}/edit` | `school_groups` | `/teacher/groups/{group_id}/edit` | Edit group form |
| POST | `/teacher/groups/{group_id}/edit` | `school_groups` | `/teacher/groups/{group_id}/edit` | Edit group |
| GET | `/teacher/groups/{group_id}/posts` | `school_groups` | `/teacher/groups/{group_id}/posts` | Group posts |
| GET | `/teacher/groups/{group_id}/posts/{post_id}` | `school_groups` | `/teacher/groups/{group_id}/posts/{post_id}` | View post |
| POST | `/teacher/groups/{group_id}/posts/{post_id}/delete` | `school_groups` | `/teacher/groups/{group_id}/posts/{post_id}/delete` | Delete post |
| GET | `/teacher/chat` | `school_chat` | `/teacher/chat` | Teacher chat |
| GET | `/teacher/timetable` | `school_timetable` | `/teacher/timetable` | Teacher timetable |

### WebSocket Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| WS | `/api/ws/chat` | `school_chat` | `/ws/chat` | WebSocket chat |

---

## Module Status Summary

| Module | Endpoints | Status | Priority |
|--------|-----------|--------|----------|
| `web_common` | ~18 | 🆕 New | Low |
| `school_student` (web) | ~32 | 🆕 New | Low |
| `school_teacher` (web) | ~51 | 🆕 New | Low |
| `school_chat` (ws) | ~1 | 🆕 New | Medium |

---

## Notes

1. Web routes are HTML pages that render templates
2. These are separate from API endpoints which return JSON
3. WebSocket endpoint for real-time chat needs special handling
4. Many web routes duplicate API functionality but return HTML

---

## Action Items

### web_common
- [ ] Create new module for common web routes
- [ ] Add home page
- [ ] Add login/signup pages
- [ ] Add register pages

### school_student (web)
- [ ] Add dashboard page
- [ ] Add profile page
- [ ] Add courses page
- [ ] Add assignments page
- [ ] Add tests page
- [ ] Add other student pages

### school_teacher (web)
- [ ] Add dashboard page
- [ ] Add profile page
- [ ] Add courses page
- [ ] Add assignments page
- [ ] Add tests page
- [ ] Add attendance page
- [ ] Add grades page
- [ ] Add other teacher pages

### school_chat (ws)
- [ ] Add WebSocket endpoint
- [ ] Implement real-time messaging
