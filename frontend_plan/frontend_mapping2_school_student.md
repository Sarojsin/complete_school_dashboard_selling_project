# Frontend Mapping 2: School Student Module

## Overview
Migration of Student Portal from Jinja templates to React.

## Backend API Source
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

## Additional Related Endpoints
**Courses:** `/api/courses`
- GET /api/courses/student/my - Student's courses

**Assignments:** `/api/assignments`
- GET /api/assignments/student/my - Student's assignments

**Grades:** `/api/grades`
- GET /api/grades/student/my - Student's grades

**Attendance:** `/api/attendance`
- GET /api/attendance/student/my - Student's attendance

**Fees:** `/api/fees`
- GET /api/fees/student/my - Student's fees

**Notices:** `/api/notices`
- GET /api/notices/student/my - Student's notices

## Old Jinja Templates (Source)
Location: `backup/templates/student/`
- dashboard.html
- profile.html
- courses.html
- grades.html
- attendance.html
- assignments.html
- assignments_detail.html
- notices.html
- fees.html
- library.html
- messages.html
- notes.html
- videos.html
- timetable.html
- exam_results.html
- groups.html
- sidebar.html
- test_list.html
- take_test.html
- test_result.html
- teachers.html

## Frontend Module Structure
```
frontend/src/modules/school/school_student/
├── api/
│   └── students.js       # ✅ ALREADY EXISTS & COMPLETE
├── pages/
│   ├── Dashboard.jsx    # ✅ ALREADY EXISTS
│   ├── Courses.jsx       # ✅ ALREADY EXISTS
│   ├── Grades.jsx       # ✅ ALREADY EXISTS
│   ├── Attendance.jsx   # ✅ ALREADY EXISTS
│   ├── Assignments.jsx  # ✅ ALREADY EXISTS
│   ├── Notices.jsx      # ✅ ALREADY EXISTS
│   ├── Library.jsx      # ❌ MISSING
│   ├── Fees.jsx         # ❌ MISSING
│   ├── Timetable.jsx    # ❌ MISSING
│   ├── Tests.jsx        # ❌ MISSING
│   ├── Videos.jsx       # ❌ MISSING
│   ├── Notes.jsx        # ❌ MISSING
│   ├── Groups.jsx       # ❌ MISSING
│   ├── Profile.jsx      # ❌ MISSING
│   └── Teachers.jsx     # ❌ MISSING
└── styles/
    ├── dashboard.css
    ├── courses.css
    ├── grades.css
    └── attendance.css
```

## Frontend Pages Status

### Completed Pages ✅

#### 1. Dashboard.jsx
**Status:** ✅ Complete
**Features:**
- Welcome message with student name
- Quick stats (courses, assignments, grades summary)
- Recent notices
- Upcoming events

**API Calls:**
```javascript
// frontend/src/modules/school/school_student/api/students.js
- getStudentDashboard() → GET /api/students/dashboard
- getStudentProfile() → GET /api/students/me
```

#### 2. Courses.jsx
**Status:** ✅ Complete
**Features:**
- List of enrolled courses
- Course details (name, code, teacher)
- Click to view course details

**API Calls:**
```javascript
- getMyCourses() → GET /api/students/my-courses
```

#### 3. Grades.jsx
**Status:** ✅ Complete
**Features:**
- List of grades with subject, score, grade
- GPA calculation
- Filter by semester

**API Calls:**
```javascript
- getMyGrades() → GET /api/students/my-grades
```

#### 4. Attendance.jsx
**Status:** ✅ Complete
**Features:**
- Monthly attendance calendar
- Present/Absent/Late status
- Attendance percentage

**API Calls:**
```javascript
- getMyAttendance() → GET /api/students/my-attendance
```

#### 5. Assignments.jsx
**Status:** ✅ Complete
**Features:**
- List of assignments
- Status (pending, submitted, graded)
- Due dates
- Submit assignment form

**API Calls:**
```javascript
- getMyAssignments() → GET /api/students/my-assignments
```

#### 6. Notices.jsx
**Status:** ✅ Complete
**Features:**
- List of notices
- Date, title, content
- Read/unread status

**API Calls:**
```javascript
- getMyNotices() → GET /api/students/my-notices
```

### Missing Pages ❌

#### 7. Library.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List available books
- Search books
- Borrow book functionality
- My borrowed books

**API Calls needed:**
```javascript
// Create in api/students.js
- getLibraryBooks() → GET /api/library/books
- borrowBook(bookId) → POST /api/library/loans
- getMyBorrowedBooks() → GET /api/library/loans/student/{id}
```

#### 8. Fees.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Fee structure display
- Payment history
- Pending fees
- Payment form

**API Calls needed:**
```javascript
// Create in api/students.js
- getMyFees() → GET /api/students/my-fees
- getFeeStructure() → GET /api/fees/structure
```

#### 9. Timetable.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Weekly timetable view
- Day/time grid
- Subject, room, teacher info

**API Calls needed:**
```javascript
- getMyTimetable() → GET /api/students/my-timetable
```

#### 10. Tests.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Available tests list
- Take test interface
- Test results

**API Calls needed:**
```javascript
- getMyTests() → GET /api/students/my-tests
- submitTest(testId, answers) → POST /api/tests/{id}/submit
```

#### 11. Videos.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Video library
- Video player
- Categories

**API Calls needed:**
```javascript
- getMyVideos() → GET /api/students/my-videos
```

#### 12. Notes.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Shared notes list
- Download notes
- Categories

**API Calls needed:**
```javascript
- getMyNotes() → GET /api/students/my-notes
```

#### 13. Groups.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Student groups
- Group posts
- Join group

**API Calls needed:**
```javascript
- getMyGroups() → GET /api/groups/student/my
- joinGroup(code) → POST /api/groups/join
```

#### 14. Profile.jsx
**Status:** ❌ MISSING
**Features to implement:**
- View profile
- Edit profile
- Change password

**API Calls needed:**
```javascript
- getProfile() → GET /api/students/me
- updateProfile(data) → PATCH /api/students/me
```

#### 15. Teachers.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List of teachers
- Teacher contact info

**API Calls needed:**
```javascript
- getTeachers() → GET /api/teachers/
```

## Data Schemas

### Student Profile
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone: string,
  address: string,
  date_of_birth: string,
  gender: string,
  enrollment_date: string,
  profile_pic?: string,
  class_id?: number,
  section_id?: number
}
```

### Course
```javascript
{
  id: number,
  name: string,
  code: string,
  description: string,
  teacher_id: number,
  teacher_name: string,
  credits: number
}
```

### Grade
```javascript
{
  id: number,
  student_id: number,
  subject: string,
  score: number,
  grade: string,
  semester: string,
  academic_year: string
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
  status: "pending" | "submitted" | "graded",
  submitted_at?: string,
  marks_obtained?: number
}
```

## Implementation Order
1. ✅ Dashboard - Complete
2. ✅ Courses - Complete
3. ✅ Grades - Complete
4. ✅ Attendance - Complete
5. ✅ Assignments - Complete
6. ✅ Notices - Complete
7. ❌ Library - Next priority
8. ❌ Fees - Next priority
9. ❌ Timetable - Next priority
10. ❌ Tests - Next priority
11. ❌ Videos - Next priority
12. ❌ Notes - Next priority
13. ❌ Groups - Next priority
14. ❌ Profile - Next priority
15. ❌ Teachers - Next priority

## Notes
- Student module is ~40% complete
- Need to add API functions for missing pages
- Can reuse existing API client structure
