# Frontend Mapping 8: Other School Modules

## Overview
Migration of remaining school modules from Jinja templates to React.

This covers:
- School Attendance
- School Timetable
- School Groups
- School Chat
- School Notes
- School Videos
- School Exam Section
- School HOD
- School Account Section

---

## Module 1: School Attendance

### Backend API Source
**Prefix:** `/api/attendance`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/attendance/student/my | Get student attendance |
| GET | /api/attendance/teacher/sessions | Teacher's attendance sessions |
| POST | /api/attendance/sessions | Create attendance session |
| POST | /api/attendance/mark | Mark attendance |
| GET | /api/attendance/sessions/{id} | Get session details |

### Frontend Module Structure
```
frontend/src/modules/school/school_attendance/
├── api/
│   └── attendance.js    # ❌ NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── Sessions.jsx     # ❌ MISSING
│   ├── Report.jsx       # ❌ MISSING
│   └── MyAttendance.jsx # ❌ MISSING
└── styles/
    └── attendance.css
```

### Pages to Create
1. Dashboard - Attendance overview
2. Sessions - Manage attendance sessions (Teacher)
3. Report - Attendance reports
4. MyAttendance - View own attendance (Student)

---

## Module 2: School Timetable

### Backend API Source
**Prefix:** `/api/timetable`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/timetable/student/{id} | Get student timetable |
| GET | /api/timetable/teacher/{id} | Get teacher timetable |
| GET | /api/timetable/class/{id} | Get class timetable |
| POST | /api/timetable/ | Create timetable entry |
| PUT | /api/timetable/{id} | Update timetable entry |
| DELETE | /api/timetable/{id} | Delete timetable entry |

### Frontend Module Structure
```
frontend/src/modules/school/school_timetable/
├── api/
│   └── timetable.js    # ❌ NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── MyTimetable.jsx  # ❌ MISSING
│   ├── Manage.jsx       # ❌ MISSING
│   └── TimetableGrid.jsx # ❌ MISSING
└── styles/
    └── timetable.css
```

### Pages to Create
1. Dashboard - Timetable overview
2. MyTimetable - View personal timetable
3. Manage - Manage timetable (Authority)
4. TimetableGrid - Visual timetable grid

---

## Module 3: School Groups

### Backend API Source
**Prefix:** `/api/groups`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/groups/ | List all groups |
| POST | /api/groups/ | Create group |
| GET | /api/groups/{id} | Get group details |
| PUT | /api/groups/{id} | Update group |
| DELETE | /api/groups/{id} | Delete group |
| POST | /api/groups/join | Join group |
| GET | /api/groups/{id}/posts | Get group posts |
| POST | /api/groups/{id}/posts | Create post |

### Old Jinja Templates
Location: `backup/templates/groups/`
- group_list.html
- group_detail.html
- create_group.html
- edit_group.html
- manage_members.html
- group_posts.html
- new_post.html
- view_post.html

### Frontend Module Structure
```
frontend/src/modules/school/school_groups/
├── api/
│   └── groups.js        # ❌ NEED TO CREATE
├── pages/
│   ├── GroupList.jsx    # ❌ MISSING
│   ├── GroupDetail.jsx  # ❌ MISSING
│   ├── CreateGroup.jsx  # ❌ MISSING
│   ├── EditGroup.jsx    # ❌ MISSING
│   ├── ManageMembers.jsx # ❌ MISSING
│   └── GroupPosts.jsx   # ❌ MISSING
└── styles/
    └── groups.css
```

### Pages to Create
1. GroupList - List all groups
2. GroupDetail - View group details
3. CreateGroup - Create new group
4. EditGroup - Edit group
5. ManageMembers - Manage group members
6. GroupPosts - View/create posts

---

## Module 4: School Chat

### Backend API Source
**Prefix:** `/api/chat`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/chat/contacts | Get chat contacts |
| GET | /api/chat/messages/{contact_id} | Get messages |
| POST | /api/chat/messages | Send message |
| WebSocket | /ws/chat | Real-time chat |

### Old Jinja Templates
Location: `backup/templates/` (chat functionality in student/teacher/parent)

### Frontend Module Structure
```
frontend/src/modules/school/school_chat/
├── api/
│   └── chat.js          # ❌ NEED TO CREATE
├── hooks/
│   └── useWebSocket.js  # ❌ NEED TO CREATE
├── pages/
│   ├── ChatList.jsx     # ❌ MISSING
│   ├── ChatWindow.jsx   # ❌ MISSING
│   └── NewChat.jsx      # ❌ MISSING
└── styles/
    └── chat.css
```

### Pages to Create
1. ChatList - List of conversations
2. ChatWindow - Chat message window
3. NewChat - Start new conversation

---

## Module 5: School Notes

### Backend API Source
**Prefix:** `/api/notes`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/notes/ | List notes |
| POST | /api/notes/ | Upload note |
| GET | /api/notes/{id} | Get note |
| PUT | /api/notes/{id} | Update note |
| DELETE | /api/notes/{id} | Delete note |

### Old Jinja Templates
Location: `backup/templates/student/notes.html`
Location: `backup/templates/teacher/upload_notes.html`

