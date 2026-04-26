# Frontend Mapping 4: School Authority Module

## Overview
Migration of Authority Portal from Jinja templates to React.

## Backend API Source
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

## Additional Related Endpoints
**Students:** `/api/students`
- GET /api/students/ - List all students
- POST /api/students/ - Create student
- GET /api/students/{id} - Get student
- PUT /api/students/{id} - Update student
- DELETE /api/students/{id} - Delete student

**Teachers:** `/api/teachers`
- GET /api/teachers/ - List all teachers
- POST /api/teachers/ - Create teacher
- GET /api/teachers/{id} - Get teacher
- PUT /api/teachers/{id} - Update teacher
- DELETE /api/teachers/{id} - Delete teacher

**Courses:** `/api/courses`
- GET /api/courses/ - List all courses
- POST /api/courses/ - Create course
- PUT /api/courses/{id} - Update course
- DELETE /api/courses/{id} - Delete course

**Fees:** `/api/fees`
- GET /api/fees/ - List all fees
- POST /api/fees/ - Create fee record
- PUT /api/fees/{id} - Update fee

**Notices:** `/api/notices`
- GET /api/notices/ - List all notices
- POST /api/notices/ - Create notice

**Departments:** `/api/departments`
- GET /api/departments/ - List departments

## Old Jinja Templates (Source)
Location: `backup/templates/authority/`
- dashboard.html
- students.html
- student_detail.html
- add_student.html
- edit_student.html
- teachers.html
- teacher_detail.html
- add_teacher.html
- edit_teacher.html
- courses.html
- course_detail.html
- add_course.html
- edit_course.html
- fees.html
- add_fee.html
- fee_structure.html
- notices.html
- create_notice.html
- edit_notice.html
- view_notice.html
- groups.html
- create_group.html
- manage_group.html
- departments.html
- analytics_v2.html
- reports.html

## Frontend Module Structure
```
frontend/src/modules/school/school_authority/
├── api/
│   ├── students.js       # ✅ ALREADY EXISTS
│   ├── teachers.js       # ✅ ALREADY EXISTS
│   └── authority.js     # ❌ MISSING
├── pages/
│   ├── Dashboard.jsx    # ✅ ALREADY EXISTS
│   ├── Students.jsx     # ✅ ALREADY EXISTS
│   ├── Teachers.jsx    # ✅ ALREADY EXISTS
│   ├── Courses.jsx     # ✅ ALREADY EXISTS
│   ├── Fees.jsx        # ✅ ALREADY EXISTS
│   ├── Notices.jsx     # ✅ ALREADY EXISTS
│   ├── Reports.jsx     # ✅ ALREADY EXISTS
│   ├── Departments.jsx # ❌ MISSING
│   ├── Groups.jsx      # ❌ MISSING
│   └── Profile.jsx     # ❌ MISSING
└── styles/
    ├── students.css
    ├── teachers.css
    ├── courses.css
    └── fees.css
```

## Frontend Pages Status

### Completed Pages ✅

#### 1. Dashboard.jsx
**Status:** ✅ Complete
**Features:**
- Statistics overview
- Quick links
- Recent activities

**API Calls:**
```javascript
- getAuthorityDashboard() → GET /api/authorities/dashboard
```

#### 2. Students.jsx
**Status:** ✅ Complete
**Features:**
- List all students
- Search/filter students
- Add new student
- Edit student
- Delete student
- View student details

**API Calls:**
```javascript
- getAllStudents() → GET /api/authorities/students
- createStudent(data) → POST /api/students/
- updateStudent(id, data) → PUT /api/students/{id}
- deleteStudent(id) → DELETE /api/students/{id}
```

#### 3. Teachers.jsx
**Status:** ✅ Complete
**Features:**
- List all teachers
- Search/filter teachers
- Add new teacher
- Edit teacher
- Delete teacher
- View teacher details

**API Calls:**
```javascript
- getAllTeachers() → GET /api/authorities/teachers
- createTeacher(data) → POST /api/teachers/
- updateTeacher(id, data) → PUT /api/teachers/{id}
- deleteTeacher(id) → DELETE /api/teachers/{id}
```

