# Frontend Mapping 1: Auth Module

## Overview
Migration of Authentication module from Jinja templates to React.

## Backend API Source
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
| GET | /api/auth/me | Get current user info |

## Old Jinja Templates (Source)
Location: `backup/templates/auth/`
- login.html
- signup.html
- signup_account.html
- signup_admin.html
- signup_authority.html
- signup_exam_section.html
- signup_hod.html
- signup_library.html
- signup_parent.html
- signup_student.html
- signup_teacher.html

## Frontend Module Structure
```
frontend/src/modules/auth/
├── api/
│   └── auth.js           # API calls (ALREADY EXISTS)
├── pages/
│   ├── LoginPage.jsx     # ✅ ALREADY EXISTS
│   ├── SignupPage.jsx    # ✅ ALREADY EXISTS
│   └── LogoutPage.jsx   # ✅ ALREADY EXISTS (in App.jsx)
└── styles/
    └── auth.css
```

## Frontend Pages to Create

### 1. LoginPage.jsx (ALREADY EXISTS)
**Status:** ✅ Complete
**Features:**
- Email/password form
- Role selector (dropdown)
- Error handling
- Redirects based on role after login

**API Calls:**
```javascript
// Already implemented in api/auth.js
- login(credentials) → POST /api/auth/login-json
- getCurrentUser() → GET /api/auth/me
```

### 2. SignupPage.jsx (ALREADY EXISTS)
**Status:** ✅ Complete
**Features:**
- Multi-step signup form
- Role selection (student, teacher, authority, parent, admin, hod, exam-section, library, account)
- Dynamic form fields based on role
- Validation
- Success redirect to login

**API Calls:**
```javascript
// Already implemented in api/auth.js
- signupStudent(data) → POST /api/auth/signup/student
- signupTeacher(data) → POST /api/auth/signup/teacher
- signupAuthority(data) → POST /api/auth/signup/authority
- signupParent(data) → POST /api/auth/signup/parent
- signupHOD(data) → POST /api/auth/signup/hod
- signupExamSection(data) → POST /api/auth/signup/exam-section
- signupLibrary(data) → POST /api/auth/signup/library
- signupAccount(data) → POST /api/auth/signup/account
```

## Data Schemas

### Login Request
```javascript
{
  username: string,    // email
  password: string
}
```

### Signup Request (Student)
```javascript
{
  email: string,
  password: string,
  first_name: string,
  last_name: string,
  phone: string,
  address: string,
  date_of_birth: string,  // ISO date
  gender: string,
  student_id?: string     // optional
}
```

### User Response
```javascript
{
  id: number,
  email: string,
  first_name: string,
  last_name: string,
  role: string,  // student, teacher, authority, parent, admin, hod, etc.
  is_active: boolean
}
```

## Implementation Checklist
- [x] LoginPage.jsx - Complete
- [x] SignupPage.jsx - Complete  
- [x] auth.js API client - Complete
- [x] Token storage (localStorage) - Complete
- [x] Auth context/useAuth hook - Complete

## Notes
- Auth module is 100% complete
- Uses JWT tokens stored in localStorage
- Role-based redirect after login
