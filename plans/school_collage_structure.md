# School & College Management System - Final Best Structure

**Version:** 2.0  
**Last Updated:** 2026-03-22  
**Author:** Saroj Singh Dhami

---

## Overview

This document defines the final best structure for a unified School & College Management System. The system supports both educational institutions with separate databases, shared authentication, and role-specific modules.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UNIFIED APPLICATION                                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SHARED CORE (Auth, Config, DB)                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                       │
│           ┌────────────────────────┴────────────────────────┐             │
│           ▼                                                 ▼             │
│  ┌─────────────────────┐                        ┌─────────────────────┐   │
│  │    SCHOOL SYSTEM    │                        │   COLLEGE SYSTEM    │   │
│  │                     │                        │                     │   │
│  │  school_db          │                        │   college_db        │   │
│  │                     │                        │                     │   │
│  │  Modules:           │                        │   Modules:          │   │
│  │  - authority       │                        │   - dean            │   │
│  │  - teacher         │                        │   - hod             │   │
│  │  - student         │                        │   - faculty         │   │
│  │  - parent          │                        │   - student         │   │
│  │  - exam_section    │                        │   - registrar       │   │
│  │  - account_section │                        │   - exam_section    │   │
│  │  - library         │                        │   - account_section │   │
│  │                     │                        │   - library         │   │
│  │                     │                        │   - placement       │   │
│  │                     │                        │   - research        │   │
│  │                     │                        │   - hostel         │   │
│  │                     │                        │   - lab             │   │
│  └─────────────────────┘                        └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
education_management_system/
│
├── app/                              # Main application
│   ├── core/                         # Shared core components
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app
│   │   ├── config.py                 # Configuration
│   │   ├── database.py               # Database connection
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── auth.py                   # JWT/Authentication
│   │   └── constants.py              # Shared constants
│   │
│   ├── shared/                       # Shared modules
│   │   ├── auth/                     # Authentication
│   │   │   ├── dependencies.py
│   │   │   ├── jwt.py
│   │   │   ├── permissions.py
│   │   │   └── schemas.py
│   │   ├── middleware/               # Shared middleware
│   │   │   ├── security.py
│   │   │   ├── cors.py
│   │   │   └── institution.py        # School/College detector
│   │   └── utils/                    # Shared utilities
│   │       ├── email.py
│   │       ├── sms.py
│   │       └── storage.py
│   │
│   ├── models/                       # Database models
│   │   ├── base.py                   # Base model
│   │   ├── user.py                   # User model
│   │   ├── school/                   # School models
│   │   │   ├── student.py
│   │   │   ├── teacher.py
│   │   │   ├── parent.py
│   │   │   ├── authority.py
│   │   │   ├── class.py
│   │   │   └── section.py
│   │   └── college/                  # College models
│   │       ├── student.py
│   │       ├── faculty.py
│   │       ├── department.py
│   │       ├── program.py
│   │       ├── semester.py
│   │       ├── dean.py
│   │       └── registrar.py
│   │
│   ├── modules/                      # Feature modules
│   │   ├── school/                   # School-specific modules
│   │   │   ├── authority/            # Admin module for school
│   │   │   ├── teacher/
│   │   │   ├── student/
│   │   │   ├── parent/
│   │   │   ├── exam_section/
│   │   │   ├── account_section/
│   │   │   ├── library/
│   │   │   └── attendance/
│   │   │
│   │   └── college/                  # College-specific modules
│   │       ├── dean/
│   │       ├── hod/
│   │       ├── faculty/
│   │       ├── student/
│   │       ├── registrar/
│   │       ├── exam_section/
│   │       ├── account_section/
│   │       ├── library/
│   │       ├── placement/
│   │       ├── research/
│   │       ├── hostel/
│   │       └── lab/
│   │
│   ├── api/                          # API endpoints
│   │   ├── v1/
│   │   │   ├── auth.py               # Shared auth
│   │   │   ├── school/               # School endpoints
│   │   │   │   ├── students.py
│   │   │   │   ├── teachers.py
│   │   │   │   ├── authorities.py
│   │   │   │   ├── parents.py
│   │   │   │   ├── exams.py
│   │   │   │   ├── fees.py
│   │   │   │   └── library.py
│   │   │   │
│   │   │   └── college/              # College endpoints
│   │   │       ├── students.py
│   │   │       ├── faculty.py
│   │   │       ├── deans.py
│   │   │       ├── hod.py
│   │   │       ├── registrar.py
│   │   │       ├── exams.py
│   │   │       ├── fees.py
│   │   │       ├── library.py
│   │   │       ├── placements.py
│   │   │       ├── research.py
│   │   │       ├── hostels.py
│   │   │       └── labs.py
│   │   │
│   │   └── endpoints/                # Legacy endpoints
│   │
│   ├── web/                          # Web routes (HTML templates)
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── school/               # School web routes
│   │   │   │   ├── authority.py
│   │   │   │   ├── teacher.py
│   │   │   │   ├── student.py
│   │   │   │   ├── parent.py
│   │   │   │   └── dashboard.py
│   │   │   │
│   │   │   └── college/              # College web routes
│   │   │       ├── dean.py
│   │   │       ├── hod.py
│   │   │       ├── faculty.py
│   │   │       ├── student.py
│   │   │       └── dashboard.py
│   │   │
│   │   └── templates/                # HTML templates
│   │       ├── base.html
│   │       ├── auth/
│   │       ├── school/               # School templates
│   │       │   ├── authority/
│   │       │   ├── teacher/
│   │       │   ├── student/
│   │       │   ├── parent/
│   │       │   └── shared/
│   │       │
│   │       └── college/              # College templates
│   │           ├── dean/
│   │           ├── hod/
│   │           ├── faculty/
│   │           ├── student/
│   │           ├── registrar/
│   │           ├── exam_section/
│   │           ├── library/
│   │           ├── placement/
│   │           ├── research/
│   │           ├── hostel/
│   │           └── shared/
│   │
│   ├── static/                      # Static files
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   │       ├── school/
│   │       └── college/
│   │
│   └── migrations/                   # Database migrations
│
├── scripts/                          # Utility scripts
│   ├── migrate_school.py
│   ├── migrate_college.py
│   ├── seed_data.py
│   └── backup.py
│
├── tests/                           # Test files
│   ├── test_school/
│   ├── test_college/
│   └── test_shared/
│
├── docs/                            # Documentation
├── config/                          # Configuration files
│   ├── school.env
│   └── college.env
│
├── docker-compose.yml               # Docker configuration
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Module Structure (Per Module)

