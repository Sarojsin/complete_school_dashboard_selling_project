# Missing Endpoints Migration Plan - Priority 8: Web Routes & WebSocket

**Plan 8: Web Routes & Real-time Communication**

This plan covers Web Routes (HTML pages), WebSocket, and any remaining endpoints.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Web Routes | ~120+ endpoints | LOW |
| WebSocket | 1 endpoint | LOW |

---

## 1. Web Routes (HTML Pages)

**Target Location:** `modules/web_common/` or individual module `web.py` files

### Missing Web Routes by Category

#### Common Routes

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/` | Home page (HTML) | backup/web/routers/common.py |
| GET | `/logout` | Logout | backup/web/routers/common.py |
| GET | `/login` | Login page (HTML) | backup/web/routers/common.py |
| GET | `/signup` | Signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/student` | Student signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/teacher` | Teacher signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/authority` | Authority signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/parent` | Parent signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/hod` | HOD signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/exam-section` | Exam section signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/library` | Library signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/account` | Account signup page (HTML) | backup/web/routers/common.py |
| GET | `/signup/admin` | Admin signup page (HTML) | backup/web/routers/common.py |
| POST | `/signup/admin` | Admin signup handler | backup/web/routers/common.py |
| GET | `/register` | Register page (HTML) | backup/web/routers/common.py |
| GET | `/register/student` | Register student page (HTML) | backup/web/routers/common.py |
| GET | `/register/teacher` | Register teacher page (HTML) | backup/web/routers/common.py |
| GET | `/register/parent` | Register parent page (HTML) | backup/web/routers/common.py |

#### Student Web Routes

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/student/dashboard` | Student dashboard | backup/web/routers/student.py |
| GET | `/student/profile` | Student profile | backup/web/routers/student.py |
| POST | `/student/profile` | Update student profile | backup/web/routers/student.py |
| GET | `/student/courses` | Student courses | backup/web/routers/student.py |
| GET | `/student/assignments` | Student assignments | backup/web/routers/student.py |
| GET | `/student/fees` | Student fees | backup/web/routers/student.py |
| GET | `/student/assignments/{assignment_id}` | Assignment detail | backup/web/routers/student.py |
| POST | `/student/assignments/{assignment_id}/submit` | Submit assignment | backup/web/routers/student.py |
| GET | `/student/tests` | Test list | backup/web/routers/student.py |
| GET | `/student/tests/{test_id}/start` | Take test | backup/web/routers/student.py |
| POST | `/student/tests/{test_id}/submit` | Submit test | backup/web/routers/student.py |
| GET | `/student/tests/{test_id}/result` | Test result | backup/web/routers/student.py |
| GET | `/student/notices` | Student notices | backup/web/routers/student.py |
| GET | `/student/timetable` | Student timetable | backup/web/routers/student.py |
| GET | `/student/notes` | Student notes | backup/web/routers/student.py |
| GET | `/student/videos` | Student videos | backup/web/routers/student.py |
| GET | `/student/forum` | Student forum | backup/web/routers/student.py |
| GET | `/student/messages` | Student messages | backup/web/routers/student.py |
| POST | `/student/messages/{message_id}/read` | Mark message read | backup/web/routers/student.py |
| GET | `/student/teachers` | Student teachers | backup/web/routers/student.py |
| POST | `/student/teachers/{teacher_id}/contact` | Contact teacher | backup/web/routers/student.py |
| GET | `/student/groups` | Student groups | backup/web/routers/student.py |
| GET | `/student/grades` | Student grades | backup/web/routers/student.py |
| GET | `/student/attendance` | Student attendance | backup/web/routers/student.py |
| POST | `/student/mark-video-watched/{video_id}` | Mark video watched | backup/web/routers/student.py |
| GET | `/student/groups/{group_id}` | Group detail | backup/web/routers/student.py |
| POST | `/student/groups/join` | Join group | backup/web/routers/student.py |
| GET | `/student/groups/{group_id}/posts` | Group posts | backup/web/routers/student.py |
| GET | `/student/groups/{group_id}/posts/{post_id}` | View post | backup/web/routers/student.py |
| GET | `/student/exam-results` | Exam results | backup/web/routers/student.py |
| GET | `/student/library` | Student library | backup/web/routers/student.py |

