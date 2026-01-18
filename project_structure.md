## Project Structure

```
school_management_system/
├── 📄 Root Configuration Files
│   ├── .env                          # Environment variables
│   ├── .env.example                  # Environment template
│   ├── .gitignore                    # Git ignore rules
│   ├── Dockerfile                    # Docker container definition
│   ├── docker-compose.yml            # Docker services orchestration
│   ├── requirements.txt              # Python dependencies
│   ├── pytest.ini                    # Pytest configuration
│   ├── render.yaml                   # Render deployment config
│   ├── build.sh                      # Build script
│   ├── run.py                        # Application entry point
│   ├── main.py                       # Legacy main (backup)
│   ├── dependencies.py               # FastAPI dependencies
│   └── makefile                      # Common commands
|
├── 📱 app/                           # Main application package
│   ├── __init__.py
│   ├── main.py                       # FastAPI application factory
│   │
│   ├── 🎯 core/                      # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                 # Settings & environment
│   │   ├── database.py               # AsyncPG database setup
│   │   └── templates.py              # Jinja2 template config
│   │
│   ├── 🔐 middleware/                # Request middleware
│   │   ├── __init__.py
│   │   ├── csrf.py                   # CSRF protection
│   │   └── security.py               # Security headers
│   │
│   ├── 🌐 web/                       # Web interface
│   │   ├── __init__.py
│   │   ├── authority_crud.py         # Authority CRUD helpers
│   │   └── routers/                  # Role-based route modules
│   │       ├── __init__.py
│   │       ├── common.py             # Common routes (login, signup)
│   │       ├── student.py            # Student portal routes
│   │       ├── teacher.py            # Teacher portal routes
│   │       ├── authority.py          # Authority portal routes
│   │       └── parent.py             # Parent portal routes
│   │
│   ├── 🔌 api/                       # REST API endpoints (future)
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── endpoints/
│   │
│   └── 📁 static/                    # Static assets
│       ├── __init__.py
│       ├── images/                   # Images
│       │   └── default-avatar.png
│       └── uploads/                  # User uploads
│           ├── assignments/
│           ├── avatars/
│           ├── chat/
│           ├── notes/
│           ├── notices/
│           └── videos/
|
├── 🗄️ models/                        # SQLAlchemy models
│   ├── __init__.py
│   ├── models.py                     # Core models (User, Student, Teacher, etc.)
│   ├── test_models.py                # Test system models
│   ├── chat_models.py                # Chat/messaging models
│   └── group_models.py               # Group system models
|
├── 🔀 routes/                        # API route handlers (async)
│   ├── __init__.py
│   ├── auth.py                       # Authentication endpoints
│   ├── students.py                   # Student API
│   ├── teachers.py                   # Teacher API
│   ├── authority.py                  # Authority API
│   ├── parents.py                    # Parent API
│   ├── courses.py                    # Course management
│   ├── assignments.py                # Assignment operations
│   ├── attendance.py                 # Attendance tracking
│   ├── grades.py                     # Grade management
│   ├── fees.py                       # Fee management
│   ├── tests.py                      # Test system
│   ├── notices.py                    # Notice board
│   ├── notes.py                      # Course notes
│   ├── videos.py                     # Course videos
│   ├── chat.py                       # REST chat API
│   ├── websocket_chat.py             # WebSocket chat
│   ├── groups.py                     # Group management
│   └── group_posts.py                # Group posts
|
├── 💼 repositories/                  # Data access layer (async)
│   ├── __init__.py
│   ├── user_repository.py            # User operations
│   ├── student_repository.py         # Student data access
│   ├── teacher_repository.py         # Teacher data access
│   ├── parent_repository.py          # Parent data access
│   ├── course_repository.py          # Course data access
│   ├── assignment_repository.py      # Assignment operations
│   ├── attendance_repository.py      # Attendance operations
│   ├── grade_repository.py           # Grade operations
│   ├── fee_repository.py             # Fee operations
│   ├── fee_structure_repository.py   # Fee structure config
│   ├── test_repository.py            # Test operations
│   ├── notice_repository.py          # Notice operations
│   ├── notes_repository.py           # Notes operations
│   ├── videos_repository.py          # Video operations
│   ├── message_repository.py         # Messaging operations
│   ├── chat_repository.py            # Chat operations
│   ├── group_repository.py           # Group operations
│   └── group_post_repository.py      # Group post operations
|
├── 🎯 services/                      # Business logic layer (async)
│   ├── __init__.py
│   ├── auth_service.py               # Authentication logic
│   ├── student_service.py            # Student business logic
│   ├── teacher_service.py            # Teacher business logic
│   ├── attendance_service.py         # Attendance logic
│   ├── grade_service.py              # Grading logic
│   ├── test_service.py               # Test management logic
│   ├── notification_service.py       # Notification system
│   ├── chat_cleanup_service.py       # Chat cleanup jobs
│   ├── group_service.py              # Group management
│   └── group_post_service.py         # Group post logic
|
├── 📋 tables/                        # Pydantic schemas
│   ├── __init__.py
│   ├── tables.py                     # Core schemas
│   ├── test_tables.py                # Test schemas
│   ├── chat_tables.py                # Chat schemas
│   ├── group_schemas.py              # Group schemas
│   └── group_post_schemas.py         # Group post schemas
|
├── 🎨 templates/                     # Jinja2 HTML templates
│   ├── __init__.py
│   ├── base.html                     # Base template
│   ├── index.html                    # Landing page
│   │
│   ├── auth/                         # Authentication pages
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── signup_student.html
│   │   ├── signup_teacher.html
│   │   ├── signup_parent.html
│   │   └── signup_authority.html
│   │
│   ├── student/                      # Student portal
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── courses.html
│   │   ├── assignments.html
│   │   ├── assignments_detail.html
│   │   ├── grades.html
│   │   ├── attendance.html
│   │   ├── fees.html
│   │   ├── test_list.html
│   │   ├── take_test.html
│   │   ├── test_result.html
│   │   ├── notes.html
│   │   ├── videos.html
│   │   ├── notices.html
│   │   ├── messages.html
│   │   ├── groups.html
│   │   ├── timetable.html
│   │   └── sidebar.html
│   │
│   ├── teacher/                      # Teacher portal
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── courses.html
│   │   ├── course_detail.html
│   │   ├── students.html
│   │   ├── student_detail.html
│   │   ├── assignments.html
│   │   ├── create_assignment.html
│   │   ├── edit_assignment.html
│   │   ├── view_submissions.html
│   │   ├── grades.html
│   │   ├── student_grades.html
│   │   ├── add_grade.html
│   │   ├── attendance.html
│   │   ├── take_attendance.html
│   │   ├── create_test.html
│   │   ├── edit_test.html
│   │   ├── view_tests.html
│   │   ├── upload_notes.html
│   │   ├── upload_videos.html
│   │   ├── messages.html
│   │   ├── chat.html
│   │   ├── groups.html
│   │   ├── create_notice.html
│   │   ├── timetable.html
│   │   └── sidebar.html
│   │
│   ├── authority/                    # Authority portal
│   │   ├── dashboard.html
│   │   ├── students.html
│   │   ├── student_detail.html
│   │   ├── add_student.html
│   │   ├── edit_student.html
│   │   ├── teachers.html
│   │   ├── teacher_detail.html
│   │   ├── add_teacher.html
│   │   ├── edit_teacher.html
│   │   ├── courses.html
│   │   ├── course_detail.html
│   │   ├── add_course.html
│   │   ├── edit_course.html
│   │   ├── fees.html
│   │   ├── fee_structure.html
│   │   ├── add_fee.html
│   │   ├── notices.html
│   │   ├── create_notice.html
│   │   ├── edit_notice.html
│   │   ├── view_notice.html
│   │   ├── add_notice.html
│   │   ├── groups.html
│   │   ├── create_group.html
│   │   ├── analytics_v2.html
│   │   └── reports.html
│   │
│   ├── parent/                       # Parent portal
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── attendance.html
│   │   ├── grades.html
│   │   ├── homework.html
│   │   ├── notices.html
│   │   └── chat.html
│   │
│   └── groups/                       # Group system templates
│       ├── group_list.html
│       ├── group_detail.html
│       ├── create_group.html
│       ├── edit_group.html
│       ├── manage_members.html
│       ├── group_posts.html
│       ├── new_post.html
│       └── view_post.html
|
├── 💅 static/                        # Frontend assets
│   ├── __init__.py
│   ├── css/
│   │   ├── style.css                 # Main stylesheet
│   │   └── test.css                  # Test page styles
│   ├── groups/
│   │   ├── groups.css                # Group styles
│   │   └── posts.css                 # Post styles
│   ├── js/
│   │   ├── __init__.py
│   │   ├── main.js                   # Main JavaScript
│   │   ├── dashboard.js              # Dashboard features
│   │   ├── chat.js                   # Chat functionality
│   │   └── test_timer.js             # Test timer logic
│   └── uploads/                      # User-generated content
│       ├── assignments/
│       ├── avatars/
│       ├── notes/
│       └── videos/
|
├── 🧪 tests/                         # Test suite
│   ├── conftest.py                   # Pytest fixtures (async)
│   ├── test_auth_api_only.py
│   ├── test_authority_routes.py
│   ├── test_student_routes.py
│   ├── test_teacher_search.py
│   ├── test_parent_dashboard.py
│   ├── test_login_signup.py
│   ├── test_course_search.py
│   ├── test_fee_structure.py
│   └── ... (22+ test files)
|
├── 🔧 utils/                         # Utility functions
│   ├── __init__.py
│   ├── constants.py                  # Application constants
│   ├── exceptions.py                 # Custom exceptions
│   ├── websocket_manager.py          # WebSocket connection manager
│   └── bcrypt_compat.py              # Bcrypt compatibility
|
├── 🛠️ scripts/                       # Management scripts
│   ├── setup/                        # Setup scripts
│   │   ├── setup_database.py         # Database initialization
│   │   ├── create_user.py
│   │   ├── create_signup_student.py
│   │   └── ...
│   ├── check/                        # Diagnostic scripts
│   │   ├── check_db_enum.py
│   │   ├── check_schema.py
│   │   └── ...
│   ├── fix/                          # Fix utilities
│   │   ├── fix_authority_urls.py
│   │   └── ...
│   ├── migrations/                   # Data migrations
│   └── verify/                       # Verification scripts
|
├── 🗂️ database/                      # Legacy database (deprecated)
│   └── database.py                   # Old sync database config
|
├── 🔧 config/                        # Legacy config (deprecated)
│   └── config.py                     # Old config file
|
├── 📊 media/                         # Media assets
│   └── logo2.png
|
├── 📝 Documentation
│   ├── README.md                     # Main documentation
│   ├── quickstart.md                 # Quick start guide
│   ├── deployment.md                 # Deployment guide
│   ├── RENDER_DEPLOYMENT.md          # Render-specific deployment
│   ├── api_testing.md                # API testing guide
│   ├── test.md                       # Production readiness assessment
│   ├── know_about_project.md         # Project overview
│   ├── enrollment_system.md          # Enrollment system docs
│   ├── group.md                      # Group system docs
│   └── ... (various planning/tracking docs)
|
└── 🗃️ migrations/                    # Database migrations
    ├── add_name_columns.sql
    ├── add_parent_to_enum.sql
    └── add_parent_id_to_students.py
```

