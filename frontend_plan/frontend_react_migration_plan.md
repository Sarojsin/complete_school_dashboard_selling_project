# Frontend Migration Plan: Jinja → React

## Current Status

### Backend Modules (Python/FastAPI)
| Module | Status | Purpose |
|--------|--------|---------|
| `auth` | ✅ Complete | Login, signup, JWT auth |
| `school_student` | ✅ Complete | Student CRUD, dashboard |
| `school_teacher` | ✅ Complete | Teacher CRUD, dashboard |
| `school_parent` | ✅ Complete | Parent management |
| `school_authority` | ✅ Complete | School authority dashboard |
| `school_account_section` | ✅ Complete | Fees, payments |
| `school_library` | ✅ Complete | Books, loans |
| `school_exam_section` | ✅ Complete | Exams, results |
| `school_attendance` | ✅ Complete | Attendance tracking |
| `school_courses` | ✅ Complete | Course management |
| `school_assignments` | ✅ Complete | Assignments |
| `school_tests` | ✅ Complete | Online tests |
| `school_notices` | ✅ Complete | Notices board |
| `school_grades` | ✅ Complete | Grades, assessments |
| `school_notes` | ✅ Complete | Notes sharing |
| `school_videos` | ✅ Complete | Video lessons |
| `school_hod` | ✅ Complete | HOD dashboard |
| `school_groups` | ✅ Complete | Student groups |
| `school_chat` | ✅ Complete | Real-time chat |
| `school_timetable` | ✅ Complete | Timetable |
| `school_dashboard` | ✅ Complete | Role-based dashboards |
| `super_admin` | ✅ Complete | System admin |

### Frontend Modules (React/Vite)
| Module | Status | Pages |
|--------|--------|-------|
| `auth` | ⚠️ Partial | Login only |
| `school_student` | ⚠️ Partial | Dashboard only |
| `school_teacher` | ⚠️ Partial | Dashboard only |
| `school_authority` | ⚠️ Partial | Dashboard only |
| `school_parent` | ❌ Missing | - |
| `school_account_section` | ❌ Missing | - |
| `school_library` | ❌ Missing | - |
| `school_exam_section` | ❌ Missing | - |
| `school_attendance` | ❌ Missing | - |
| `school_courses` | ❌ Missing | - |
| `school_assignments` | ❌ Missing | - |
| `school_tests` | ❌ Missing | - |
| `school_notices` | ❌ Missing | - |
| `school_grades` | ❌ Missing | - |
| `school_notes` | ❌ Missing | - |
| `school_videos` | ❌ Missing | - |
| `school_hod` | ❌ Missing | - |
| `school_groups` | ❌ Missing | - |
| `school_chat` | ❌ Missing | - |
| `school_timetable` | ❌ Missing | - |
| `super_admin` | ⚠️ Partial | Dashboard only |
| `college/*` | ⚠️ Partial | Placement, teacher only |

---

## Migration Priority

### Phase 1: Core Authentication (Week 1)
- [ ] Complete LoginPage with proper error handling
- [ ] Implement Signup pages for all roles
- [ ] Add logout functionality
- [ ] Add token refresh logic
- [ ] Create PrivateRoute component
- [ ] Create AuthLayout (navbar, sidebar)

### Phase 2: Student Portal (Week 1-2)
- [ ] Student Dashboard (already exists, enhance)
- [ ] Student Courses page
- [ ] Student Grades page
- [ ] Student Attendance page
- [ ] Student Assignments page
- [ ] Student Notices page
- [ ] Student Library page
- [ ] Student Tests/Exams page
- [ ] Student Profile page

### Phase 3: Teacher Portal (Week 2-3)
- [ ] Teacher Dashboard (already exists)
- [ ] Teacher Courses page
- [ ] Teacher Students page
- [ ] Teacher Attendance page
- [ ] Teacher Assignments (create/edit)
- [ ] Teacher Tests (create/edit)
- [ ] Teacher Grades input
- [ ] Teacher Notices page
- [ ] Teacher Profile page

### Phase 4: Authority Portal (Week 3-4)
- [ ] Authority Dashboard (already exists)
- [ ] Manage Students
- [ ] Manage Teachers
- [ ] Manage Courses
- [ ] Fees Management
- [ ] Notices Board
- [ ] Reports

### Phase 5: Parent Portal (Week 4)
- [ ] Parent Dashboard
- [ ] Child Attendance
- [ ] Child Grades
- [ ] Child Fees
- [ ] Notices

### Phase 6: Other Modules (Week 5-6)
- [ ] Library
- [ ] Timetable
- [ ] Groups
- [ ] Chat
- [ ] Videos
- [ ] Notes
- [ ] HOD Dashboard
- [ ] Exam Section
- [ ] Account Section

### Phase 7: Super Admin (Week 6-7)
- [ ] Full Super Admin Dashboard
- [ ] User Management
- [ ] Settings
- [ ] Security
- [ ] Backups

---

## Implementation Checklist

### Shared Components to Create
- [ ] `MainLayout.jsx` - Main app layout with sidebar
- [ ] `Sidebar.jsx` - Navigation sidebar
- [ ] `Navbar.jsx` - Top navigation
- [ ] `DataTable.jsx` - Reusable table component
- [ ] `Modal.jsx` - Reusable modal
- [ ] `Button.jsx` - Styled button component
- [ ] `FormInput.jsx` - Reusable form input
- [ ] `Card.jsx` - Card component
- [ ] `Loader.jsx` - Loading spinner
- [ ] `Alert.jsx` - Alert/notification component