#### Teacher Web Routes

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/teacher/dashboard` | Teacher dashboard | backup/web/routers/teacher.py |
| GET | `/teacher/profile` | Teacher profile | backup/web/routers/teacher.py |
| POST | `/teacher/profile` | Update teacher profile | backup/web/routers/teacher.py |
| GET | `/teacher/students` | Teacher students | backup/web/routers/teacher.py |
| GET | `/teacher/students/{student_id}` | Student detail | backup/web/routers/teacher.py |
| GET | `/teacher/students/{student_id}/grades` | Student grades | backup/web/routers/teacher.py |
| POST | `/teacher/students/{student_id}/contact` | Contact student | backup/web/routers/teacher.py |
| GET | `/teacher/messages` | Teacher messages | backup/web/routers/teacher.py |
| POST | `/teacher/messages/{message_id}/read` | Mark message read | backup/web/routers/teacher.py |
| GET | `/teacher/assignments` | Teacher assignments | backup/web/routers/teacher.py |
| GET | `/teacher/assignments/{id}/edit` | Edit assignment | backup/web/routers/teacher.py |
| POST | `/teacher/assignments/{id}/edit` | Edit assignment post | backup/web/routers/teacher.py |
| GET | `/teacher/assignments/create` | Create assignment | backup/web/routers/teacher.py |
| POST | `/teacher/assignments/create` | Create assignment post | backup/web/routers/teacher.py |
| GET | `/teacher/assignments/{id}/submissions` | View submissions | backup/web/routers/teacher.py |
| POST | `/teacher/assignments/submissions/{submission_id}/grade` | Grade submission | backup/web/routers/teacher.py |
| DELETE | `/teacher/assignments/delete/{id}` | Delete assignment | backup/web/routers/teacher.py |
| GET | `/teacher/notes/upload` | Upload notes | backup/web/routers/teacher.py |
| POST | `/teacher/notes/upload` | Upload notes post | backup/web/routers/teacher.py |
| GET | `/teacher/courses/{id}` | Course detail | backup/web/routers/teacher.py |
| GET | `/teacher/courses/{id}/students` | Course students | backup/web/routers/teacher.py |
| GET | `/teacher/attendance/take` | Take attendance | backup/web/routers/teacher.py |
| POST | `/teacher/attendance/save` | Save attendance | backup/web/routers/teacher.py |
| GET | `/teacher/attendance` | Attendance list | backup/web/routers/teacher.py |
| GET | `/teacher/attendance/view/{id}` | View attendance | backup/web/routers/teacher.py |
| GET | `/teacher/grades` | Teacher grades | backup/web/routers/teacher.py |
| GET | `/teacher/grades/add` | Add grades | backup/web/routers/teacher.py |
| POST | `/teacher/grades/add` | Add grades post | backup/web/routers/teacher.py |
| GET | `/teacher/attendance/{id}/edit` | Edit attendance | backup/web/routers/teacher.py |
| GET | `/teacher/tests` | Teacher tests | backup/web/routers/teacher.py |
| GET | `/teacher/tests/create` | Create test | backup/web/routers/teacher.py |
| GET | `/teacher/tests/{id}/results` | Test results | backup/web/routers/teacher.py |
| GET | `/teacher/tests/{id}/edit` | Edit test | backup/web/routers/teacher.py |
| POST | `/teacher/tests/create` | Create test post | backup/web/routers/teacher.py |
| DELETE | `/teacher/tests/delete/{id}` | Delete test | backup/web/routers/teacher.py |
| GET | `/teacher/videos/upload` | Upload videos | backup/web/routers/teacher.py |
| POST | `/teacher/videos/upload` | Upload videos post | backup/web/routers/teacher.py |
| GET | `/teacher/courses` | Teacher courses | backup/web/routers/teacher.py |
| GET | `/teacher/notices/create` | Create notice | backup/web/routers/teacher.py |
| POST | `/teacher/notices/create` | Create notice post | backup/web/routers/teacher.py |
| GET | `/teacher/groups` | Teacher groups | backup/web/routers/teacher.py |
| GET | `/teacher/groups/{group_id}` | Group detail | backup/web/routers/teacher.py |
| GET | `/teacher/groups/{group_id}/posts/create` | Create post form | backup/web/routers/teacher.py |
| POST | `/teacher/groups/{group_id}/posts/create` | Create post | backup/web/routers/teacher.py |
| GET | `/teacher/groups/{group_id}/edit` | Edit group form | backup/web/routers/teacher.py |
| POST | `/teacher/groups/{group_id}/edit` | Edit group | backup/web/routers/teacher.py |
| GET | `/teacher/groups/{group_id}/posts` | Group posts | backup/web/routers/teacher.py |
| GET | `/teacher/groups/{group_id}/posts/{post_id}` | View post | backup/web/routers/teacher.py |
| POST | `/teacher/groups/{group_id}/posts/{post_id}/delete` | Delete post | backup/web/routers/teacher.py |
| GET | `/teacher/chat` | Teacher chat | backup/web/routers/teacher.py |
| GET | `/teacher/timetable` | Teacher timetable | backup/web/routers/teacher.py |
| POST | `/teacher/timetable` | Timetable post | backup/web/routers/teacher.py |

#### Authority Web Routes

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/authority/dashboard` | Authority dashboard | backup/web/routers/authority.py |
| GET | `/authority/students` | Authority students | backup/web/routers/authority.py |
| GET | `/authority/teachers` | Authority teachers | backup/web/routers/authority.py |
| GET | `/authority/courses` | Authority courses | backup/web/routers/authority.py |
| GET | `/authority/fees` | Authority fees | backup/web/routers/authority.py |
| GET | `/authority/notices` | Authority notices | backup/web/routers/authority.py |
| GET | `/authority/analytics` | Authority analytics | backup/web/routers/authority.py |
| GET | `/authority/students/add` | Add student form | backup/web/routers/authority.py |
| POST | `/authority/students/add` | Add student | backup/web/routers/authority.py |
| GET | `/authority/students/{id}` | Student detail | backup/web/routers/authority.py |
| GET | `/authority/students/{id}/edit` | Edit student form | backup/web/routers/authority.py |
| POST | `/authority/students/{id}/edit` | Edit student | backup/web/routers/authority.py |
| POST | `/authority/students/{id}/delete` | Delete student | backup/web/routers/authority.py |
| GET | `/authority/teachers/add` | Add teacher form | backup/web/routers/authority.py |
| POST | `/authority/teachers/add` | Add teacher | backup/web/routers/authority.py |
| GET | `/authority/teachers/{id}` | Teacher detail | backup/web/routers/authority.py |
| GET | `/authority/teachers/{id}/edit` | Edit teacher form | backup/web/routers/authority.py |
| POST | `/authority/teachers/{id}/edit` | Edit teacher | backup/web/routers/authority.py |
| POST | `/authority/teachers/{id}/delete` | Delete teacher | backup/web/routers/authority.py |
| GET | `/authority/courses/add` | Add course form | backup/web/routers/authority.py |
| POST | `/authority/courses/add` | Add course | backup/web/routers/authority.py |
| GET | `/authority/courses/{id}` | Course detail | backup/web/routers/authority.py |
| POST | `/authority/courses/{id}/enroll` | Enroll student | backup/web/routers/authority.py |
| POST | `/authority/courses/{id}/unenroll` | Unenroll student | backup/web/routers/authority.py |
| GET | `/authority/courses/{id}/edit` | Edit course form | backup/web/routers/authority.py |
| POST | `/authority/courses/{id}/edit` | Edit course | backup/web/routers/authority.py |
| POST | `/authority/courses/{id}/delete` | Delete course | backup/web/routers/authority.py |
| GET | `/authority/notices/create` | Create notice form | backup/web/routers/authority.py |
| POST | `/authority/notices/create` | Create notice | backup/web/routers/authority.py |
| GET | `/authority/notices/{id}` | View notice | backup/web/routers/authority.py |
| GET | `/authority/notices/{id}/edit` | Edit notice form | backup/web/routers/authority.py |
| POST | `/authority/notices/{id}/edit` | Edit notice | backup/web/routers/authority.py |
| GET | `/authority/fees/add` | Add fee form | backup/web/routers/authority.py |
| POST | `/authority/fees/add` | Add fee | backup/web/routers/authority.py |
| GET | `/authority/fees/structure` | Fee structure | backup/web/routers/authority.py |
| GET | `/authority/groups` | Authority groups | backup/web/routers/authority.py |
| GET | `/authority/groups/create` | Create group form | backup/web/routers/authority.py |
| POST | `/authority/groups/create` | Create group | backup/web/routers/authority.py |
| GET | `/authority/groups/{group_id}/manage` | Manage group | backup/web/routers/authority.py |
| POST | `/authority/groups/{group_id}/delete` | Delete group | backup/web/routers/authority.py |
| POST | `/authority/groups/{group_id}/add-member` | Add group member | backup/web/routers/authority.py |
| POST | `/authority/groups/{group_id}/remove-member` | Remove group member | backup/web/routers/authority.py |
| GET | `/authority/groups/{group_id}/posts` | Group posts | backup/web/routers/authority.py |
| GET | `/authority/groups/{group_id}/posts/create` | Create post form | backup/web/routers/authority.py |
| POST | `/authority/groups/{group_id}/posts/create` | Create post | backup/web/routers/authority.py |
| GET | `/authority/groups/{group_id}/posts/{post_id}` | View post | backup/web/routers/authority.py |
| POST | `/authority/groups/{group_id}/posts/{post_id}/delete` | Delete post | backup/web/routers/authority.py |
| GET | `/authority/reports` | Authority reports | backup/web/routers/authority.py |
| GET | `/authority/departments` | Authority departments | backup/web/routers/authority.py |
| POST | `/authority/departments/add` | Add department | backup/web/routers/authority.py |
| POST | `/authority/departments/{id}/edit` | Edit department | backup/web/routers/authority.py |
| POST | `/authority/departments/{id}/delete` | Delete department | backup/web/routers/authority.py |

