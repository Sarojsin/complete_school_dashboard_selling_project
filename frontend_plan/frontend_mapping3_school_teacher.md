# Frontend Mapping 3: School Teacher Module

## Overview
Migration of Teacher Portal from Jinja templates to React.

## Backend API Source
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

## Additional Related Endpoints
**Courses:** `/api/courses`
- GET /api/courses/teacher/my - Teacher's courses
- POST /api/courses - Create course

**Assignments:** `/api/assignments`
- GET /api/assignments/teacher/my - Teacher's assignments
- POST /api/assignments - Create assignment
- PUT /api/assignments/{id} - Update assignment

**Tests:** `/api/tests`
- GET /api/tests/teacher/my - Teacher's tests
- POST /api/tests - Create test

**Grades:** `/api/grades`
- POST /api/grades - Enter grades

**Attendance:** `/api/attendance`
- GET /api/attendance/teacher/sessions - Teacher's sessions
- POST /api/attendance/sessions - Create attendance session

**Notices:** `/api/notices`
- GET /api/notices/teacher/my - Teacher's notices
- POST /api/notices - Create notice

## Old Jinja Templates (Source)
Location: `backup/templates/teacher/`
- dashboard.html
- profile.html
- courses.html
- course_detail.html
- students.html
- student_detail.html
- student_grades.html
- assignments.html
- create_assignment.html
- edit_assignment.html
- tests.html
- create_test.html
- edit_test.html
- view_tests.html
- grades.html
- add_grade.html
- attendance.html
- take_attendance.html
- view_attendance_session.html
- notices.html
- create_notice.html
- sidebar.html
- timetable.html
- upload_notes.html
- upload_videos.html
- groups.html
- messages.html
- chat.html

## Frontend Module Structure
```
frontend/src/modules/school/school_teacher/
├── api/
│   └── teachers.js       # ✅ ALREADY EXISTS & COMPLETE
├── pages/
│   ├── Dashboard.jsx    # ✅ ALREADY EXISTS
│   ├── Courses.jsx      # ✅ ALREADY EXISTS (with create assignment form)
│   ├── Students.jsx     # ✅ ALREADY EXISTS
│   ├── Assignments.jsx  # ✅ ALREADY EXISTS
│   ├── Profile.jsx      # ❌ MISSING
│   ├── Tests.jsx        # ❌ MISSING
│   ├── Grades.jsx       # ❌ MISSING
│   ├── Attendance.jsx   # ❌ MISSING
│   ├── Notices.jsx      # ❌ MISSING
│   ├── Timetable.jsx    # ❌ MISSING
│   ├── Notes.jsx        # ❌ MISSING
│   ├── Videos.jsx       # ❌ MISSING
│   └── Groups.jsx       # ❌ MISSING
└── styles/
    ├── courses.css
    └── students.css
```

## Frontend Pages Status

### Completed Pages ✅

#### 1. Dashboard.jsx
**Status:** ✅ Complete
**Features:**
- Welcome message with teacher name
- Quick stats (courses, students, pending assignments)
- Recent activities
- Upcoming classes

**API Calls:**
```javascript
// frontend/src/modules/school/school_teacher/api/teachers.js
- getTeacherDashboard() → GET /api/teachers/dashboard
- getTeacherProfile() → GET /api/teachers/me
```

#### 2. Courses.jsx
**Status:** ✅ Complete
**Features:**
- List of teacher's courses
- Add new course form
- View course details
- Course statistics

**API Calls:**
```javascript
- getMyCourses() → GET /api/teachers/my-courses
- createCourse(data) → POST /api/courses
```

#### 3. Students.jsx
**Status:** ✅ Complete
**Features:**
- List of students in teacher's courses
- Student search
- View student details
- Student grades

**API Calls:**
```javascript
- getMyStudents() → GET /api/teachers/my-students
- getStudentDetails(studentId) → GET /api/students/{id}
```

#### 4. Assignments.jsx
**Status:** ✅ Complete
**Features:**
- List of teacher's assignments
- Create new assignment form
- Edit assignment
- View submissions

**API Calls:**
```javascript
- getMyAssignments() → GET /api/teachers/my-assignments
- createAssignment(data) → POST /api/assignments
- updateAssignment(id, data) → PUT /api/assignments/{id}
```

### Missing Pages ❌