### Key Directories Explained

#### 🎯 Core Application (`app/`)
- **`core/`**: Configuration, async database setup, and template engine
- **`middleware/`**: Security and CSRF protection layers
- **`web/routers/`**: Modular, role-based route handlers (NEW - fully async)

#### 💾 Data Layer
- **`models/`**: SQLAlchemy ORM models defining database schema
- **`repositories/`**: Data access objects with async operations (19 repositories)
- **`tables/`**: Pydantic schemas for request/response validation

#### 🔀 API Layer
- **`routes/`**: FastAPI route handlers for REST API endpoints (all async)
- **`services/`**: Business logic layer between routes and repositories (all async)

#### 🎨 Presentation Layer
- **`templates/`**: Jinja2 HTML templates organized by role
- **`static/`**: CSS, JavaScript, and media files

#### 🧪 Quality Assurance
- **`tests/`**: Comprehensive test suite with async fixtures
- **`scripts/`**: Setup, verification, and maintenance utilities

### Architecture Highlights

✅ **Full Async Stack**: AsyncPG + AsyncSession throughout  
✅ **Repository Pattern**: 19+ specialized data access objects  
✅ **Service Layer**: 11+ business logic services  
✅ **Modular Routes**: Role-based route organization  
✅ **Type Safety**: Pydantic schemas for all data  
✅ **Test Coverage**: Pytest with async support configured