#### Admin Web Routes

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/admin/dashboard` | Admin dashboard | backup/web/routers/admin.py |
| GET | `/admin/features` | Admin features | backup/web/routers/admin.py |
| GET | `/admin/features/{feature_code}` | Feature detail | backup/web/routers/admin.py |
| GET | `/admin/audit` | Audit logs | backup/web/routers/admin.py |
| GET | `/admin/settings` | Admin settings | backup/web/routers/admin.py |
| GET | `/admin/users` | Admin users | backup/web/routers/admin.py |
| GET | `/admin/academic` | Admin academic | backup/web/routers/admin.py |
| GET | `/admin/finance` | Admin finance | backup/web/routers/admin.py |
| GET | `/admin/system` | Admin system | backup/web/routers/admin.py |
| GET | `/admin/security` | Admin security | backup/web/routers/admin.py |
| GET | `/admin/backup` | Admin backup | backup/web/routers/admin.py |
| GET | `/admin/reports` | Admin reports | backup/web/routers/admin.py |
| GET | `/admin/notices` | Admin notices | backup/web/routers/admin.py |
| GET | `/admin/communication` | Admin communication | backup/web/routers/admin.py |
| GET | `/admin/media` | Admin media | backup/web/routers/admin.py |
| GET | `/admin/advanced` | Admin advanced | backup/web/routers/admin.py |

#### Other Web Routes (HOD, Exam Section, Library, Account, Groups)

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/hod/dashboard` | HOD dashboard | backup/web/routers/hod.py |
| GET | `/hod/teachers` | HOD teachers | backup/web/routers/hod.py |
| GET | `/hod/students` | HOD students | backup/web/routers/hod.py |
| GET | `/hod/students/{student_id}/performance` | Student performance | backup/web/routers/hod.py |
| GET | `/hod/reports` | HOD reports | backup/web/routers/hod.py |
| GET | `/hod/profile` | HOD profile | backup/web/routers/hod.py |
| GET | `/exam-section/dashboard` | Exam dashboard | backup/web/routers/exam_section.py |
| GET | `/exam-section/post-result` | Post result page | backup/web/routers/exam_section.py |
| POST | `/exam-section/post-result` | Post result action | backup/web/routers/exam_section.py |
| GET | `/exam-section/results` | All results | backup/web/routers/exam_section.py |
| GET | `/exam-section/grade-sheet/{student_id}` | Grade sheet | backup/web/routers/exam_section.py |
| GET | `/exam-section/notices` | Exam notices | backup/web/routers/exam_section.py |
| GET | `/exam-section/notices/create` | Create notice page | backup/web/routers/exam_section.py |
| POST | `/exam-section/notices/create` | Create notice action | backup/web/routers/exam_section.py |
| GET | `/exam-section/profile` | Exam profile | backup/web/routers/exam_section.py |
| GET | `/library/dashboard` | Library dashboard | backup/web/routers/library.py |
| GET | `/library/issue-book` | Issue book page | backup/web/routers/library.py |
| POST | `/library/issue-book` | Issue book action | backup/web/routers/library.py |
| GET | `/library/return-book` | Return book page | backup/web/routers/library.py |
| POST | `/library/return-book/{loan_id}` | Return book action | backup/web/routers/library.py |
| GET | `/library/overdue` | Overdue books | backup/web/routers/library.py |
| GET | `/library/history/{student_id}` | Student history | backup/web/routers/library.py |
| GET | `/library/books` | Book catalog | backup/web/routers/library.py |
| GET | `/library/books/add` | Add book page | backup/web/routers/library.py |
| POST | `/library/books/add` | Add book action | backup/web/routers/library.py |
| GET | `/library/profile` | Library profile | backup/web/routers/library.py |
| GET | `/account/dashboard` | Account dashboard | backup/web/routers/account.py |
| GET | `/account/record-payment` | Record payment page | backup/web/routers/account.py |
| POST | `/account/record-payment` | Record payment action | backup/web/routers/account.py |
| GET | `/account/fees` | Fees list | backup/web/routers/account.py |
| GET | `/account/fees/record` | Record fee page | backup/web/routers/account.py |
| POST | `/account/fees/record` | Record fee action | backup/web/routers/account.py |
| GET | `/account/payments` | Payments history | backup/web/routers/account.py |
| GET | `/account/reports` | Financial reports | backup/web/routers/account.py |
| GET | `/account/profile` | Account profile | backup/web/routers/account.py |
| GET | `/groups` | Groups list | backup/web/routers/groups.py |
| GET | `/groups/create` | Create group redirect | backup/web/routers/groups.py |
| GET | `/groups/{group_id}` | Group detail | backup/web/routers/groups.py |
| GET | `/groups/{group_id}/posts/create` | Create post form | backup/web/routers/groups.py |
| GET | `/groups/{group_id}/posts` | Group posts redirect | backup/web/routers/groups.py |
| GET | `/groups/{group_id}/edit` | Edit group redirect | backup/web/routers/groups.py |