#### 5. Profile.jsx
**Status:** ❌ MISSING
**Features to implement:**
- View profile
- Edit profile
- Change password
- Upload profile picture

**API Calls needed:**
```javascript
- getProfile() → GET /api/teachers/me
- updateProfile(data) → PUT /api/teachers/me
```

#### 6. Tests.jsx (Create Test)
**Status:** ❌ MISSING
**Features to implement:**
- List of tests
- Create new test
- Edit test
- Add questions
- View results

**API Calls needed:**
```javascript
- getMyTests() → GET /api/teachers/my-tests
- createTest(data) → POST /api/tests
- updateTest(id, data) → PUT /api/tests/{id}
- getTestQuestions(testId) → GET /api/tests/{id}/questions
- addQuestion(testId, data) → POST /api/tests/{id}/questions
```

#### 7. Grades.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Enter grades for students
- View grade history
- Export grades

**API Calls needed:**
```javascript
- getStudentsForGrading(courseId) → GET /api/grades/course/{id}/students
- submitGrade(data) → POST /api/grades
- updateGrade(id, data) → PUT /api/grades/{id}
```

#### 8. Attendance.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Take attendance for class
- View attendance history
- Attendance reports

**API Calls needed:**
```javascript
- getMySessions() → GET /api/teachers/my-attendance
- createSession(data) → POST /api/attendance/sessions
- markAttendance(sessionId, data) → POST /api/attendance/mark
- getSessionDetails(sessionId) → GET /api/attendance/sessions/{id}
```

#### 9. Notices.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Create notice
- View posted notices
- Edit/Delete notice

**API Calls needed:**
```javascript
- getMyNotices() → GET /api/notices/teacher/my
- createNotice(data) → POST /api/notices
- updateNotice(id, data) → PUT /api/notices/{id}
- deleteNotice(id) → DELETE /api/notices/{id}
```

#### 10. Timetable.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Weekly schedule view
- Class details
- Room assignments

**API Calls needed:**
```javascript
- getMyTimetable() → GET /api/teachers/my-timetable
```

#### 11. Notes.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Upload notes
- Manage notes
- View shared notes

**API Calls needed:**
```javascript
- getMyNotes() → GET /api/notes/teacher/my
- uploadNote(data) → POST /api/notes (multipart/form-data)
- deleteNote(id) → DELETE /api/notes/{id}
```

#### 12. Videos.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Upload videos
- Manage videos
- Video categories

**API Calls needed:**
```javascript
- getMyVideos() → GET /api/videos/teacher/my
- uploadVideo(data) → POST /api/videos (multipart/form-data)
- deleteVideo(id) → DELETE /api/videos/{id}
```

#### 13. Groups.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Manage student groups
- Group posts
- Group materials

**API Calls needed:**
```javascript
- getMyGroups() → GET /api/groups/teacher/my
- createGroup(data) → POST /api/groups
- manageGroupMembers(groupId) → GET /api/groups/{id}/members
```

## Data Schemas

### Teacher Profile
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone: string,
  address: string,
  designation: string,
  department: string,
  qualification: string,
  experience_years: number,
  profile_pic?: string,
  join_date: string
}
```

### Course (Teacher's)
```javascript
{
  id: number,
  name: string,
  code: string,
  description: string,
  credits: number,
  department: string,
  semester: string,
  student_count: number
}
```

### Assignment
```javascript
{
  id: number,
  title: string,
  description: string,
  course_id: number,
  course_name: string,
  due_date: string,
  total_marks: number,
  submissions_count: number,
  status: "draft" | "published"
}
```

### Test
```javascript
{
  id: number,
  title: string,
  course_id: number,
  course_name: string,
  duration_minutes: number,
  total_marks: number,
  questions_count: number,
  scheduled_date: string,
  status: "draft" | "published" | "completed"
}
```

## Implementation Order
1. ✅ Dashboard - Complete
2. ✅ Courses - Complete
3. ✅ Students - Complete
4. ✅ Assignments - Complete
5. ❌ Profile - Next priority
6. ❌ Tests - Next priority
7. ❌ Grades - Next priority
8. ❌ Attendance - Next priority
9. ❌ Notices - Next priority
10. ❌ Timetable - Next priority
11. ❌ Notes - Next priority
12. ❌ Videos - Next priority
13. ❌ Groups - Next priority

## Notes
- Teacher module is ~30% complete
- Need to add API functions for missing pages
- Tests and Grades are critical for teacher workflow
