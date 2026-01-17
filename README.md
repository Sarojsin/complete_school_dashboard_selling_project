# School Management System

A comprehensive FastAPI-based school management system with role-based access control for students, teachers, and administrators.

## Features

- **Student Portal**: View courses, assignments, grades, attendance, fees, notices, timetable, notes, and videos
- **Teacher Portal**: Manage students, courses, assignments, attendance, grades, and tests
- **Admin Portal**: Oversee all students, teachers, courses, fees, notices, analytics, and reports
- **Authentication**: JWT-based authentication with role-based access control
- **Real-time Chat**: WebSocket-based messaging system
- **Testing System**: Create and manage online tests with automatic grading

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update the database credentials:

```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/school_db
SECRET_KEY=your-secret-key-change-this-in-production
```

### 3. Setup Database

```bash
python -m scripts.setup.setup_database
```

This creates default users:
- **Admin**: username=`admin`, password=`admin123`
- **Teacher**: username=`teacher`, password=`teacher123`
- **Student**: username=`student`, password=`student123`

### 4. Run the Application

```bash
python run.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --port 8000
```

The application will be available at: http://localhost:8000

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Project Structure

```
claud/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── RENDER_DEPLOYMENT.md
├── api_testing.md
├── app
│   ├── api
│   │   └── v1
│   │       └── endpoints
│   ├── core
│   │   ├── config.py
│   │   ├── database.py
│   │   └── templates.py
│   ├── main.py
│   ├── middleware
│   │   └── security.py
│   ├── static
│   │   ├── images
│   │   │   └── default-avatar.png
│   │   └── uploads
│   │       ├── assignments
│   │       │   └── 07f47ade-3552-4fd4-b411-c18cb460164e.jpg
│   │       ├── avatars
│   │       │   ├── 2cc78636-5756-4ee7-8fd3-618e73a21912.jpeg
│   │       │   ├── 43ce75b3-1fca-4634-8567-b5e0b4ab43d4.jpg
│   │       │   ├── bfba1bef-2551-4bf9-9056-721be7bcded7.jpg
│   │       │   └── e4263e2a-0ec9-49e9-85e4-75c30c4ebde9.jpeg
│   │       ├── chat
│   │       ├── notes
│   │       │   ├── bf72ae6d-a437-4b7f-b405-63a65f512784.pptx
│   │       │   └── bff963cd-e61d-49fd-9652-ac1a37137433.pptx
│   │       ├── notices
│   │       └── videos
│   └── web
│       ├── authority_crud.py
│       └── routes.py
├── authority_routes_complete.py
├── build.sh
├── config
│   └── config.py
├── database
│   └── database.py
├── debug_enrollments.py
├── debug_test_questions.py
├── debug_tests.py
├── debug_visibility.py
├── dependencies.py
├── deployment.md
├── drop_column.py
├── enrollment_system.md
├── final_debug.py
├── finally_check_list.md
├── fix_main.py
├── group.md
├── guide.md
├── issue_to_solve.md
├── issued_by_claud.md
├── know_about_project.md
├── main.py
├── main.py.backup
├── makefile
├── media
│   └── logo2.png
├── migrate_grades.py
├── migrate_profile_pic.py
├── migrations
│   ├── add_name_columns.sql
│   ├── add_parent_id_to_students.py
│   └── add_parent_to_enum.sql
├── models
│   ├── chat_models.py
│   ├── group_models.py
│   ├── models.py
│   └── test_models.py
├── models_backup.py
├── old_fee_routes.py
├── plan_implemented.md
├── plan_to_do.txt
├── production_ready.md
├── project_report.md
├── quick_Solve_issue_API.md
├── quickstart.md
├── render.yaml
├── repositories
│   ├── assignment_repository.py
│   ├── attendance_repository.py
│   ├── chat_repository.py
│   ├── course_repository.py
│   ├── fee_repository.py
│   ├── fee_structure_repository.py
│   ├── grade_repository.py
│   ├── group_post_repository.py
│   ├── group_repository.py
│   ├── message_repository.py
│   ├── notes_repository.py
│   ├── notice_repository.py
│   ├── parent_repository.py
│   ├── student_repository.py
│   ├── teacher_repository.py
│   ├── test_repository.py
│   ├── user_repository.py
│   └── videos_repository.py
├── requirements.txt
├── routes
│   ├── assignments.py
│   ├── attendance.py
│   ├── auth.py
│   ├── authority.py
│   ├── chat.py
│   ├── courses.py
│   ├── fees.py
│   ├── grades.py
│   ├── group_posts.py
│   ├── groups.py
│   ├── notes.py
│   ├── notices.py
│   ├── parents.py
│   ├── students.py
│   ├── students.py.backup
│   ├── teachers.py
│   ├── tests.py
│   ├── videos.py
│   └── websocket_chat.py
├── routes.txt
├── run.py
├── schemas
│   ├── group_post_schemas.py
│   └── group_schemas.py
├── school_db.sqlite
├── scripts
│   ├── add_target_classes_column.py
│   ├── check
│   │   ├── check_db_enum.py
│   │   ├── check_enum.py
│   │   ├── check_enum_values.py
│   │   ├── check_local_db.py
│   │   ├── check_role_type.py
│   │   ├── check_schema.py
│   │   └── check_users.py
│   ├── create_assignment_test_data.py
│   ├── create_test_users.py
│   ├── debug_access.py
│   ├── fix
│   │   ├── fix_authority_urls.py
│   │   ├── fix_null_bytes.py
│   │   └── fix_student_urls.py
│   ├── generate_tree.py
│   ├── list_courses.py
│   ├── list_users.py
│   ├── migrations
│   │   ├── migrations_add_messages.py
│   │   └── run_add_name_migration.py
│   ├── raw_list_courses.py
│   ├── raw_list_users.py
│   ├── seed_courses.py
│   ├── setup
│   │   ├── add_parent_enum.py
│   │   ├── create_messages_table.py
│   │   ├── create_signup_student.py
│   │   ├── create_test_parent.py
│   │   ├── create_user.py
│   │   └── setup_database.py
│   ├── temp
│   │   ├── reproduce_enum.py
│   │   ├── temp_routes.py
│   │   ├── temp_routes_2.py
│   │   └── temp_routes_3.py
│   ├── test_auth.py
│   ├── verify
│   │   ├── debug_filter.py
│   │   ├── inspect_routes.py
│   │   ├── verify_authority_search.py
│   │   ├── verify_endpoints.py
│   │   └── verify_fix.py
│   └── verify_groups.py
├── security.md
├── services
│   ├── attendance_service.py
│   ├── auth_service.py
│   ├── chat_cleanup_service.py
│   ├── grade_service.py
│   ├── group_post_service.py
│   ├── group_service.py
│   ├── notification_service.py
│   ├── student_service.py
│   ├── teacher_service.py
│   └── test_service.py
├── setup_database.py
├── simple_debug.py
├── static
│   ├── css
│   │   ├── style.css
│   │   └── test.css
│   ├── groups
│   │   ├── groups.css
│   │   └── posts.css
│   ├── js
│   │   ├── chat.js
│   │   ├── dashboard.js
│   │   ├── main.js
│   │   └── test_timer.js
│   └── uploads
│       ├── assignments
│       ├── avatars
│       ├── notes
│       └── videos
├── tables
│   ├── chat_tables.py
│   ├── group_post_schemas.py
│   ├── group_schemas.py
│   ├── tables.py
│   └── test_tables.py
├── templates
│   ├── auth
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── signup_authority.html
│   │   ├── signup_parent.html
│   │   ├── signup_student.html
│   │   └── signup_teacher.html
│   ├── authority
│   │   ├── add_course.html
│   │   ├── add_fee.html
│   │   ├── add_notice.html
│   │   ├── add_student.html
│   │   ├── add_teacher.html
│   │   ├── analytics_v2.html
│   │   ├── course_detail.html
│   │   ├── courses.html
│   │   ├── create_notice.html
│   │   ├── dashboard.html
│   │   ├── edit_course.html
│   │   ├── edit_notice.html
│   │   ├── edit_student.html
│   │   ├── edit_teacher.html
│   │   ├── fee_structure.html
│   │   ├── fees.html
│   │   ├── groups.html
│   │   ├── notices.html
│   │   ├── reports.html
│   │   ├── student_detail.html
│   │   ├── students.html
│   │   ├── teacher_detail.html
│   │   ├── teachers.html
│   │   └── view_notice.html
│   ├── base.html
│   ├── groups
│   │   ├── create_group.html
│   │   ├── edit_group.html
│   │   ├── group_detail.html
│   │   ├── group_list.html
│   │   ├── group_posts.html
│   │   ├── manage_members.html
│   │   ├── new_post.html
│   │   └── view_post.html
│   ├── index.html
│   ├── parent
│   │   ├── attendance.html
│   │   ├── chat.html
│   │   ├── dashboard.html
│   │   ├── grades.html
│   │   ├── homework.html
│   │   ├── notices.html
│   │   └── profile.html
│   ├── student
│   │   ├── assignments.html
│   │   ├── assignments_detail.html
│   │   ├── attendance.html
│   │   ├── courses.html
│   │   ├── dashboard.html
│   │   ├── fees.html
│   │   ├── forum.html
│   │   ├── grades.html
│   │   ├── groups.html
│   │   ├── messages.html
│   │   ├── notes.html
│   │   ├── notices.html
│   │   ├── profile.html
│   │   ├── sidebar.html
│   │   ├── take_test.html
│   │   ├── teachers.html
│   │   ├── test_list.html
│   │   ├── test_result.html
│   │   ├── timetable.html
│   │   └── videos.html
│   └── teacher
│       ├── add_grade.html
│       ├── assignments.html
│       ├── attendance.html
│       ├── chat.html
│       ├── course_detail.html
│       ├── courses.html
│       ├── create_assignment.html
│       ├── create_notice.html
│       ├── create_test.html
│       ├── dashboard.html
│       ├── edit_assignment.html
│       ├── edit_test.html
│       ├── grades.html
│       ├── groups.html
│       ├── messages.html
│       ├── profile.html
│       ├── sidebar.html
│       ├── student_detail.html
│       ├── student_grades.html
│       ├── students.html
│       ├── take_attendance.html
│       ├── timetable.html
│       ├── upload_notes.html
│       ├── upload_videos.html
│       ├── view_submissions.html
│       └── view_tests.html
├── test_output.txt
├── test_output_2.txt
├── tests
│   ├── test_add_course.py
│   ├── test_add_student_form.py
│   ├── test_auth_api_only.py
│   ├── test_auth_fix.py
│   ├── test_bcrypt.py
│   ├── test_chat_simple.py
│   ├── test_course_search.py
│   ├── test_fee_structure.py
│   ├── test_login_signup.py
│   ├── test_name_fields.py
│   ├── test_parent_all_teachers.py
│   ├── test_parent_chat.py
│   ├── test_parent_dashboard.py
│   ├── test_parent_endpoints.py
│   ├── test_parent_teacher_chat.py
│   ├── test_refresh_flow.py
│   ├── test_signup_api.py
│   ├── test_student_auth.py
│   ├── test_teacher_chat.py
│   └── test_teacher_search.py
├── things_to_add_on security.md
├── things_we_learn_by_this_project.md
├── utils
│   ├── bcrypt_compat.py
│   ├── constants.py
│   ├── exceptions.py
│   └── websocket_manager.py
└── verify_cleanup.py
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/signup` - Register new user