Each module follows a consistent structure:

```
module_name/
├── __init__.py
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── repository.py        # Data access layer
├── service.py          # Business logic
├── api.py              # API routes
├── web.py              # Web routes
├── constants.py        # Module constants
├── exceptions.py       # Custom exceptions
├── utils.py            # Helper functions
├── templates/          # HTML templates
│   ├── dashboard.html
│   ├── list.html
│   ├── detail.html
│   └── form.html
└── tests/
    ├── test_service.py
    └── test_api.py
```

---

## Role Comparison: School vs College

### Shared Roles (Similar but Different)

| Role | School | College |
|------|--------|---------|
| **Administrator** | Authority | Dean |
| **Teacher** | Teacher | Faculty/Professor |
| **Student** | Student | Student |
| **Exam Manager** | Exam Section | Exam Section |
| **Finance** | Account Section | Account Section |
| **Library** | Library | Library |

### Unique Roles

| School Only | College Only |
|-------------|--------------|
| Parent | HOD (Head of Department) |
| Class Teacher | Registrar |
| Section In-charge | Dean |
| - | Placement Cell |
| - | Research Manager |
| - | Hostel Warden |
| - | Lab Incharge |

---

## Database Structure

### Shared Database (auth_db)

```
auth_users
├── id
├── email (unique)
├── username
├── password_hash
├── full_name
├── role
├── is_active
├── can_access_school
├── can_access_college
├── created_at
└── updated_at

auth_sessions
├── id
├── user_id
├── session_token
├── institution_type
├── expires_at
└── created_at
```

### School Database (school_db)

```
schools
├── id
├── name
├── address
├── phone
├── email
├── logo
├── established_year
└── academic_year_start

classes (Grades 1-12)
├── id
├── school_id
├── name (Class 1, Class 2...)
├── section (A, B, C...)
├── class_teacher_id
└── academic_year

sections
├── id
├── class_id
├── name (A, B, C)
└── capacity

subjects
├── id
├── name
├── code
├── class_id
└── teacher_id

students
├── id
├── user_id
├── admission_no
├── class_id
├── section_id
├── roll_number
├── parent_id
└── (other fields)

teachers
├── id
├── user_id
├── employee_id
├── qualification
├── department
└── (other fields)

fees
├── id
├── class_id
├── fee_type
├── amount
├── due_date
└── academic_year
```

### College Database (college_db)

```
colleges
├── id
├── name
├── address
├── phone
├── email
├── university_affiliation
└── established_year

departments
├── id
├── college_id
├── name
├── code
├── hod_id
└── description

programs
├── id
├── department_id
├── name (BSc, MSc, BTech...)
├── code
├── duration_years
├── total_credits
└── level

semesters
├── id
├── program_id
├── name (Fall 2024, Spring 2025)
├── start_date
├── end_date
└── is_current

courses
├── id
├── code
├── name
├── credits
├── semester_id
├── program_id
├── department_id
├── instructor_id
└── is_elective

students
├── id
├── user_id
├── roll_number
├── program_id
├── semester_id
├── department_id
├── enrollment_date
└── (other fields)

faculty
├── id
├── user_id
├── employee_id
├── department_id
├── designation
├── qualification
├── specialization
└── (other fields)

salaries
├── id
├── faculty_id
├── month
├── basic_salary
├── allowances
├── deductions
└── net_pay
```

---

## API Endpoints Structure