#### 4. Courses.jsx
**Status:** ✅ Complete
**Features:**
- List all courses
- Add new course
- Edit course
- Delete course
- Assign teachers

**API Calls:**
```javascript
- getAllCourses() → GET /api/authorities/courses
- createCourse(data) → POST /api/courses/
- updateCourse(id, data) → PUT /api/courses/{id}
- deleteCourse(id) → DELETE /api/courses/{id}
```

#### 5. Fees.jsx
**Status:** ✅ Complete
**Features:**
- Fee records list
- Add fee record
- Edit fee record
- Payment status

**API Calls:**
```javascript
- getAllFees() → GET /api/authorities/fees
- createFee(data) → POST /api/fees/
- updateFee(id, data) → PUT /api/fees/{id}
```

#### 6. Notices.jsx
**Status:** ✅ Complete
**Features:**
- Notice board management
- Create notice
- Edit notice
- Delete notice

**API Calls:**
```javascript
- getAllNotices() → GET /api/authorities/notices
- createNotice(data) → POST /api/notices/
- updateNotice(id, data) → PUT /api/notices/{id}
- deleteNotice(id) → DELETE /api/notices/{id}
```

#### 7. Reports.jsx
**Status:** ✅ Complete
**Features:**
- Generate reports
- Student reports
- Teacher reports
- Finance reports

**API Calls:**
```javascript
- getReports() → GET /api/authorities/reports
- getStudentAnalytics() → GET /api/authorities/analytics/students
- getAttendanceAnalytics() → GET /api/authorities/analytics/attendance
- getPerformanceAnalytics() → GET /api/authorities/analytics/performance
```

### Missing Pages ❌

#### 8. Departments.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List departments
- Add department
- Edit department
- Manage department staff

**API Calls needed:**
```javascript
- getDepartments() → GET /api/departments/
- createDepartment(data) → POST /api/departments/
- updateDepartment(id, data) → PUT /api/departments/{id}
- deleteDepartment(id) → DELETE /api/departments/{id}
```

#### 9. Groups.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Manage student groups
- Create groups
- Assign students to groups

**API Calls needed:**
```javascript
- getGroups() → GET /api/groups/
- createGroup(data) → POST /api/groups/
- updateGroup(id, data) → PUT /api/groups/{id}
- deleteGroup(id) → DELETE /api/groups/{id}
```

#### 10. Profile.jsx
**Status:** ❌ MISSING
**Features to implement:**
- View authority profile
- Edit profile
- Change password

**API Calls needed:**
```javascript
- getProfile() → GET /api/authorities/me
- updateProfile(data) → PATCH /api/authorities/me
```

## Data Schemas

### Student (Authority View)
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone: string,
  class: string,
  section: string,
  roll_number: string,
  enrollment_date: string,
  status: "active" | "inactive" | "graduated"
}
```

### Teacher (Authority View)
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  phone: string,
  designation: string,
  department: string,
  qualification: string,
  join_date: string,
  status: "active" | "inactive"
}
```

### Course
```javascript
{
  id: number,
  name: string,
  code: string,
  description: string,
  credits: number,
  department: string,
  semester: string,
  teacher_id: number,
  teacher_name: string
}
```

### Fee Record
```javascript
{
  id: number,
  student_id: number,
  student_name: string,
  amount: number,
  due_date: string,
  paid_amount: number,
  paid_date?: string,
  status: "paid" | "pending" | "overdue"
}
```

## Implementation Order
1. ✅ Dashboard - Complete
2. ✅ Students - Complete
3. ✅ Teachers - Complete
4. ✅ Courses - Complete
5. ✅ Fees - Complete
6. ✅ Notices - Complete
7. ✅ Reports - Complete
8. ❌ Departments - Next priority
9. ❌ Groups - Next priority
10. ❌ Profile - Next priority

## Notes
- Authority module is ~70% complete
- Most critical pages are done
- Need to complete departments, groups, and profile