### Student Endpoints
- `GET /api/students/dashboard` - Student dashboard
- `GET /api/students/courses` - Enrolled courses
- `GET /api/students/assignments` - Assignments
- `GET /api/students/grades` - Grades
- `GET /api/students/attendance` - Attendance records
- `GET /api/students/fees` - Fee records
- `GET /api/students/notices` - Notices
- `GET /api/students/timetable` - Class schedule
- `GET /api/students/notes` - Course notes
- `GET /api/students/videos` - Course videos

### Teacher Endpoints
- `GET /api/teachers/dashboard` - Teacher dashboard
- `GET /api/teachers/students` - Students list
- `GET /api/teachers/courses` - Teaching courses
- `GET /api/teachers/assignments` - Created assignments
- `GET /api/teachers/attendance` - Attendance records
- `GET /api/teachers/grades` - Grades

### Authority Endpoints
- `GET /api/authority/dashboard` - Admin dashboard
- `GET /api/authority/students` - All students
- `GET /api/authority/teachers` - All teachers
- `GET /api/authority/courses` - All courses
- `GET /api/authority/fees` - All fee records
- `GET /api/authority/notices` - All notices
- `GET /api/authority/analytics` - System analytics
- `GET /api/authority/reports` - System reports

### Chat Endpoints
- `GET /api/chat/contacts/parent` - Get parent's teacher contacts
- `GET /api/chat/messages/{user_id}` - Get chat history with a user
- `POST /api/chat/messages/{user_id}` - Send a message to a user

## Testing

Run the endpoint verification script:

```bash
python -m scripts.verify.verify_endpoints
```

## Documentation

- [API Testing Guide](api_testing.md) - Detailed API testing examples
- [Deployment Guide](deployment.md) - Production deployment instructions
- [Quick Start Guide](quickstart.md) - Getting started guide
- [Feature Checklist](finally_check_list.md) - Complete feature list

## License

MIT License
# Admin
1. Saroj 

## contibuters
1. Saroj Singh Dhami (backend)
2. Rijan Ghimire (frontend)
3. sushil Ghimire (frontend)
4. sujal pant (Designer)