---

## 2. WebSocket Endpoint

**Target Location:** `modules/web_common/websocket.py`

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| WS | `/ws/chat` | WebSocket chat endpoint | backup/websocket/router.py |

### Implementation Steps

1. **Create WebSocket module:**
   ```
   modules/web_common/
   ├── __init__.py
   ├── websocket.py
   └── connection_manager.py
   ```

2. **Implement WebSocket handler for chat**

3. **Integrate with Chat module from Plan 3**

---

## Implementation Summary

### Endpoints Count

| Category | Endpoints |
|----------|-----------|
| Common Routes | 18 |
| Student Web | 31 |
| Teacher Web | 50 |
| Authority Web | 48 |
| Admin Web | 16 |
| Other (HOD, Exam, Library, Account, Groups) | 44 |
| WebSocket | 1 |
| **Total** | **~208 endpoints** |

---

## Migration Strategy

### Step 1: Create web.py in Each Module
Add web.py files to existing modules for HTML routes

### Step 2: Implement WebSocket
Create WebSocket handler in modules/web_common/

### Step 3: Templates
Reuse existing templates or create new ones

---

## Time Estimate

| Component | Development Time | Testing Time |
|-----------|-----------------|--------------|
| Web Routes | 5-7 days | 2 days |
| WebSocket | 1-2 days | 0.5 day |
| **Total** | **6-9 days** | **2.5 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/web/routers/common.py`
- `backup/web/routers/student.py`
- `backup/web/routers/teacher.py`
- `backup/web/routers/authority.py`
- `backup/web/routers/admin.py`
- `backup/web/routers/hod.py`
- `backup/web/routers/exam_section.py`
- `backup/web/routers/library.py`
- `backup/web/routers/account.py`
- `backup/web/routers/groups.py`
- `backup/websocket/router.py`

---

*Plan created: 2026-03-26*