### Frontend Module Structure
```
frontend/src/modules/school/school_notes/
├── api/
│   └── notes.js         # ❌ NEED TO CREATE
├── pages/
│   ├── NotesList.jsx    # ❌ MISSING
│   ├── UploadNote.jsx   # ❌ MISSING
│   └── NoteDetail.jsx   # ❌ MISSING
└── styles/
    └── notes.css
```

---

## Module 6: School Videos

### Backend API Source
**Prefix:** `/api/videos`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/videos/ | List videos |
| POST | /api/videos/ | Upload video |
| GET | /api/videos/{id} | Get video |
| DELETE | /api/videos/{id} | Delete video |

### Old Jinja Templates
Location: `backup/templates/student/videos.html`
Location: `backup/templates/teacher/upload_videos.html`

### Frontend Module Structure
```
frontend/src/modules/school/school_videos/
├── api/
│   └── videos.js        # ❌ NEED TO CREATE
├── pages/
│   ├── VideoList.jsx    # ❌ MISSING
│   ├── UploadVideo.jsx  # ❌ MISSING
│   └── VideoPlayer.jsx  # ❌ MISSING
└── styles/
    └── videos.css
```

---

## Module 7: School Exam Section

### Backend API Source
**Prefix:** `/api/exams`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/exams | Create exam |
| GET | /api/exams/{exam_id} | Get exam |
| GET | /api/exams | List exams |
| PUT | /api/exams/{exam_id} | Update exam |
| DELETE | /api/exams/{exam_id} | Delete exam |
| POST | /api/exams/grades | Create grade |
| GET | /api/exams/grades | List grades |

### Old Jinja Templates
Location: `backup/templates/exam_section/`
- dashboard.html
- post_result.html
- results.html
- grade_sheet.html
- notices.html

### Frontend Module Structure
```
frontend/src/modules/school/school_exam_section/
├── api/
│   └── exams.js         # ❌ NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── CreateExam.jsx   # ❌ MISSING
│   ├── PostResult.jsx   # ❌ MISSING
│   ├── Results.jsx      # ❌ MISSING
│   ├── GradeSheet.jsx   # ❌ MISSING
│   └── Notices.jsx      # ❌ MISSING
└── styles/
    └── exam_section.css
```

---

## Module 8: School HOD

### Backend API Source
**Prefix:** `/api/hod`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/hod/dashboard | Get HOD dashboard |
| GET | /api/hod/department | Get department info |
| GET | /api/hod/teachers | List department teachers |
| GET | /api/hod/students | List department students |
| GET | /api/hod/reports | Get department reports |

### Old Jinja Templates
Location: `backup/templates/hod/`
- dashboard.html
- teachers.html
- students.html
- reports.html
- student_performance.html

### Frontend Module Structure
```
frontend/src/modules/school/school_hod/
├── api/
│   └── hod.js           # ❌ NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── Teachers.jsx     # ❌ MISSING
│   ├── Students.jsx     # ❌ MISSING
│   ├── Reports.jsx      # ❌ MISSING
│   └── Performance.jsx  # ❌ MISSING
└── styles/
    └── hod.css
```

---

## Module 9: School Account Section

### Backend API Source
**Prefix:** `/api/account`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/account/dashboard | Get account dashboard |
| GET | /api/account/fees | List all fees |
| POST | /api/account/fees | Create fee |
| PUT | /api/account/fees/{id} | Update fee |
| GET | /api/account/payments | List payments |
| POST | /api/account/payments | Record payment |
| GET | /api/account/summary | Get financial summary |

### Old Jinja Templates
Location: `backup/templates/account/`
- dashboard.html
- record_teacher_payment.html

### Frontend Module Structure
```
frontend/src/modules/school/school_account_section/
├── api/
│   └── account.js       # ❌ NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── Fees.jsx         # ❌ MISSING
│   ├── Payments.jsx     # ❌ MISSING
│   ├── Summary.jsx      # ❌ MISSING
│   └── TeacherPayments.jsx # ❌ MISSING
└── styles/
    └── account.css
```

---

## Summary of All Modules

| # | Module | Status | Pages to Create |
|---|--------|--------|----------------|
| 1 | Auth | ✅ Complete | 2 |
| 2 | School Student | ⚠️ Partial | 9 |
| 3 | School Teacher | ⚠️ Partial | 9 |
| 4 | School Authority | ⚠️ Partial | 3 |
| 5 | School Parent | ❌ Missing | 7 |
| 6 | School Library | ❌ Missing | 7 |
| 7 | Super Admin | ⚠️ Partial | 12 |
| 8 | School Attendance | ❌ Missing | 4 |
| 9 | School Timetable | ❌ Missing | 4 |
| 10 | School Groups | ❌ Missing | 6 |
| 11 | School Chat | ❌ Missing | 3 |
| 12 | School Notes | ❌ Missing | 3 |
| 13 | School Videos | ❌ Missing | 3 |
| 14 | School Exam Section | ❌ Missing | 6 |
| 15 | School HOD | ❌ Missing | 5 |
| 16 | School Account Section | ❌ Missing | 5 |

**Total Pages to Create: ~90 pages**

## Implementation Priority
1. Parent Portal (high impact)
2. Library (high impact)
3. Super Admin (system critical)
4. Groups (student engagement)
5. Chat (communication)
6. Exam Section (academic critical)
7. HOD (departmental management)
8. Account Section (financial)
9. Attendance
10. Timetable
11. Notes
12. Videos