### Authentication (Shared)
```
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

### School Endpoints
```
# Authority
GET    /api/v1/school/authorities
POST   /api/v1/school/authorities
GET    /api/v1/school/authorities/{id}
PUT    /api/v1/school/authorities/{id}
DELETE /api/v1/school/authorities/{id}

# Teachers
GET    /api/v1/school/teachers
POST   /api/v1/school/teachers
GET    /api/v1/school/teachers/{id}
PUT    /api/v1/school/teachers/{id}
DELETE /api/v1/school/teachers/{id}

# Students
GET    /api/v1/school/students
POST   /api/v1/school/students
GET    /api/v1/school/students/{id}
PUT    /api/v1/school/students/{id}
DELETE /api/v1/school/students/{id}

# Classes
GET    /api/v1/school/classes
POST   /api/v1/school/classes
GET    /api/v1/school/classes/{id}
PUT    /api/v1/school/classes/{id}

# Fees
GET    /api/v1/school/fees
POST   /api/v1/school/fees
GET    /api/v1/school/fees/student/{id}
POST   /api/v1/school/fees/pay
```

### College Endpoints
```
# Dean
GET    /api/v1/college/deans
POST   /api/v1/college/deans
GET    /api/v1/college/deans/{id}

# HOD
GET    /api/v1/college/hods
POST   /api/v1/college/hods
GET    /api/v1/college/hods/{id}
PUT    /api/v1/college/hods/{id}

# Faculty
GET    /api/v1/college/faculty
POST   /api/v1/college/faculty
GET    /api/v1/college/faculty/{id}
PUT    /api/v1/college/faculty/{id}

# Students
GET    /api/v1/college/students
POST   /api/v1/college/students
GET    /api/v1/college/students/{id}
PUT    /api/v1/college/students/{id}

# Programs
GET    /api/v1/college/programs
POST   /api/v1/college/programs
GET    /api/v1/college/programs/{id}

# Semesters
GET    /api/v1/college/semesters
POST   /api/v1/college/semesters

# Courses
GET    /api/v1/college/courses
POST   /api/v1/college/courses
GET    /api/v1/college/courses/{id}
PUT    /api/v1/college/courses/{id}

# Enrollments
GET    /api/v1/college/enrollments
POST   /api/v1/college/enrollments
PUT    /api/v1/college/enrollments/{id}/approve

# Placements
GET    /api/v1/college/companies
POST   /api/v1/college/companies
GET    /api/v1/college/jobs
POST   /api/v1/college/jobs
POST   /api/v1/college/jobs/{id}/apply

# Research
GET    /api/v1/college/projects
POST   /api/v1/college/projects
GET    /api/v1/college/publications
POST   /api/v1/college/publications

# Hostel
GET    /api/v1/college/hostels
POST   /api/v1/college/hostels
GET    /api/v1/college/rooms
POST   /api/v1/college/rooms/allocate
```

---

## Key Differences Summary

| Feature | School | College |
|---------|--------|---------|
| **Academic Structure** | Classes 1-12 | Programs, Semesters, Credits |
| **Time Period** | Terms (2-3/year) | Semesters (2/year) |
| **Assessment** | Marks/Percentage | GPA/CGPA |
| **Student ID** | Admission No | Roll No + Enrollment No |
| **Teacher ID** | Employee ID | Employee ID |
| **Primary Role** | Authority | Dean |
| **Department** | Optional | Core Feature |
| **Fees** | Annual/Term | Per Credit/Semester |
| **Exams** | Unit Tests + Finals | Mid-sem + End-sem |
| **Research** | Not Applicable | Core Feature |
| **Placements** | Not Applicable | Core Feature |
| **Hostel** | Optional | Common |
| **Parent Access** | Full | Limited |

---

## Implementation Strategy

### Phase 1: Infrastructure
- Setup shared authentication
- Create database schemas
- Build core API structure

### Phase 2: School System
- Implement authority module
- Implement teacher module
- Implement student module
- Implement parent module
- Implement exam section
- Implement account section
- Implement library

### Phase 3: College System
- Implement dean module
- Implement HOD module
- Implement faculty module
- Implement registrar module
- Implement placement module
- Implement research module
- Implement hostel module
- Implement lab module

### Phase 4: Production
- API Gateway (Nginx)
- Monitoring & Logging
- Automated Backups
- Testing

---

## Best Practices

1. **Modular Design**: Each role has its own module with consistent structure
2. **Shared Core**: Authentication and configuration shared between systems
3. **Separate Databases**: Complete data isolation for security
4. **Role-Based Access**: Clear permission boundaries
5. **API Versioning**: Use /api/v1/ prefix
6. **Database Indexing**: Index frequently queried columns
7. **Caching**: Redis for frequently accessed data
8. **Documentation**: Keep API docs updated

---

## Conclusion

This structure provides:
- Complete separation between school and college
- Shared authentication infrastructure
- Modular, maintainable codebase
- Clear role-based access control
- Scalable architecture for future growth

*End of Best Structure Document*
