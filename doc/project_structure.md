## project_structure.md
## Project Structure

school_management_system/
├── 📱 app/
│   ├── 🔌 api/
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── assignments.py
│   │   │   ├── attendance.py
│   │   │   ├── auth.py
│   │   │   ├── authority.py
│   │   │   ├── chat.py
│   │   │   ├── courses.py
│   │   │   ├── fees.py
│   │   │   ├── grades.py
│   │   │   ├── group_posts.py
│   │   │   ├── groups.py
│   │   │   ├── notes.py
│   │   │   ├── notices.py
│   │   │   ├── parents.py
│   │   │   ├── students.py
│   │   │   ├── students.py.backup
│   │   │   ├── teachers.py
│   │   │   ├── tests.py
│   │   │   ├── videos.py
│   │   │   └── websocket_chat.py
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── 🎯 core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── templates.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── legacy/
│   │   ├── schemas/
│   │   │   ├── group_post_schemas.py
│   │   │   └── group_schemas.py
│   │   ├── 📋 tables/
│   │   │   ├── __init__.py
│   │   │   ├── chat_tables.py
│   │   │   ├── group_post_schemas.py
│   │   │   ├── group_schemas.py
│   │   │   ├── tables.py
│   │   │   └── test_tables.py
│   │   └── old_fee_routes.py.backup
│   ├── 📊 media/
│   │   └── logo2.png
│   ├── 🔐 middleware/
│   │   ├── __init__.py
│   │   ├── csrf.py
│   │   └── security.py
│   ├── 🗄️ models/
│   │   ├── __init__.py
│   │   ├── chat_models.py
│   │   ├── group_models.py
│   │   ├── models.py
│   │   └── test_models.py
│   ├── 💼 repositories/
│   │   ├── __init__.py
│   │   ├── assignment_repository.py
│   │   ├── attendance_repository.py
│   │   ├── chat_repository.py
│   │   ├── course_repository.py
│   │   ├── fee_repository.py
│   │   ├── fee_structure_repository.py
│   │   ├── grade_repository.py
│   │   ├── group_post_repository.py
│   │   ├── group_repository.py
│   │   ├── message_repository.py
│   │   ├── notes_repository.py
│   │   ├── notice_repository.py
│   │   ├── parent_repository.py
│   │   ├── student_repository.py
│   │   ├── teacher_repository.py
│   │   ├── test_repository.py
│   │   ├── user_repository.py
│   │   └── videos_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── assignment.py
│   │   ├── attendance.py
│   │   ├── auth.py
│   │   ├── authority.py
│   │   ├── course.py
│   │   ├── fee.py
│   │   ├── grade.py
│   │   ├── group.py
│   │   ├── group_post.py
│   │   ├── misc.py
│   │   ├── notice.py
│   │   ├── parent.py
│   │   ├── student.py
│   │   ├── teacher.py
│   │   └── user.py
│   ├── 🎯 services/
│   │   ├── __init__.py
│   │   ├── attendance_service.py
│   │   ├── auth_service.py
│   │   ├── authority_service.py
│   │   ├── chat_cleanup_service.py
│   │   ├── chat_service.py
│   │   ├── grade_service.py
│   │   ├── group_post_service.py
│   │   ├── group_service.py
│   │   ├── notification_service.py
│   │   ├── parent_service.py
│   │   ├── student_service.py
│   │   ├── teacher_service.py
│   │   └── test_service.py
│   ├── 📁 static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── test.css
│   │   ├── groups/
│   │   │   ├── groups.css
│   │   │   └── posts.css
│   │   ├── images/
│   │   │   └── default-avatar.png
│   │   ├── js/
│   │   │   ├── __init__.py
│   │   │   ├── chat.js
│   │   │   ├── dashboard.js
│   │   │   ├── main.js
│   │   │   └── test_timer.js
│   │   ├── uploads/
│   │   │   ├── assignments/
│   │   │   │   └── 07f47ade-3552-4fd4-b411-c18cb460164e.jpg
│   │   │   ├── avatars/
│   │   │   │   ├── 2cc78636-5756-4ee7-8fd3-618e73a21912.jpeg
│   │   │   │   ├── 43ce75b3-1fca-4634-8567-b5e0b4ab43d4.jpg
│   │   │   │   ├── bfba1bef-2551-4bf9-9056-721be7bcded7.jpg
│   │   │   │   └── e4263e2a-0ec9-49e9-85e4-75c30c4ebde9.jpeg
│   │   │   ├── notes/
│   │   │   │   ├── bf72ae6d-a437-4b7f-b405-63a65f512784.pptx
│   │   │   │   └── bff963cd-e61d-49fd-9652-ac1a37137433.pptx
│   │   │   └── videos/
│   │   │       └── de3e010f-8577-4539-b681-8a43a493427f.mp4
│   │   └── __init__.py
│   ├── 🎨 templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── signup.html
│   │   │   ├── signup_authority.html
│   │   │   ├── signup_parent.html
│   │   │   ├── signup_student.html
│   │   │   └── signup_teacher.html
│   │   ├── authority/
│   │   │   ├── add_course.html
│   │   │   ├── add_fee.html
│   │   │   ├── add_notice.html
│   │   │   ├── add_student.html
│   │   │   ├── add_teacher.html
│   │   │   ├── analytics_v2.html
│   │   │   ├── course_detail.html
│   │   │   ├── courses.html
│   │   │   ├── create_group.html
│   │   │   ├── create_notice.html
│   │   │   ├── dashboard.html
│   │   │   ├── edit_course.html
│   │   │   ├── edit_notice.html
│   │   │   ├── edit_student.html
│   │   │   ├── edit_teacher.html
│   │   │   ├── fee_structure.html
│   │   │   ├── fees.html
│   │   │   ├── groups.html
│   │   │   ├── manage_group.html
│   │   │   ├── notices.html
│   │   │   ├── reports.html
│   │   │   ├── student_detail.html
│   │   │   ├── students.html
│   │   │   ├── teacher_detail.html
│   │   │   ├── teachers.html
│   │   │   └── view_notice.html
│   │   ├── groups/
│   │   │   ├── create_group.html
│   │   │   ├── edit_group.html
│   │   │   ├── group_detail.html
│   │   │   ├── group_list.html
│   │   │   ├── group_posts.html
│   │   │   ├── manage_members.html
│   │   │   ├── new_post.html
│   │   │   └── view_post.html
│   │   ├── parent/
│   │   │   ├── attendance.html
│   │   │   ├── chat.html
│   │   │   ├── dashboard.html
│   │   │   ├── grades.html
│   │   │   ├── homework.html
│   │   │   ├── notices.html
│   │   │   └── profile.html
│   │   ├── student/
│   │   │   ├── assignments.html
│   │   │   ├── assignments_detail.html
│   │   │   ├── attendance.html
│   │   │   ├── courses.html
│   │   │   ├── dashboard.html
│   │   │   ├── fees.html
│   │   │   ├── forum.html
│   │   │   ├── grades.html
│   │   │   ├── groups.html
│   │   │   ├── messages.html
│   │   │   ├── notes.html
│   │   │   ├── notices.html
│   │   │   ├── profile.html
│   │   │   ├── sidebar.html
│   │   │   ├── take_test.html
│   │   │   ├── teachers.html
│   │   │   ├── test_list.html
│   │   │   ├── test_result.html
│   │   │   ├── timetable.html
│   │   │   └── videos.html
│   │   ├── teacher/
│   │   │   ├── add_grade.html
│   │   │   ├── assignments.html
│   │   │   ├── attendance.html
│   │   │   ├── chat.html
│   │   │   ├── course_detail.html
│   │   │   ├── courses.html
│   │   │   ├── create_assignment.html
│   │   │   ├── create_notice.html
│   │   │   ├── create_test.html
│   │   │   ├── dashboard.html
│   │   │   ├── edit_assignment.html
│   │   │   ├── edit_test.html
│   │   │   ├── grades.html
│   │   │   ├── groups.html
│   │   │   ├── messages.html
│   │   │   ├── profile.html
│   │   │   ├── sidebar.html
│   │   │   ├── student_detail.html
│   │   │   ├── student_grades.html
│   │   │   ├── students.html
│   │   │   ├── take_attendance.html
│   │   │   ├── timetable.html
│   │   │   ├── upload_notes.html
│   │   │   ├── upload_videos.html
│   │   │   ├── view_attendance_session.html
│   │   │   ├── view_submissions.html
│   │   │   └── view_tests.html
│   │   ├── __init__.py
│   │   ├── base.html
│   │   └── index.html
│   ├── 🔧 utils/
│   │   ├── __init__.py
│   │   ├── bcrypt_compat.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── websocket_manager.py
│   ├── 🌐 web/
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── authority.py
│   │   │   ├── common.py
│   │   │   ├── group_posts.py
│   │   │   ├── groups.py
│   │   │   ├── parent.py
│   │   │   ├── student.py
│   │   │   └── teacher.py
│   │   ├── __init__.py
│   │   ├── authority_crud.py
│   │   └── routes.py.old
│   ├── websocket/
│   │   ├── __init__.py
│   │   └── router.py
│   ├── __init__.py
│   └── main.py
├── 🔧 config/
│   ├── __init__.py
│   └── config.py
├── 🗂️ database/
│   ├── __init__.py
│   └── database.py
├── 🔀 routes/
├── 🛠️ scripts/
│   ├── check/
│   │   ├── check_db_enum.py
│   │   ├── check_db_teachers.py
│   │   ├── check_enum.py
│   │   ├── check_enum_values.py
│   │   ├── check_integrity.py
│   │   ├── check_local_db.py
│   │   ├── check_role_type.py
│   │   ├── check_schema.py
│   │   ├── check_test.py
│   │   ├── check_users.py
│   │   ├── list_courses.py
│   │   ├── list_users.py
│   │   ├── raw_list_courses.py
│   │   ├── raw_list_users.py
│   │   ├── test_auth.py
│   │   └── test_teacher_lookup.py
│   ├── debug/
│   │   ├── debug_access.py
│   │   ├── debug_enrollments.py
│   │   ├── debug_teacher_repo.py
│   │   ├── debug_test_questions.py
│   │   ├── debug_tests.py
│   │   ├── debug_visibility.py
│   │   ├── final_debug.py
│   │   └── simple_debug.py
│   ├── fix/
│   │   ├── fix_authority_urls.py
│   │   ├── fix_imports_bulk.py
│   │   ├── fix_main.py
│   │   ├── fix_null_bytes.py
│   │   ├── fix_student_urls.py
│   │   └── inject_csrf.py
│   ├── 🗃️ migrations/
│   │   ├── add_name_columns.sql
│   │   ├── add_parent_id_to_students.py
│   │   ├── add_parent_to_enum.sql
│   │   ├── add_target_classes_column.py
│   │   ├── drop_column.py
│   │   ├── migrate_attendance.py
│   │   ├── migrate_grades.py
│   │   ├── migrate_profile_pic.py
│   │   ├── migrations_add_messages.py
│   │   └── run_add_name_migration.py
│   ├── setup/
│   │   ├── add_parent_enum.py
│   │   ├── create_assignment_test_data.py
│   │   ├── create_messages_table.py
│   │   ├── create_signup_student.py
│   │   ├── create_test_parent.py
│   │   ├── create_test_users.py
│   │   ├── create_user.py
│   │   ├── seed_courses.py
│   │   └── setup_database.py
│   ├── temp/
│   │   ├── authority_routes_complete.py
│   │   ├── main.py.backup
│   │   ├── models_backup.py
│   │   ├── reproduce_enum.py
│   │   ├── routes.txt
│   │   ├── temp_routes.py
│   │   ├── temp_routes_2.py
│   │   └── temp_routes_3.py
│   ├── 🔧 utils/
│   └── verify/
│       ├── debug_filter.py
│       ├── inspect_routes.py
│       ├── verify_authority_search.py
│       ├── verify_cleanup.py
│       ├── verify_endpoints.py
│       ├── verify_fix.py
│       └── verify_groups.py
├── 📁 static/
│   └── uploads/
│       └── videos/
├── 🧪 tests/
│   ├── conftest.py
│   ├── test_add_course.py
│   ├── test_add_student_form.py
│   ├── test_auth_api_only.py
│   ├── test_auth_fix.py
│   ├── test_authority_routes.py
│   ├── test_bcrypt.py
│   ├── test_chat_simple.py
│   ├── test_course_search.py
│   ├── test_delete_route.py
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
│   ├── test_student_routes.py
│   ├── test_teacher_chat.py
│   ├── test_teacher_search.py
│   └── test_web_basic.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── RENDER_DEPLOYMENT.md
├── api_testing.md
├── build.sh
├── csrf.md
├── deployment.md
├── docker-compose.yml
├── enrollment_system.md
├── finally_check_list.md
├── group.md
├── guide.md
├── issue_to_solve.md
├── issued_by_claud.md
├── know_about_project.md
├── lets_go.md
├── lets_go2.md
├── logic_feature.md
├── main.py
├── makefile
├── new.md
├── plan_implemented.md
├── plan_to_do.txt
├── problem.md
├── production_ready.md
├── project_report.md
├── project_structure.md
├── pytest.ini
├── quick_Solve_issue_API.md
├── quickstart.md
├── render.yaml
├── requirements.txt
├── roadmap_to_10.md
├── run.py
├── school_db.sqlite
├── security.md
├── test.md
├── things_to_add_on security.md
├── things_we_learn_by_this_project.md
└── tree.py


### Key Directories Explained

#### 🎯 Core Application (`app/`)
- **`core/`**: Configuration, async database setup, and template engine
- **`middleware/`**: Security and CSRF protection layers
- **`web/routers/`**: Modular, role-based route handlers (NEW - fully async)

#### 💾 Data Layer
- **`models/`**: SQLAlchemy ORM models defining database schema
- **`repositories/`**: Data access objects with async operations (19 repositories)
- **`tables/`**: Pydantic schemas for request/response validation
- **`schemas/`**: Additional Pydantic schemas (e.g. groups)

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