### Shared Hooks to Create
- [ ] `useAuth.js` - Auth context and helpers
- [ ] `useApi.js` - API call wrapper
- [ ] `useLocalStorage.js` - Local storage hook

### API Client Enhancement
- [ ] Add response interceptors for auth errors
- [ ] Add request retry logic
- [ ] Add proper TypeScript types

---

## File Structure for Frontend

```
frontend/src/
├── App.jsx                    # Main app with routing
├── main.jsx                   # Entry point
├── index.css                  # Global styles
├── modules/
│   ├── auth/
│   │   ├── api/auth.js        # Auth API calls
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   └── LogoutPage.jsx
│   │   └── styles/auth.css
│   │
│   ├── school/
│   │   ├── school_student/
│   │   │   ├── api/students.js
│   │   │   └── pages/
│   │   │       ├── Dashboard.jsx
│   │   │       ├── Courses.jsx
│   │   │       ├── Grades.jsx
│   │   │       ├── Attendance.jsx
│   │   │       ├── Assignments.jsx
│   │   │       ├── Notices.jsx
│   │   │       ├── Library.jsx
│   │   │       ├── Tests.jsx
│   │   │       └── Profile.jsx
│   │   │
│   │   ├── school_teacher/
│   │   │   ├── api/teachers.js
│   │   │   └── pages/
│   │   │       ├── Dashboard.jsx
│   │   │       ├── Courses.jsx
│   │   │       ├── Students.jsx
│   │   │       ├── Attendance.jsx
│   │   │       ├── Assignments.jsx
│   │   │       ├── Tests.jsx
│   │   │       ├── Grades.jsx
│   │   │       └── Profile.jsx
│   │   │
│   │   ├── school_authority/
│   │   │   ├── api/authority.js
│   │   │   └── pages/
│   │   │       ├── Dashboard.jsx
│   │   │       ├── Students.jsx
│   │   │       ├── Teachers.jsx
│   │   │       ├── Courses.jsx
│   │   │       ├── Fees.jsx
│   │   │       └── Reports.jsx
│   │   │
│   │   ├── school_parent/
│   │   │   ├── api/parents.js
│   │   │   └── pages/
│   │   │       ├── Dashboard.jsx
│   │   │       ├── ChildAttendance.jsx
│   │   │       ├── ChildGrades.jsx
│   │   │       └── ChildFees.jsx
│   │   │
│   │   ├── school_library/
│   │   ├── school_attendance/
│   │   ├── school_courses/
│   │   ├── school_assignments/
│   │   ├── school_tests/
│   │   ├── school_notices/
│   │   ├── school_grades/
│   │   ├── school_notes/
│   │   ├── school_videos/
│   │   ├── school_hod/
│   │   ├── school_groups/
│   │   ├── school_chat/
│   │   ├── school_timetable/
│   │   ├── school_exam_section/
│   │   └── school_account_section/
│   │
│   ├── college/
│   │   ├── college_student/
│   │   ├── college_teacher/
│   │   ├── college_faculty/
│   │   └── ... (other college modules)
│   │
│   └── super_admin/
│       ├── api/superadmin.js
│       └── pages/
│           ├── Dashboard.jsx
│           ├── Users.jsx
│           ├── Settings.jsx
│           └── Security.jsx
│
└── modules/
    └── shared/
        ├── api/client.js      # Axios instance
        ├── components/
        │   ├── Button.jsx
        │   ├── Card.jsx
        │   ├── DataTable.jsx
        │   ├── FormInput.jsx
        │   ├── Loader.jsx
        │   ├── Modal.jsx
        │   ├── Navbar.jsx
        │   ├── Sidebar.jsx
        │   └── Alert.jsx
        ├── hooks/
        │   ├── useApi.js
        │   ├── useAuth.js
        │   └── useLocalStorage.js
        ├── layouts/
        │   ├── AuthLayout.jsx
        │   └── MainLayout.jsx
        └── styles/
            └── global.css
```

---

## API Endpoints Mapping

| Frontend Page | Backend Endpoint |
|---------------|-----------------|
| Student Dashboard | `GET /api/v1/school/dashboard/student` |
| Student Courses | `GET /api/v1/school/courses/student/my` |
| Student Grades | `GET /api/v1/school/grades/my-grades` |
| Student Attendance | `GET /api/v1/school/attendance/student/my` |
| Teacher Courses | `GET /api/v1/school/courses/teacher/my` |
| Teacher Dashboard | `GET /api/v1/school/dashboard/teacher` |
| Authority Students | `GET /api/v1/school/authority/students` |
| Authority Teachers | `GET /api/v1/school/authority/teachers` |
| Library Books | `GET /api/v1/school/library/books` |
| Notices | `GET /api/v1/school/notices` |
| Groups | `GET /api/v1/school/groups` |
| Chat Messages | `GET /api/v1/school/chat/messages` |

---

## Next Steps

1. **Start Phase 1**: Enhance auth module (signup pages, token refresh)
2. **Create shared components**: Layouts, sidebar, navbar
3. **Implement student portal**: Complete all student pages
4. **Implement teacher portal**: Complete all teacher pages
5. **Implement authority portal**: Complete all authority pages
6. **Implement remaining modules**: Following priority list
7. **Add college modules**: When backend college APIs are ready

---

## Notes

- Frontend uses Vite + React + React Router
- API calls go through `/api/v1/*` (configured in vite.config.js proxy)
- JWT token stored in `localStorage.getItem('access_token')`
- Role-based routing with `PrivateRoute` component
- CSS can use plain CSS or integrate Tailwind (if added)
