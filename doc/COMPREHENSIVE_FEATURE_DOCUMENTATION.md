# School Management System - Complete Feature Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [User Roles & Permissions](#user-roles--permissions)
4. [Database Architecture](#database-architecture)
5. [Feature Modules](#feature-modules)
6. [API Endpoints](#api-endpoints)
7. [Web Routes](#web-routes)
8. [Service Layer Logic](#service-layer-logic)
9. [Authentication & Security](#authentication--security)
10. [File Upload System](#file-upload-system)
11. [Real-time Features](#real-time-features)
12. [Extending the System](#extending-the-system)

---

## 1. Project Overview

This is a **modular, production-ready School Management System** built with **FastAPI** (Python). It provides a complete solution for managing students, teachers, courses, attendance, grades, fees, library, exams, and communication within an educational institution.

### Architecture Pattern: Repository Pattern with Service Layer

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌─────────────────────┐    ┌──────────────────────────┐  │
│  │   Web Routers       │    │   API Endpoints          │  │
│  │   (HTML Templates)  │    │   (JSON API)             │  │
│  └─────────────────────┘    └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   Business Logic, Validation, Data Transformation    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   REPOSITORY LAYER                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   Data Access, Database Queries, CRUD Operations     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   SQLAlchemy ORM Models (Database Tables)          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI |
| **Database** | SQLite (development) / PostgreSQL (production) |
| **ORM** | SQLAlchemy (Async) |
| **Authentication** | JWT (JSON Web Tokens) |
| **Frontend** | Jinja2 Templates + Bootstrap |
| **WebSocket** | Starlette WebSocket |
| **Scheduler** | APScheduler |
| **Security** | bcrypt, CSRF Protection |

---

## 3. User Roles & Permissions

The system defines the following user roles in [`app/models/models.py:7-17`](app/models/models.py:7):

```python
class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    AUTHORITY = "AUTHORITY"
    PARENT = "PARENT"
    HOD = "HOD"
    EXAM_SECTION = "EXAM_SECTION"
    LIBRARY_MANAGER = "LIBRARY_MANAGER"
    ACCOUNT_SECTION = "ACCOUNT_SECTION"
    GROUP_CREATOR = "GROUP_CREATOR"
```

### Role-Based Access Control (RBAC)

Access control is implemented in [`app/dependencies/auth.py`](app/dependencies/auth.py):

| Dependency | Purpose | Usage |
|------------|---------|-------|
| `get_current_user` | Basic authentication | Most routes |
| `get_current_student` | Student-only access | Student-specific routes |
| `get_current_teacher` | Teacher-only access | Teacher-specific routes |
| `get_current_authority` | Authority-only access | Admin routes |
| `get_current_parent` | Parent-only access | Parent-specific routes |
| `get_current_teacher_or_authority` | Teacher or Authority | Shared routes |

### How to Create a New Role

1. **Add to Enum** - Update `UserRole` in [`app/models/models.py:7`](app/models/models.py:7)
2. **Create Profile Model** - Add profile table if needed (e.g., `HOD`, `LIBRARY_MANAGER` use `Authority`)
3. **Add Dependency** - Create new dependency in [`app/dependencies/auth.py`](app/dependencies/auth.py)
4. **Create Web Router** - Add new router in `app/web/routers/`
5. **Create Service** - Add business logic in `app/services/`

---

## 4. Database Architecture

### Core Models

#### User Model ([`app/models/models.py:20-40`](app/models/models.py:20))
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    profile_picture = Column(String(255))
    role = Column(SQLEnum(UserRole))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

**Relationships:**
- One-to-One with: `Student`, `Teacher`, `Authority`, `Parent`
- Used in: `Message`, `ChatMessage`, `GroupPost`, `TeacherPayment`

#### Student Model ([`app/models/models.py:41-75`](app/models/models.py:41))
```python
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(String(50), unique=True)  # Roll number
    full_name = Column(String(255))
    date_of_birth = Column(Date)
    phone = Column(String(20))
    address = Column(Text)
    parent_name = Column(String(255))
    parent_phone = Column(String(20))
    parent_id = Column(Integer, ForeignKey("parents.id"))
    enrollment_date = Column(Date)
    grade_level = Column(String(20))  # Class (e.g., "10", "11")
    section = Column(String(10))      # Section (e.g., "A", "B")
    department_id = Column(Integer, ForeignKey("departments.id"))
```

**Relationships:**
- Many-to-One: `User`, `Parent`, `Department`
- One-to-Many: `CourseEnrollment`, `AssignmentSubmission`, `Attendance`, `Grade`, `FeeRecord`, `TestSubmission`, `BookLoan`

#### Teacher Model ([`app/models/models.py:77-106`](app/models/models.py:77))
```python
class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String(50), unique=True)
    full_name = Column(String(255))
    phone = Column(String(20))
    department = Column(String(100))
    qualification = Column(String(255))
    specialization = Column(String(255))
    joining_date = Column(Date)
    status = Column(String(20))  # active, inactive, on_leave, retired
    department_id = Column(Integer, ForeignKey("departments.id"))
```

**Relationships:**
- One-to-Many: `Course`, `Assignment`, `Test`, `Note`, `Video`, `Notice`, `TeacherPayment`

#### Course Model ([`app/models/models.py:139-162`](app/models/models.py:139))
```python
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    course_code = Column(String(50), unique=True)
    course_name = Column(String(255))
    description = Column(Text)
    credits = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    grade_level = Column(String(20))
    semester = Column(String(20))
    created_at = Column(DateTime)
```

**Relationships:**
- Many-to-One: `Teacher`
- One-to-Many: `CourseEnrollment`, `Assignment`, `Attendance`, `Grade`, `Note`, `Video`, `Schedule`

#### CourseEnrollment Model ([`app/models/models.py:163-174`](app/models/models.py:163))
Links students to courses (Many-to-Many relationship between Student and Course).

---

## 5. Feature Modules

### 5.1 Authentication System

**Features:**
- User Registration (with role-based signup)
- Login with JWT tokens
- Token refresh mechanism
- Session management via cookies
- Password hashing with bcrypt

**Files:**
- [`app/api/endpoints/auth.py`](app/api/endpoints/auth.py) - API routes
- [`app/services/auth_service.py`](app/services/auth_service.py) - Token generation/verification
- [`app/repositories/user_repository.py`](app/repositories/user_repository.py) - User data access

**How It Works:**

1. **Login Flow:**
   ```python
   # app/api/endpoints/auth.py:15-60
   @router.post("/login")
   async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
       # 1. Authenticate user
       user = await UserRepository.authenticate(db, username, password)
       
       # 2. Generate tokens
       tokens = AuthService.create_token_for_user(user)
       
       # 3. Set cookies and return response
       response.set_cookie(key="access_token", value=f"Bearer {access_token}")
       response.set_cookie(key="refresh_token", value=refresh_token)
   ```

2. **Token Structure:**
   ```python
   # app/services/auth_service.py:21-36
   {
       "access_token": "eyJ...",      # Expires in 15 minutes
       "refresh_token": "eyJ...",      # Expires in 7 days
       "token_type": "bearer"
   }
   ```

3. **Signup Options:**
   - `/api/auth/signup/student` - Student self-registration
   - `/api/auth/signup/teacher` - Teacher registration
   - `/api/auth/signup/authority` - Authority (requires secret key)
   - `/api/auth/signup/parent` - Parent (links to existing student)
   - `/api/auth/signup/hod` - Head of Department
   - `/api/auth/signup/exam-section` - Exam Section (requires secret key)
   - `/api/auth/signup/library` - Library Manager (requires secret key)
   - `/api/auth/signup/account` - Account Section (requires secret key)

**How to Modify:**
- To change token expiry: Edit `ACCESS_TOKEN_EXPIRE_MINUTES` or `REFRESH_TOKEN_EXPIRE_DAYS` in [`app/core/config.py`](app/core/config.py)
- To add new signup: Copy existing signup endpoint and modify role

---

### 5.2 Student Management

**Features:**
- View dashboard with stats, assignments, grades, attendance
- View and update profile
- View enrolled courses
- Submit assignments
- Take online tests
- View grades and attendance
- View notices
- Access study materials (notes, videos)
- Fee payment tracking
- Library book borrowing

**Files:**
- [`app/web/routers/student.py`](app/web/routers/student.py) - Web routes
- [`app/services/student_service.py`](app/services/student_service.py) - Business logic
- [`app/repositories/student_repository.py`](app/repositories/student_repository.py) - Data access

**Dashboard Data Structure** ([`app/services/student_service.py:17-165`](app/services/student_service.py:17)):
```python
{
    "student": Student object,
    "courses": [Course, ...],
    "assignments": [Assignment, ...],  # Upcoming deadlines
    "recent_grades": [{"course": str, "score": float, ...}, ...],
    "attendance_overview": [{"course_name": str, "percentage": float}, ...],
    "attendance_grid": [...],  # Weekly attendance grid
    "days_labels": [...],      # Day labels for grid
    "stats": {
        "gpa": "3.80",
        "attendance": "94%",
        "courses_count": 5,
        "pending_assignments": 3
    },
    "latest_notice": Notice object,
    "library_stats": {
        "total_borrowed": 5,
        "currently_borrowed": 2,
        "overdue": 0
    }
}
```

**Key Routes:**
| Route | Function | Description |
|-------|----------|-------------|
| `/student/dashboard` | `student_dashboard()` | Main dashboard |
| `/student/profile` | `student_profile()` | View/edit profile |
| `/student/courses` | `student_courses()` | List enrolled courses |
| `/student/assignments` | `student_assignments()` | List assignments with filters |
| `/student/assignments/{id}` | `student_assignment_detail()` | Assignment details |
| `/student/tests` | `student_test_list()` | Available tests |
| `/student/tests/{id}/start` | `student_take_test()` | Take a test |
| `/student/fees` | `student_fees()` | Fee payment |
| `/student/notices` | `student_notices()` | School notices |
| `/student/grades` | `student_grades()` | View grades |
| `/student/attendance` | `student_attendance()` | Attendance record |

---

### 5.3 Teacher Management

**Features:**
- Dashboard with course overview
- Manage courses (create, edit)
- Create and manage assignments
- Create and manage tests/quizzes
- Take attendance
- Upload notes and videos
- Grade submissions
- View student performance
- Create notices

**Files:**
- [`app/web/routers/teacher.py`](app/web/routers/teacher.py) - Web routes
- [`app/services/teacher_service.py`](app/services/teacher_service.py) - Business logic
- [`app/repositories/teacher_repository.py`](app/repositories/teacher_repository.py) - Data access

**Key Routes:**
| Route | Function |
|-------|----------|
| `/teacher/dashboard` | `teacher_dashboard()` |
| `/teacher/courses` | `teacher_courses()` |
| `/teacher/courses/{id}` | `course_detail()` |
| `/teacher/assignments` | `teacher_assignments()` |
| `/teacher/assignments/create` | `create_assignment()` |
| `/teacher/attendance` | `teacher_attendance()` |
| `/teacher/attendance/take` | `take_attendance()` |
| `/teacher/grades` | `teacher_grades()` |
| `/teacher/students` | `teacher_students()` |
| `/teacher/tests` | `teacher_tests()` |
| `/teacher/upload/notes` | `upload_notes()` |
| `/teacher/upload/videos` | `upload_videos()` |

---

### 5.4 Authority/Admin Management

**Features:**
- Manage students (add, edit, delete)
- Manage teachers (add, edit, delete)
- Manage courses
- Manage fee structures
- View reports and analytics
- Create notices
- Manage groups

**Files:**
- [`app/web/routers/authority.py`](app/web/routers/authority.py) - Web routes
- [`app/services/authority_service.py`](app/services/authority_service.py) - Business logic

---

### 5.5 Attendance System

**Features:**
- Teachers take attendance for their courses
- Students can view their attendance
- Automatic calculation of attendance percentage
- Weekly attendance grid view

**Models:**
- [`app/models/models.py:211-225`](app/models/models.py:211) - `Attendance` model

```python
class Attendance(Base):
    student_id = Column(Integer, ForeignKey)
    course_id = Column(Integer, ForeignKey)
    date = Column(Date)
    status = Column(String(20))  # present, absent, late
    arrival_time = Column(Time)
    remarks = Column(Text)
```

**How Attendance Works:**
1. Teacher navigates to `/teacher/attendance/take`
2. Selects course and date
3. System fetches enrolled students
4. Teacher marks each student as present/absent/late
5. Data is saved to `Attendance` table
6. Students can view their attendance at `/student/attendance`

**Attendance Calculation** ([`app/services/student_service.py:76-111`](app/services/student_service.py:76)):
```python
# Calculate overall attendance
overall_attendance = (total_present / total_expected * 100) if total_expected > 0 else 100

# Per-course attendance
stats = await AttendanceRepository.get_attendance_stats(db, student.id, course.id)
# Returns: {present: int, absent: int, late: int, total: int, percentage: float}
```

---

### 5.6 Assignment & Submission System

**Features:**
- Teachers create assignments with due dates
- Students submit assignments (text or file)
- Teachers grade submissions
- Status tracking (pending, submitted, graded, overdue)

**Models:**
- [`app/models/models.py:175-210`](app/models/models.py:175)

```python
class Assignment(Base):
    title = Column(String(255))
    description = Column(Text)
    course_id = Column(Integer, ForeignKey)
    teacher_id = Column(Integer, ForeignKey)
    due_date = Column(DateTime)
    max_score = Column(Float)
    file_path = Column(String(500))
    target_classes = Column(String(255))  # "9A,9B" - comma-separated

class AssignmentSubmission(Base):
    assignment_id = Column(Integer, ForeignKey)
    student_id = Column(Integer, ForeignKey)
    submission_text = Column(Text)
    file_path = Column(String(500))
    submitted_at = Column(DateTime)
    score = Column(Float)
    feedback = Column(Text)
    graded_at = Column(DateTime)
```

**Workflow:**
1. Teacher creates assignment at `/teacher/assignments/create`
2. System saves to `Assignment` table
3. Student sees assignment at `/student/assignments`
4. Student submits at `/student/assignments/{id}/submit`
5. Submission saved to `AssignmentSubmission`
6. Teacher grades at `/teacher/view_submissions/{id}`
7. Grade saved to submission record

**Target Classes Feature:**
The `target_classes` field allows teachers to specify which classes can see the assignment:
- Format: `"9A,9B,10A"` (comma-separated)
- Query filter in [`app/repositories/assignment_repository.py`](app/repositories/assignment_repository.py)

---

### 5.7 Online Testing System

**Features:**
- Create tests with multiple question types
- MCQ, True/False, Short Answer, Essay
- Timed tests
- Auto-grading for objective questions
- Section/grade-level targeting
- Performance analytics

**Models:**
- [`app/models/test_models.py`](app/models/test_models.py)

```python
class QuestionType(str, enum.Enum):
    MCQ = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"

class Test(Base):
    title = Column(String(255))
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # minutes
    total_points = Column(Float)
    target_section = Column(String(50))
    is_active = Column(Boolean)

class TestQuestion(Base):
    test_id = Column(Integer, ForeignKey)
    question_text = Column(Text)
    question_type = Column(SQLEnum(QuestionType))
    options = Column(JSON)  # ["Option A", "Option B", ...]
    correct_answer = Column(Text)
    points = Column(Float)
    explanation = Column(Text)
    order = Column(Integer)

class TestSubmission(Base):
    test_id = Column(Integer, ForeignKey)
    student_id = Column(Integer, ForeignKey)
    answers = Column(JSON)  # {question_id: answer}
    score = Column(Float)
    max_score = Column(Float)
    percentage = Column(Float)
    started_at = Column(DateTime)
    submitted_at = Column(DateTime)
    time_taken = Column(Integer)  # seconds
    is_graded = Column(Boolean)
    feedback = Column(Text)
```

**Test Flow:**
1. Teacher creates test at `/teacher/create_test`
2. Adds questions (MCQ, True/False, etc.)
3. Sets time window and duration
4. Student sees available tests at `/student/tests`
5. Student starts test at `/student/tests/{id}/start`
6. System creates `TestSubmission` with `started_at`
7. Student answers questions within time limit
8. Student submits at `/student/tests/{id}/submit`
9. Auto-grading happens in [`app/services/test_service.py`](app/services/test_service.py)
10. Student views results at `/student/tests/{id}/result`

**Auto-Grading Logic** ([`app/services/test_service.py`](app/services/test_service.py)):
```python
# For each answer:
if question.question_type == QuestionType.MCQ:
    is_correct = (user_answer.strip().lower() == 
                  question.correct_answer.strip().lower())
elif question.question_type == QuestionType.TRUE_FALSE:
    is_correct = (user_answer.strip().lower() == 
                 question.correct_answer.strip().lower())
# Essay and Short Answer are not auto-graded
```

---

### 5.8 Grade Management

**Features:**
- Teachers add grades for students
- Multiple grade types (midterm, final, quiz, assignment)
- GPA calculation
- Grade sheets and reports

**Models:**
- [`app/models/models.py:245-261`](app/models/models.py:245)

```python
class Grade(Base):
    student_id = Column(Integer, ForeignKey)
    course_id = Column(Integer, ForeignKey)
    grade_type = Column(String(50))  # midterm, final, quiz, assignment
    score = Column(Float)
    max_score = Column(Float)
    grade = Column(String(5))  # A, B+, B, C, etc.
    remarks = Column(Text)
    date = Column(Date)
```

**GPA Calculation** ([`app/repositories/grade_repository.py`](app/repositories/grade_repository.py)):
```python
# Typical GPA calculation:
# A = 4.0, A- = 3.7, B+ = 3.3, B = 3.0, B- = 2.7, C+ = 2.3, C = 2.0, etc.
# GPA = Sum(grade_points * credits) / Sum(credits)
```

---

### 5.9 Fee Management

**Features:**
- Fee structure by grade level
- Fee records per student
- Payment tracking
- Fee status (pending, paid, overdue, partial)
- Payment history

**Models:**
- [`app/models/models.py:226-319`](app/models/models.py:226) - `FeeStructure` and `FeeRecord`

```python
class FeeStructure(Base):
    grade_level = Column(String(20))
    academic_year = Column(String(20))
    tuition_fee = Column(Float)
    registration_fee = Column(Float)
    library_fee = Column(Float)
    sports_fee = Column(Float)
    lab_fee = Column(Float)
    activity_fee = Column(Float)
    other_charges = Column(Float)
    total_amount = Column(Float)
    due_date = Column(Date)

class FeeRecord(Base):
    student_id = Column(Integer, ForeignKey)
    fee_type = Column(String(100))  # tuition, library, sports
    amount = Column(Float)
    due_date = Column(Date)
    paid_amount = Column(Float)
    payment_date = Column(Date)
    status = Column(String(20))  # pending, paid, overdue, partial
```

**Fee Workflow:**
1. Authority creates fee structure at `/authority/fee-structure`
2. System generates fee records for all students
3. Students view fees at `/student/fees`
4. (Future) Online payment integration
5. Authority records payment at `/authority/fees`
6. System updates status automatically

**Fee Status Logic** ([`app/repositories/fee_repository.py:66-78`](app/repositories/fee_repository.py:66)):
```python
# Auto-update status based on payment
if fee.paid_amount >= fee.amount:
    fee.status = 'paid'
elif fee.paid_amount > 0:
    fee.status = 'partial'
else:
    fee.status = 'pending'

# Check overdue
if fee.status != 'paid' and fee.due_date < date.today():
    fee.status = 'overdue'
```

---

### 5.10 Library Management

**Features:**
- Add books to library
- Issue books to students
- Return books
- Track overdue books
- Calculate fines

**Models:**
- [`app/models/library_models.py`](app/models/library_models.py)

```python
class Book(Base):
    title = Column(String(255))
    author = Column(String(255))
    isbn = Column(String(20), unique=True)
    category = Column(String(100))
    total_copies = Column(Integer)
    available_copies = Column(Integer)

class BookLoan(Base):
    student_id = Column(Integer, ForeignKey)
    book_id = Column(Integer, ForeignKey)
    book_title = Column(String)
    book_author = Column(String)
    taken_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date)
    status = Column(String)  # borrowed, returned, overdue
    fine_amount = Column(Integer)
```

**Library Workflow:**
1. Library Manager adds books at `/library/add-book`
2. Student borrows book at `/library/issue-book`
3. System creates `BookLoan` with due date (typically 14 days)
4. Student returns at `/library/return-book`
5. If overdue, fine is calculated
6. Student can view borrowed books at `/student/library`

---

### 5.11 Notice Management

**Features:**
- Create notices (Authority, Teacher)
- Target specific roles/grades
- Priority levels (low, normal, high, urgent)
- Expiration dates
- File attachments

**Models:**
- [`app/models/models.py:319-337`](app/models/models.py:319)

```python
class Notice(Base):
    title = Column(String(255))
    content = Column(Text)
    authority_id = Column(Integer, ForeignKey)
    teacher_id = Column(Integer, ForeignKey)
    target_role = Column(String(20))  # all, student, teacher
    target_grade = Column(String(50))
    priority = Column(String(20))  # low, normal, high, urgent
    file_path = Column(String(500))
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
```

---

### 5.12 Course Management

**Features:**
- Create courses with details
- Assign teachers
- Enroll students
- Set schedules
- Course materials (notes, videos)

**Models:**
- [`app/models/models.py:139-174`](app/models/models.py:139) - Course, CourseEnrollment

**Enrollment Flow:**
1. Authority creates course at `/authority/add-course`
2. Authority assigns teacher
3. Students enroll (or are auto-enrolled)
4. Enrollment saved to `CourseEnrollment`

---

### 5.13 Group & Forum System

**Features:**
- Create groups (class groups, study groups)
- Unique join codes
- Group posts (notices, notes, links)
- Member management

**Models:**
- [`app/models/group_models.py`](app/models/group_models.py)

```python
class Group(Base):
    name = Column(String(255))
    description = Column(Text)
    code = Column(String(50), unique=True)  # Join code
    created_by = Column(Integer, ForeignKey)
    is_active = Column(Boolean)

class GroupMember(Base):
    group_id = Column(Integer, ForeignKey)
    user_id = Column(Integer, ForeignKey)
    role = Column(String(50))  # teacher, student
    is_active = Column(Boolean)

class GroupPost(Base):
    group_id = Column(Integer, ForeignKey)
    author_id = Column(Integer, ForeignKey)
    title = Column(String(255))
    content = Column(Text)
    post_type = Column(String(50))  # notice, note, link
    link_url = Column(String(500))
    is_published = Column(Boolean)
```

---

### 5.14 Chat & Messaging System

**Features:**
- Direct messaging between users
- File attachments
- Read status tracking
- Message expiration (auto-cleanup)
- Real-time WebSocket chat

**Models:**
- [`app/models/chat_models.py`](app/models/chat_models.py)

```python
class ChatMessage(Base):
    sender_id = Column(Integer, ForeignKey)
    receiver_id = Column(Integer, ForeignKey)
    content = Column(Text)
    file_path = Column(String(500))
    file_name = Column(String(255))
    file_type = Column(String(50))
    is_read = Column(Boolean)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)  # Auto-cleanup
```

**Auto-Cleanup** ([`app/services/chat_cleanup_service.py`](app/services/chat_cleanup_service.py)):
```python
# Runs every hour via APScheduler
# Deletes messages older than MESSAGE_RETENTION_DAYS (default: 30)
```

---

### 5.15 Exam Section

**Features:**
- Manage exam schedules
- Publish results
- Create exam notices
- Grade sheets

**Files:**
- [`app/api/endpoints/exam_section.py`](app/api/endpoints/exam_section.py)
- [`app/web/routers/exam_section.py`](app/web/routers/exam_section.py)

---

### 5.16 Parent Portal

**Features:**
- View child's attendance
- View child's grades
- View child's homework/assignments
- View school notices
- Chat with teachers

**Files:**
- [`app/web/routers/parent.py`](app/web/routers/parent.py)

---

### 5.17 HOD (Head of Department)

**Features:**
- Department overview
- View teachers in department
- View students in department
- Department reports

**Files:**
- [`app/web/routers/hod.py`](app/web/routers/hod.py)

---

### 5.18 Account Section

**Features:**
- Teacher salary management
- Payment records
- Financial reports

**Files:**
- [`app/web/routers/account.py`](app/web/routers/account.py)

**Models:**
- [`app/models/account_models.py`](app/models/account_models.py)

```python
class TeacherPayment(Base):
    teacher_id = Column(Integer, ForeignKey)
    amount = Column(Float)
    month = Column(String(7))  # YYYY-MM
    payment_type = Column(String)  # salary, bonus, allowance
    paid_by = Column(Integer, ForeignKey)
    notes = Column(String)
```

---

## 6. API Endpoints

### Authentication API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login with username/password |
| POST | `/api/auth/login-json` | Login with JSON body |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/signup/student` | Register student |
| POST | `/api/auth/signup/teacher` | Register teacher |
| POST | `/api/auth/signup/authority` | Register authority |
| POST | `/api/auth/signup/parent` | Register parent |
| POST | `/api/auth/signup/hod` | Register HOD |
| POST | `/api/auth/signup/exam-section` | Register exam section |
| POST | `/api/auth/signup/library` | Register library |
| POST | `/api/auth/signup/account` | Register account |

### Students API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | List all students |
| GET | `/api/students/{id}` | Get student details |
| POST | `/api/students` | Create student |
| PUT | `/api/students/{id}` | Update student |
| DELETE | `/api/students/{id}` | Delete student |

### Teachers API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teachers` | List all teachers |
| GET | `/api/teachers/{id}` | Get teacher details |

### Courses API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/{id}` | Get course details |
| POST | `/api/courses` | Create course |
| POST | `/api/courses/{id}/enroll` | Enroll student |

### Assignments API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/assignments` | List assignments |
| POST | `/api/assignments` | Create assignment |
| POST | `/api/assignments/{id}/submit` | Submit assignment |

### Attendance API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/attendance` | Get attendance records |
| POST | `/api/attendance` | Mark attendance |

### Grades API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/grades` | Get grades |
| POST | `/api/grades` | Add grade |

### Fees API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/fees` | Get fee records |
| POST | `/api/fees` | Create fee record |
| PUT | `/api/fees/{id}` | Update fee |

### Other APIs

| Module | Endpoints |
|--------|-----------|
| Notices | `/api/notices/*` |
| Notes | `/api/notes/*` |
| Videos | `/api/videos/*` |
| Chat | `/api/chat/*` |
| Groups | `/api/groups/*` |
| Tests | `/api/tests/*` |

---

## 7. Web Routes

### Route Prefixes by Role

| Role | Prefix | File |
|------|--------|------|
| Common | `/` | `app/web/routers/common.py` |
| Student | `/student/*` | `app/web/routers/student.py` |
| Teacher | `/teacher/*` | `app/web/routers/teacher.py` |
| Parent | `/parent/*` | `app/web/routers/parent.py` |
| Authority | `/authority/*` | `app/web/routers/authority.py` |
| HOD | `/hod/*` | `app/web/routers/hod.py` |
| Exam Section | `/exam-section/*` | `app/web/routers/exam_section.py` |
| Library | `/library/*` | `app/web/routers/library.py` |
| Account | `/account/*` | `app/web/routers/account.py` |
| Groups | `/groups/*` | `app/web/routers/groups.py` |

---

## 8. Service Layer Logic

Services contain business logic and data transformation. They sit between the routers (controllers) and repositories (data access).

### Key Services

| Service | Purpose |
|---------|---------|
| [`app/services/auth_service.py`](app/services/auth_service.py) | JWT token creation/verification |
| [`app/services/student_service.py`](app/services/student_service.py) | Student dashboard, profile, assignments |
| [`app/services/teacher_service.py`](app/services/teacher_service.py) | Teacher dashboard, courses, grading |
| [`app/services/authority_service.py`](app/services/authority_service.py) | Admin statistics |
| [`app/services/group_service.py`](app/services/group_service.py) | Group management |
| [`app/services/test_service.py`](app/services/test_service.py) | Test taking, auto-grading |
| [`app/services/chat_service.py`](app/services/chat_service.py) | Chat functionality |
| [`app/services/notification_service.py`](app/services/notification_service.py) | Notifications |

---

## 9. Authentication & Security

### Security Middleware

**File:** [`app/middleware/security.py`](app/middleware/security.py)
- Adds security headers (X-Frame-Options, X-Content-Type-Options, etc.)

**File:** [`app/middleware/csrf.py`](app/middleware/csrf.py)
- CSRF token validation for POST/PUT/DELETE requests

### Session Management

**File:** [`app/main.py:61-65`](app/main.py:61)
```python
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="school_session"
)
```

### Password Hashing

Uses bcrypt via [`app/utils/bcrypt_compat.py`](app/utils/bcrypt_compat.py):

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
```

---

## 10. File Upload System

**Configuration:** [`app/core/config.py`](app/core/config.py)
```python
MAX_FILE_SIZE: int = 10485760  # 10MB
UPLOAD_DIR: str = "app/static/uploads"
ALLOWED_EXTENSIONS: str = "pdf,doc,docx,jpg,jpeg,png,mp4,avi,mov"
```

**Upload Directories:**
- `/static/uploads/avatars/` - Profile pictures
- `/static/uploads/assignments/` - Student submissions
- `/static/uploads/notes/` - Teacher notes
- `/static/uploads/videos/` - Educational videos

**Upload Handler** (in routers):
```python
@router.post("/upload")
async def upload_file(file: UploadFile):
    # 1. Validate file extension
    ext = os.path.splitext(file.filename)[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "File type not allowed")
    
    # 2. Generate unique filename
    filename = f"{uuid.uuid4()}{ext}"
    
    # 3. Save file
    file_path = f"{UPLOAD_DIR}/{filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": filename, "path": file_path}
```

---

## 11. Real-time Features

### WebSocket Chat

**File:** [`app/websocket/router.py`](app/websocket/router.py)
**Client:** [`app/static/js/chat.js`](app/static/js/chat.js)

**Connection:**
```javascript
const ws = new WebSocket(`ws://${window.location.host}/ws/chat`);
```

**Message Format:**
```json
{
    "type": "message",
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Hello!"
}
```

---

## 12. Extending the System

### How to Add a New Feature

#### Step 1: Create Database Model
Add model to appropriate file in `app/models/`:

```python
# app/models/new_feature_models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class NewFeature(Base):
    __tablename__ = "new_features"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
```

#### Step 2: Create Schema
Add Pydantic schema in `app/schemas/`:

```python
# app/schemas/new_feature.py
from pydantic import BaseModel

class NewFeatureBase(BaseModel):
    name: str
    description: str = None

class NewFeatureCreate(NewFeatureBase):
    pass
```

#### Step 3: Create Repository
Add data access methods in `app/repositories/`:

```python
# app/repositories/new_feature_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class NewFeatureRepository:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(NewFeature))
        return result.scalars().all()
```

#### Step 4: Create Service
Add business logic in `app/services/`:

```python
# app/services/new_feature_service.py
class NewFeatureService:
    @staticmethod
    async def get_all_features(db: AsyncSession):
        return await NewFeatureRepository.get_all(db)
```

#### Step 5: Add Web Router
Create route handlers in `app/web/routers/`:

```python
# app/web/routers/new_feature.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/new-feature")
async def list_features():
    return {"features": []}
```

#### Step 6: Register Router
Add to `app/main.py`:

```python
from app.web.routers import new_feature
app.include_router(new_feature.router, prefix="/new-feature")
```

#### Step 7: Create Template
Add HTML in `app/templates/new_feature/`:

```html
<!-- app/templates/new_feature/list.html -->
{% extends "base.html" %}
{% block content %}
<h1>New Feature</h1>
{% endblock %}
```

---

### Common Customization Points

| To Modify | Edit File |
|-----------|-----------|
| Token expiry | `app/core/config.py` |
| Allowed file types | `app/core/config.py` |
| User roles | `app/models/models.py` |
| Login logic | `app/services/auth_service.py` |
| Password hashing | `app/repositories/user_repository.py` |
| CORS settings | `app/main.py` |
| Database | `app/core/database.py` |

---

## Quick Reference

### Running the Application

```bash
# Development
python main.py
# or
uvicorn app.main:app --reload

# Production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Database Setup

```bash
# Initialize database
python scripts/setup/setup_database.py

# Run migrations
python scripts/migrations/run_add_name_migration.py
```

### Environment Variables

Create `.env` file:
```env
DATABASE_URL=sqlite:///./school_db.sqlite
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_ORIGINS=http://localhost:8000
AUTHORITY_SECRET_KEY=admin-secret-2024
```

### Testing

```bash
pytest tests/
```

---

## File Structure Summary

```
school_management_system/
├── app/
│   ├── api/               # REST API endpoints
│   │   └── endpoints/    # Individual feature endpoints
│   ├── core/              # Configuration, database, templates
│   ├── dependencies/      # Authentication dependencies
│   ├── middleware/        # Security middleware
│   ├── models/            # SQLAlchemy ORM models
│   ├── repositories/      # Data access layer
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic layer
│   ├── static/           # CSS, JS, uploads
│   ├── templates/        # Jinja2 HTML templates
│   ├── utils/            # Utilities
│   ├── web/              # Web routers (HTML pages)
│   ├── websocket/       # WebSocket handlers
│   └── main.py          # Application entry point
├── scripts/              # Database scripts, migrations
├── tests/                # Test files
└── requirements.txt      # Dependencies
```

---

*Document Version: 1.0*
*Last Updated: February 2026*
*For questions or modifications, refer to the code comments or contact the development team.*
