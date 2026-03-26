school_management_system/
├── 📂 alembic/
│   ├── 📂 versions/
│   │   └── 🐍 22683032b580_initial_migration.py
│   ├── 📄 README
│   ├── 🐍 env.py
│   └── 📄 script.py.mako
├── 📱 app/
│   ├── 🐍 __init__.py
│   └── 🐍 main.py
├── 📂 backup/
│   ├── 🔌 api/
│   │   ├── 📂 deps/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 admin.py
│   │   ├── 📂 endpoints/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 account.py
│   │   │   ├── 🐍 admin_academic.py
│   │   │   ├── 🐍 admin_advanced.py
│   │   │   ├── 🐍 admin_backup.py
│   │   │   ├── 🐍 admin_dashboard.py
│   │   │   ├── 🐍 admin_exams.py
│   │   │   ├── 🐍 admin_features.py
│   │   │   ├── 🐍 admin_finance.py
│   │   │   ├── 🐍 admin_media.py
│   │   │   ├── 🐍 admin_messages.py
│   │   │   ├── 🐍 admin_notices.py
│   │   │   ├── 🐍 admin_reports.py
│   │   │   ├── 🐍 admin_security.py
│   │   │   ├── 🐍 admin_settings.py
│   │   │   ├── 🐍 admin_system.py
│   │   │   ├── 🐍 admin_users.py
│   │   │   ├── 🐍 assignments.py
│   │   │   ├── 🐍 attendance.py
│   │   │   ├── 🐍 auth.py
│   │   │   ├── 🐍 authority.py
│   │   │   ├── 🐍 chat.py
│   │   │   ├── 🐍 courses.py
│   │   │   ├── 🐍 exam_section.py
│   │   │   ├── 🐍 fees.py
│   │   │   ├── 🐍 grades.py
│   │   │   ├── 🐍 group_posts.py
│   │   │   ├── 🐍 groups.py
│   │   │   ├── 🐍 hod.py
│   │   │   ├── 🐍 library.py
│   │   │   ├── 🐍 notes.py
│   │   │   ├── 🐍 notices.py
│   │   │   ├── 🐍 parents.py
│   │   │   ├── 🐍 students.py
│   │   │   ├── 📄 students.py.backup
│   │   │   ├── 🐍 teachers.py
│   │   │   ├── 🐍 tests.py
│   │   │   ├── 🐍 videos.py
│   │   │   └── 🐍 websocket_chat.py
│   │   ├── 📐 schemas/
│   │   │   ├── 📂 admin/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 academic.py
│   │   │   │   ├── 🐍 features.py
│   │   │   │   ├── 🐍 security.py
│   │   │   │   ├── 🐍 settings.py
│   │   │   │   └── 🐍 users.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 📂 v1/
│   │   │   ├── 📂 college/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 auth.py
│   │   │   │   ├── 🐍 courses.py
│   │   │   │   ├── 🐍 departments.py
│   │   │   │   ├── 🐍 enrollments.py
│   │   │   │   ├── 🐍 faculty.py
│   │   │   │   ├── 🐍 hostels.py
│   │   │   │   ├── 🐍 labs.py
│   │   │   │   ├── 🐍 placements.py
│   │   │   │   ├── 🐍 programs.py
│   │   │   │   ├── 🐍 research.py
│   │   │   │   ├── 🐍 semesters.py
│   │   │   │   └── 🐍 students.py
│   │   │   ├── 📂 endpoints/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 📂 school/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 authorities.py
│   │   │   │   ├── 🐍 parents.py
│   │   │   │   ├── 🐍 students.py
│   │   │   │   └── 🐍 teachers.py
│   │   │   └── 🐍 __init__.py
│   │   └── 🐍 __init__.py
│   ├── 🎯 core/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 config.py
│   │   ├── 🐍 crypto.py
│   │   ├── 🐍 database.py
│   │   ├── 🐍 exceptions.py
│   │   ├── 🐍 metrics.py
│   │   └── 🐍 templates.py
│   ├── 📂 dependencies/
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 auth.py
│   ├── 📂 legacy/
│   │   ├── 📐 schemas/
│   │   │   ├── 🐍 group_post_schemas.py
│   │   │   └── 🐍 group_schemas.py
│   │   ├── 📂 tables/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 chat_tables.py
│   │   │   ├── 🐍 group_post_schemas.py
│   │   │   ├── 🐍 group_schemas.py
│   │   │   ├── 🐍 tables.py
│   │   │   └── 🐍 test_tables.py
│   │   └── 📄 old_fee_routes.py.backup
│   ├── 🖼️ media/
│   │   └── 🖼️ logo2.png
│   ├── 🔐 middleware/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 csrf.py
│   │   ├── 🐍 feature_check.py
│   │   ├── 🐍 metrics.py
│   │   ├── 🐍 request_logger.py
│   │   └── 🐍 security.py
│   ├── 🗄️ models/
│   │   ├── 📂 college/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 course.py
│   │   │   ├── 🐍 department.py
│   │   │   ├── 🐍 enrollment.py
│   │   │   ├── 🐍 faculty.py
│   │   │   ├── 🐍 fee.py
│   │   │   ├── 🐍 hostel.py
│   │   │   ├── 🐍 lab.py
│   │   │   ├── 🐍 placement.py
│   │   │   ├── 🐍 program.py
│   │   │   ├── 🐍 research.py
│   │   │   ├── 🐍 semester.py
│   │   │   └── 🐍 student.py
│   │   ├── 📂 school/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 authority.py
│   │   │   ├── 🐍 class_model.py
│   │   │   ├── 🐍 fee.py
│   │   │   ├── 🐍 parent.py
│   │   │   ├── 🐍 student.py
│   │   │   └── 🐍 teacher.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 account_models.py
│   │   ├── 🐍 admin_models.py
│   │   ├── 🐍 base.py
│   │   ├── 🐍 chat_models.py
│   │   ├── 🐍 department_models.py
│   │   ├── 🐍 exam_models.py
│   │   ├── 🐍 group_models.py
│   │   ├── 🐍 library_models.py
│   │   ├── 🐍 models.py
│   │   └── 🐍 test_models.py
│   ├── 📂 modules/
│   │   ├── 📂 college/
│   │   │   ├── 📂 account_section/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 dean/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 exam_section/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 faculty/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 hod/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 hostel/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 lab/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 placement/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 program/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 registrar/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 research/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 student/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 📂 school/
│   │   │   ├── 📂 account_section/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 authority/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   └── 🐍 service.py
│   │   │   ├── 📂 exam_section/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 library/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 parent/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 student/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   ├── 📂 teacher/
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 api.py
│   │   │   │   ├── 🐍 constants.py
│   │   │   │   ├── 🐍 exceptions.py
│   │   │   │   ├── 🐍 repository.py
│   │   │   │   ├── 🐍 schemas.py
│   │   │   │   ├── 🐍 service.py
│   │   │   │   ├── 🐍 utils.py
│   │   │   │   └── 🐍 web.py
│   │   │   └── 🐍 __init__.py
│   │   └── 🐍 __init__.py
│   ├── 💼 repositories/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 account_repository.py
│   │   ├── 🐍 admin_academic_repository.py
│   │   ├── 🐍 admin_backup_repository.py
│   │   ├── 🐍 admin_exam_repository.py
│   │   ├── 🐍 admin_finance_repository.py
│   │   ├── 🐍 admin_message_repository.py
│   │   ├── 🐍 admin_notice_repository.py
│   │   ├── 🐍 admin_settings_repository.py
│   │   ├── 🐍 admin_system_repository.py
│   │   ├── 🐍 admin_user_repository.py
│   │   ├── 🐍 assignment_repository.py
│   │   ├── 🐍 attendance_repository.py
│   │   ├── 🐍 chat_repository.py
│   │   ├── 🐍 course_repository.py
│   │   ├── 🐍 dashboard_repository.py
│   │   ├── 🐍 department_repository.py
│   │   ├── 🐍 exam_repository.py
│   │   ├── 🐍 feature_repository.py
│   │   ├── 🐍 fee_repository.py
│   │   ├── 🐍 fee_structure_repository.py
│   │   ├── 🐍 grade_repository.py
│   │   ├── 🐍 group_post_repository.py
│   │   ├── 🐍 group_repository.py
│   │   ├── 🐍 library_repository.py
│   │   ├── 🐍 message_repository.py
│   │   ├── 🐍 notes_repository.py
│   │   ├── 🐍 notice_repository.py
│   │   ├── 🐍 parent_repository.py
│   │   ├── 🐍 student_repository.py
│   │   ├── 🐍 teacher_repository.py
│   │   ├── 🐍 test_repository.py
│   │   ├── 🐍 user_repository.py
│   │   └── 🐍 videos_repository.py
│   ├── 📐 schemas/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 account_schemas.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 assignment.py
│   │   ├── 🐍 attendance.py
│   │   ├── 🐍 auth.py
│   │   ├── 🐍 authority.py
│   │   ├── 🐍 college_faculty.py
│   │   ├── 🐍 college_student.py
│   │   ├── 🐍 course.py
│   │   ├── 🐍 department_schemas.py
│   │   ├── 🐍 exam_schemas.py
│   │   ├── 🐍 fee.py
│   │   ├── 🐍 grade.py
│   │   ├── 🐍 group.py
│   │   ├── 🐍 group_post.py
│   │   ├── 🐍 library_schemas.py
│   │   ├── 🐍 misc.py
│   │   ├── 🐍 notice.py
│   │   ├── 🐍 parent.py
│   │   ├── 🐍 student.py
│   │   ├── 🐍 teacher.py
│   │   └── 🐍 user.py
│   ├── 🧠 services/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 account_service.py
│   │   ├── 🐍 admin_academic_service.py
│   │   ├── 🐍 admin_backup_service.py
│   │   ├── 🐍 admin_exam_service.py
│   │   ├── 🐍 admin_finance_service.py
│   │   ├── 🐍 admin_message_service.py
│   │   ├── 🐍 admin_notice_service.py
│   │   ├── 🐍 admin_system_service.py
│   │   ├── 🐍 admin_user_service.py
│   │   ├── 🐍 attendance_service.py
│   │   ├── 🐍 auth_service.py
│   │   ├── 🐍 authority_service.py
│   │   ├── 🐍 chat_cleanup_service.py
│   │   ├── 🐍 chat_service.py
│   │   ├── 🐍 dashboard_service.py
│   │   ├── 🐍 department_service.py
│   │   ├── 🐍 exam_service.py
│   │   ├── 🐍 feature_service.py
│   │   ├── 🐍 grade_service.py
│   │   ├── 🐍 group_post_service.py
│   │   ├── 🐍 group_service.py
│   │   ├── 🐍 library_service.py
│   │   ├── 🐍 notification_service.py
│   │   ├── 🐍 parent_service.py
│   │   ├── 🐍 password_policy_service.py
│   │   ├── 🐍 student_service.py
│   │   ├── 🐍 teacher_service.py
│   │   └── 🐍 test_service.py
│   ├── 📂 shared/
│   │   ├── 📂 auth/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 dependencies.py
│   │   │   └── 🐍 jwt.py
│   │   ├── 🔐 middleware/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 csrf.py
│   │   │   ├── 🐍 feature_check.py
│   │   │   └── 🐍 security.py
│   │   ├── 🔧 utils/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 helpers.py
│   │   └── 🐍 __init__.py
│   ├── 📁 static/
│   │   ├── 📂 css/
│   │   │   ├── 🎨 admin.css
│   │   │   ├── 🎨 style.css
│   │   │   └── 🎨 test.css
│   │   ├── 📂 groups/
│   │   │   ├── 🎨 groups.css
│   │   │   └── 🎨 posts.css
│   │   ├── 📂 images/
│   │   │   └── 🖼️ default-avatar.png
│   │   ├── 📂 js/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🟨 chat.js
│   │   │   ├── 🟨 dashboard.js
│   │   │   ├── 🟨 main.js
│   │   │   └── 🟨 test_timer.js
│   │   ├── 📂 uploads/
│   │   │   ├── 📂 assignments/
│   │   │   │   └── 🖼️ 07f47ade-3552-4fd4-b411-c18cb460164e.jpg
│   │   │   ├── 📂 avatars/
│   │   │   │   ├── 🖼️ 2cc78636-5756-4ee7-8fd3-618e73a21912.jpeg
│   │   │   │   ├── 🖼️ 43ce75b3-1fca-4634-8567-b5e0b4ab43d4.jpg
│   │   │   │   ├── 🖼️ bfba1bef-2551-4bf9-9056-721be7bcded7.jpg
│   │   │   │   └── 🖼️ e4263e2a-0ec9-49e9-85e4-75c30c4ebde9.jpeg
│   │   │   ├── 📂 notes/
│   │   │   │   ├── 📄 bf72ae6d-a437-4b7f-b405-63a65f512784.pptx
│   │   │   │   └── 📄 bff963cd-e61d-49fd-9652-ac1a37137433.pptx
│   │   │   └── 📂 videos/
│   │   │       └── 🎬 de3e010f-8577-4539-b681-8a43a493427f.mp4
│   │   └── 🐍 __init__.py
│   ├── 🎨 templates/
│   │   ├── 📂 account/
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 profile.html
│   │   │   └── 🌐 record_teacher_payment.html
│   │   ├── 📂 admin/
│   │   │   ├── 🌐 academic.html
│   │   │   ├── 🌐 advanced.html
│   │   │   ├── 🌐 audit_logs.html
│   │   │   ├── 🌐 backup.html
│   │   │   ├── 🌐 communication.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 feature_detail.html
│   │   │   ├── 🌐 features.html
│   │   │   ├── 🌐 finance.html
│   │   │   ├── 🌐 media.html
│   │   │   ├── 🌐 notices.html
│   │   │   ├── 🌐 reports.html
│   │   │   ├── 🌐 security.html
│   │   │   ├── 🌐 settings.html
│   │   │   ├── 🌐 system.html
│   │   │   └── 🌐 users.html
│   │   ├── 📂 auth/
│   │   │   ├── 🌐 login.html
│   │   │   ├── 🌐 signup.html
│   │   │   ├── 🌐 signup_account.html
│   │   │   ├── 🌐 signup_admin.html
│   │   │   ├── 🌐 signup_authority.html
│   │   │   ├── 🌐 signup_exam_section.html
│   │   │   ├── 🌐 signup_hod.html
│   │   │   ├── 🌐 signup_library.html
│   │   │   ├── 🌐 signup_parent.html
│   │   │   ├── 🌐 signup_student.html
│   │   │   └── 🌐 signup_teacher.html
│   │   ├── 📂 authority/
│   │   │   ├── 🌐 add_course.html
│   │   │   ├── 🌐 add_fee.html
│   │   │   ├── 🌐 add_notice.html
│   │   │   ├── 🌐 add_student.html
│   │   │   ├── 🌐 add_teacher.html
│   │   │   ├── 🌐 analytics_v2.html
│   │   │   ├── 🌐 course_detail.html
│   │   │   ├── 🌐 courses.html
│   │   │   ├── 🌐 create_group.html
│   │   │   ├── 🌐 create_notice.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 departments.html
│   │   │   ├── 🌐 edit_course.html
│   │   │   ├── 🌐 edit_notice.html
│   │   │   ├── 🌐 edit_student.html
│   │   │   ├── 🌐 edit_teacher.html
│   │   │   ├── 🌐 fee_structure.html
│   │   │   ├── 🌐 fees.html
│   │   │   ├── 🌐 groups.html
│   │   │   ├── 🌐 manage_group.html
│   │   │   ├── 🌐 notices.html
│   │   │   ├── 🌐 reports.html
│   │   │   ├── 🌐 student_detail.html
│   │   │   ├── 🌐 students.html
│   │   │   ├── 🌐 teacher_detail.html
│   │   │   ├── 🌐 teachers.html
│   │   │   └── 🌐 view_notice.html
│   │   ├── 📂 college/
│   │   │   ├── 📂 dean/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   ├── 📂 faculty/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   ├── 📂 hostel/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   ├── 📂 placement/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   ├── 📂 research/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   ├── 📂 student/
│   │   │   │   └── 🌐 dashboard.html
│   │   │   └── 🌐 base.html
│   │   ├── 📂 exam_section/
│   │   │   ├── 🌐 create_notice.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 grade_sheet.html
│   │   │   ├── 🌐 notices.html
│   │   │   ├── 🌐 post_result.html
│   │   │   ├── 🌐 profile.html
│   │   │   └── 🌐 results.html
│   │   ├── 📂 groups/
│   │   │   ├── 🌐 create_group.html
│   │   │   ├── 🌐 edit_group.html
│   │   │   ├── 🌐 group_detail.html
│   │   │   ├── 🌐 group_list.html
│   │   │   ├── 🌐 group_posts.html
│   │   │   ├── 🌐 manage_members.html
│   │   │   ├── 🌐 new_post.html
│   │   │   └── 🌐 view_post.html
│   │   ├── 📂 hod/
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 profile.html
│   │   │   ├── 🌐 reports.html
│   │   │   ├── 🌐 sidebar.html
│   │   │   ├── 🌐 student_performance.html
│   │   │   ├── 🌐 students.html
│   │   │   └── 🌐 teachers.html
│   │   ├── 📂 library/
│   │   │   ├── 🌐 add_book.html
│   │   │   ├── 🌐 books.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 issue_book.html
│   │   │   ├── 🌐 overdue.html
│   │   │   ├── 🌐 profile.html
│   │   │   └── 🌐 return_book.html
│   │   ├── 📂 parent/
│   │   │   ├── 🌐 attendance.html
│   │   │   ├── 🌐 chat.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 grades.html
│   │   │   ├── 🌐 homework.html
│   │   │   ├── 🌐 notices.html
│   │   │   └── 🌐 profile.html
│   │   ├── 📂 school/
│   │   │   └── 🌐 base.html
│   │   ├── 📂 student/
│   │   │   ├── 🌐 assignments.html
│   │   │   ├── 🌐 assignments_detail.html
│   │   │   ├── 🌐 attendance.html
│   │   │   ├── 🌐 courses.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 exam_results.html
│   │   │   ├── 🌐 fees.html
│   │   │   ├── 🌐 forum.html
│   │   │   ├── 🌐 grades.html
│   │   │   ├── 🌐 groups.html
│   │   │   ├── 🌐 library.html
│   │   │   ├── 🌐 messages.html
│   │   │   ├── 🌐 notes.html
│   │   │   ├── 🌐 notices.html
│   │   │   ├── 🌐 profile.html
│   │   │   ├── 🌐 sidebar.html
│   │   │   ├── 🌐 take_test.html
│   │   │   ├── 🌐 teachers.html
│   │   │   ├── 🌐 test_list.html
│   │   │   ├── 🌐 test_result.html
│   │   │   ├── 🌐 timetable.html
│   │   │   └── 🌐 videos.html
│   │   ├── 📂 teacher/
│   │   │   ├── 🌐 add_grade.html
│   │   │   ├── 🌐 assignments.html
│   │   │   ├── 🌐 attendance.html
│   │   │   ├── 🌐 chat.html
│   │   │   ├── 🌐 course_detail.html
│   │   │   ├── 🌐 courses.html
│   │   │   ├── 🌐 create_assignment.html
│   │   │   ├── 🌐 create_notice.html
│   │   │   ├── 🌐 create_test.html
│   │   │   ├── 🌐 dashboard.html
│   │   │   ├── 🌐 edit_assignment.html
│   │   │   ├── 🌐 edit_test.html
│   │   │   ├── 🌐 grades.html
│   │   │   ├── 🌐 groups.html
│   │   │   ├── 🌐 messages.html
│   │   │   ├── 🌐 profile.html
│   │   │   ├── 🌐 sidebar.html
│   │   │   ├── 🌐 student_detail.html
│   │   │   ├── 🌐 student_grades.html
│   │   │   ├── 🌐 students.html
│   │   │   ├── 🌐 take_attendance.html
│   │   │   ├── 🌐 timetable.html
│   │   │   ├── 🌐 upload_notes.html
│   │   │   ├── 🌐 upload_videos.html
│   │   │   ├── 🌐 view_attendance_session.html
│   │   │   ├── 🌐 view_submissions.html
│   │   │   └── 🌐 view_tests.html
│   │   ├── 🐍 __init__.py
│   │   ├── 🌐 base.html
│   │   └── 🌐 index.html
│   ├── 🔧 utils/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 bcrypt_compat.py
│   │   ├── 🐍 constants.py
│   │   ├── 🐍 exceptions.py
│   │   └── 🐍 websocket_manager.py
│   ├── 📂 web/
│   │   ├── 📂 routers/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 account.py
│   │   │   ├── 🐍 admin.py
│   │   │   ├── 🐍 authority.py
│   │   │   ├── 🐍 common.py
│   │   │   ├── 🐍 exam_section.py
│   │   │   ├── 🐍 group_posts.py
│   │   │   ├── 🐍 groups.py
│   │   │   ├── 🐍 hod.py
│   │   │   ├── 🐍 library.py
│   │   │   ├── 🐍 parent.py
│   │   │   ├── 🐍 student.py
│   │   │   └── 🐍 teacher.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 authority_crud.py
│   │   └── 📄 routes.py.old
│   ├── 📂 websocket/
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 router.py
│   ├── 🐍 __init__.py
│   └── 🐍 main.py
├── 📚 docs/
│   └── 📝 adding_a_new_module.md
├── 🖥️ frontend/
│   ├── 🌍 public/
│   │   ├── 🖌️ favicon.svg
│   │   └── 🖌️ icons.svg
│   ├── 📦 src/
│   │   ├── 🖼️ assets/
│   │   │   ├── 🖼️ hero.png
│   │   │   ├── 🖌️ react.svg
│   │   │   └── 🖌️ vite.svg
│   │   ├── 📂 modules/
│   │   │   ├── 📂 auth/
│   │   │   │   ├── 🔌 api/
│   │   │   │   │   └── 🟨 auth.js
│   │   │   │   ├── 📄 pages/
│   │   │   │   │   └── ⚛️ LoginPage.jsx
│   │   │   │   └── 🎨 styles/
│   │   │   │       └── 🎨 auth.css
│   │   │   ├── 📂 collage/
│   │   │   │   ├── 📂 collage_placement/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ StudentDashboard.jsx
│   │   │   │   └── 📂 collage_teacher/
│   │   │   │       ├── 🔌 api/
│   │   │   │       │   └── 🟨 teachers.js
│   │   │   │       └── 📄 pages/
│   │   │   │           └── ⚛️ TeacherDashboard.jsx
│   │   │   ├── 📂 school/
│   │   │   │   ├── 📂 school_authority/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ AuthorityDashboard.jsx
│   │   │   │   ├── 📂 school_student/
│   │   │   │   │   ├── 🔌 api/
│   │   │   │   │   │   └── 🟨 students.js
│   │   │   │   │   └── 📄 pages/
│   │   │   │   │       └── ⚛️ StudentDashboard.jsx
│   │   │   │   └── 📂 school_teacher/
│   │   │   │       ├── 🔌 api/
│   │   │   │       │   └── 🟨 teachers.js
│   │   │   │       └── 📄 pages/
│   │   │   │           └── ⚛️ TeacherDashboard.jsx
│   │   │   ├── 📂 shared/
│   │   │   │   ├── 🔌 api/
│   │   │   │   │   └── 🟨 client.js
│   │   │   │   ├── 🧩 components/
│   │   │   │   │   ├── ⚛️ Button.jsx
│   │   │   │   │   ├── ⚛️ DataTable.jsx
│   │   │   │   │   ├── ⚛️ Modal.jsx
│   │   │   │   │   └── ⚛️ PrivateRoute.jsx
│   │   │   │   ├── 🪝 hooks/
│   │   │   │   │   └── 🟨 useAuth.js
│   │   │   │   ├── 📂 layouts/
│   │   │   │   │   ├── ⚛️ AuthLayout.jsx
│   │   │   │   │   └── ⚛️ MainLayout.jsx
│   │   │   │   ├── 🎨 styles/
│   │   │   │   │   └── 🎨 global.css
│   │   │   │   └── 🔧 utils/
│   │   │   │       └── 🟨 dateFormatter.js
│   │   │   └── 📂 super_admin/
│   │   │       ├── 🔌 api/
│   │   │       │   └── 🟨 students.js
│   │   │       └── 📄 pages/
│   │   │           └── ⚛️ SuperAdminDashboard.jsx
│   │   ├── 🎨 App.css
│   │   ├── ⚛️ App.jsx
│   │   ├── 🎨 index.css
│   │   └── 🚀 main.jsx
│   ├── 📄 .gitignore
│   ├── 📝 README.md
│   ├── 🟨 eslint.config.js
│   ├── 🌐 index.html
│   ├── 🧾 package-lock.json
│   ├── 📦 package.json
│   └── ⚡ vite.config.js
├── 📂 modules/
│   ├── 📂 auth/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 api.py
│   │   ├── 🐍 dependencies.py
│   │   ├── 🐍 repository.py
│   │   ├── 🐍 router.py
│   │   ├── 🐍 schemas.py
│   │   ├── 🐍 service.py
│   │   └── 🐍 utils.py
│   ├── 📂 collage/
│   │   ├── 📂 college_account_section/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_dean/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_exam_section/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_faculty/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 college_hod/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_hostel/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_lab/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_library/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 college_placement/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_registrar/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   ├── 📂 college_research/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 api.py
│   │   └── 📂 college_student/
│   │       ├── 🎨 templates/
│   │       │   └── 🐍 __init__.py
│   │       ├── 🧪 tests/
│   │       │   └── 🐍 __init__.py
│   │       ├── 🐍 __init__.py
│   │       ├── 🐍 api.py
│   │       ├── 🐍 constants.py
│   │       ├── 🐍 exceptions.py
│   │       ├── 🐍 models.py
│   │       ├── 🐍 repository.py
│   │       ├── 🐍 schemas.py
│   │       ├── 🐍 service.py
│   │       ├── 🐍 utils.py
│   │       └── 🐍 web.py
│   ├── 📂 school/
│   │   ├── 📂 school_account_section/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_assignments/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_attendance/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_authority/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_chat/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_courses/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_dashboard/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_exam_section/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_grades/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_groups/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_library/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_notes/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_notices/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_parent/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_student/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_teacher/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_tests/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   ├── 📂 school_timetable/
│   │   │   ├── 🎨 templates/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🧪 tests/
│   │   │   │   └── 🐍 __init__.py
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 api.py
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 repository.py
│   │   │   ├── 🐍 router.py
│   │   │   ├── 🐍 schemas.py
│   │   │   ├── 🐍 service.py
│   │   │   ├── 🐍 utils.py
│   │   │   └── 🐍 web.py
│   │   └── 📂 school_videos/
│   │       ├── 🎨 templates/
│   │       │   └── 🐍 __init__.py
│   │       ├── 🧪 tests/
│   │       │   └── 🐍 __init__.py
│   │       ├── 🐍 __init__.py
│   │       ├── 🐍 api.py
│   │       ├── 🐍 constants.py
│   │       ├── 🐍 exceptions.py
│   │       ├── 🐍 models.py
│   │       ├── 🐍 repository.py
│   │       ├── 🐍 router.py
│   │       ├── 🐍 schemas.py
│   │       ├── 🐍 service.py
│   │       ├── 🐍 utils.py
│   │       └── 🐍 web.py
│   ├── 📂 shared/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 auth.py
│   │   ├── 🐍 auth_utils.py
│   │   ├── 🐍 base.py
│   │   ├── 🐍 config.py
│   │   ├── 🐍 database.py
│   │   ├── 🐍 exceptions.py
│   │   ├── 🐍 feature_guard.py
│   │   ├── 🐍 health.py
│   │   ├── 🐍 logger.py
│   │   ├── 🐍 models.py
│   │   └── 🐍 utils.py
│   ├── 📂 super_admin/
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 api.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 repository.py
│   │   ├── 🐍 schemas.py
│   │   └── 🐍 service.py
│   └── 🐍 __init__.py
├── 📂 plans/
│   ├── 📝 Converting_All_Roles_to_React_with_Modular_Structure.md
│   ├── 📝 School_vs_College_mode.md
│   ├── 📝 admin.md
│   ├── 📝 admin_feature_control_plan.md
│   ├── 📝 all_school_modules_migration_plan.md
│   ├── 📝 collage.md
│   ├── 📝 elite_migration.md
│   ├── 📝 elite_plan1.md
│   ├── 📝 elite_plan10.md
│   ├── 📝 elite_plan11.md
│   ├── 📝 elite_plan12.md
│   ├── 📝 elite_plan2.md
│   ├── 📝 elite_plan3.md
│   ├── 📝 elite_plan4.md
│   ├── 📝 elite_plan5.md
│   ├── 📝 elite_plan6.md
│   ├── 📝 elite_plan7.md
│   ├── 📝 elite_plan8.md
│   ├── 📝 elite_plan9.md
│   ├── 📝 migration_phase1.md
│   ├── 📝 migration_phase2.md
│   ├── 📝 migration_phase3.md
│   ├── 📝 migration_phase4.md
│   ├── 📝 migration_phase5.md
│   ├── 📝 migration_phase6.md
│   ├── 📝 migration_phase7.md
│   ├── 📝 migration_phase8.md
│   ├── 📝 migration_plan.md
│   ├── 📝 new_structure.md
│   ├── 📝 phase1_implementation_breakdown.md
│   ├── 📝 phase2_implementation_breakdown.md
│   ├── 📝 phase3_implementation_breakdown.md
│   ├── 📝 phase4_implementation_breakdown.md
│   ├── 📝 phase5_implementation_breakdown.md
│   ├── 📝 school.md
│   ├── 📝 school_account_section_migration_plan.md
│   ├── 📝 school_analytics_migration_plan.md
│   ├── 📝 school_assignments_migration_plan.md
│   ├── 📝 school_attendance_migration_plan.md
│   ├── 📝 school_authority_migration_plan.md
│   ├── 📝 school_chat_migration_plan.md
│   ├── 📝 school_chat_section_migration_plan.md
│   ├── 📝 school_collage_structure.md
│   ├── 📝 school_courses_migration_plan.md
│   ├── 📝 school_dashboard_migration_plan.md
│   ├── 📝 school_exam_section_migration_plan.md
│   ├── 📝 school_fee_structure_migration_plan.md
│   ├── 📝 school_fees_migration_plan.md
│   ├── 📝 school_grades_migration_plan.md
│   ├── 📝 school_group_section_migration_plan.md
│   ├── 📝 school_groups_migration_plan.md
│   ├── 📝 school_library_migration_plan.md
│   ├── 📝 school_notes_migration_plan.md
│   ├── 📝 school_notices_migration_plan.md
│   ├── 📝 school_parent_migration_plan.md
│   ├── 📝 school_reports_migration_plan.md
│   ├── 📝 school_student_migration_plan.md
│   ├── 📝 school_teacher_migration_plan.md
│   ├── 📝 school_tests_migration_plan.md
│   ├── 📝 school_timetable_migration_plan.md
│   ├── 📝 school_videos_migration_plan.md
│   ├── 📝 separate_database_architecture1.md
│   ├── 📝 separate_database_architecture2.md
│   └── 📝 transformation_status.md
├── 📂 rules/
│   ├── 📝 coding_rules.md
│   ├── 📝 frontend_react_rules.md
│   └── 📝 moving_code_rules.md
├── 📜 scripts/
│   ├── 📂 check/
│   │   ├── 🐍 check_db_enum.py
│   │   ├── 🐍 check_db_teachers.py
│   │   ├── 🐍 check_enum.py
│   │   ├── 🐍 check_enum_values.py
│   │   ├── 🐍 check_integrity.py
│   │   ├── 🐍 check_local_db.py
│   │   ├── 🐍 check_role_type.py
│   │   ├── 🐍 check_schema.py
│   │   ├── 🐍 check_test.py
│   │   ├── 🐍 check_users.py
│   │   ├── 🐍 list_courses.py
│   │   ├── 🐍 list_users.py
│   │   ├── 🐍 raw_list_courses.py
│   │   ├── 🐍 raw_list_users.py
│   │   ├── 🐍 test_auth.py
│   │   └── 🐍 test_teacher_lookup.py
│   ├── 📂 debug/
│   │   ├── 🐍 debug_access.py
│   │   ├── 🐍 debug_enrollments.py
│   │   ├── 🐍 debug_teacher_repo.py
│   │   ├── 🐍 debug_test_questions.py
│   │   ├── 🐍 debug_tests.py
│   │   ├── 🐍 debug_visibility.py
│   │   ├── 🐍 final_debug.py
│   │   └── 🐍 simple_debug.py
│   ├── 📂 fix/
│   │   ├── 🐍 fix_authority_urls.py
│   │   ├── 🐍 fix_imports_bulk.py
│   │   ├── 🐍 fix_main.py
│   │   ├── 🐍 fix_null_bytes.py
│   │   ├── 🐍 fix_student_urls.py
│   │   └── 🐍 inject_csrf.py
│   ├── 🗃️ migrations/
│   │   ├── 🐍 add_admin_role.py
│   │   ├── 🐍 add_admin_security_tables.py
│   │   ├── 📄 add_name_columns.sql
│   │   ├── 🐍 add_parent_id_to_students.py
│   │   ├── 📄 add_parent_to_enum.sql
│   │   ├── 🐍 add_target_classes_column.py
│   │   ├── 🐍 drop_column.py
│   │   ├── 🐍 migrate_attendance.py
│   │   ├── 🐍 migrate_grades.py
│   │   ├── 🐍 migrate_profile_pic.py
│   │   ├── 🐍 migrate_role_modules.py
│   │   ├── 🐍 migrations_add_messages.py
│   │   └── 🐍 run_add_name_migration.py
│   ├── 📂 setup/
│   │   ├── 🐍 add_parent_enum.py
│   │   ├── 🐍 create_assignment_test_data.py
│   │   ├── 🐍 create_messages_table.py
│   │   ├── 🐍 create_signup_student.py
│   │   ├── 🐍 create_test_parent.py
│   │   ├── 🐍 create_test_users.py
│   │   ├── 🐍 create_user.py
│   │   ├── 🐍 seed_courses.py
│   │   ├── 🐍 seed_features.py
│   │   └── 🐍 setup_database.py
│   ├── 📂 temp/
│   │   ├── 🐍 authority_routes_complete.py
│   │   ├── 📄 fail_output.txt
│   │   ├── 📄 main.py.backup
│   │   ├── 🐍 reproduce_enum.py
│   │   ├── 📄 routes.txt
│   │   ├── 🐍 temp_routes.py
│   │   ├── 🐍 temp_routes_2.py
│   │   ├── 🐍 temp_routes_3.py
│   │   ├── 📄 test_output.txt
│   │   └── 📄 test_output_2.txt
│   ├── 🔧 utils/
│   │   └── 🐍 generate_tree.py
│   ├── 📂 verify/
│   │   ├── 🐍 debug_filter.py
│   │   ├── 🐍 inspect_routes.py
│   │   ├── 🐍 verify_authority_search.py
│   │   ├── 🐍 verify_cleanup.py
│   │   ├── 🐍 verify_endpoints.py
│   │   ├── 🐍 verify_fix.py
│   │   └── 🐍 verify_groups.py
│   ├── 🐍 benchmark.py
│   ├── 🐍 check_alerts.py
│   ├── 🐍 compare_benchmarks.py
│   ├── 🐍 data_inventory.py
│   ├── 🐍 detect_n_plus_one.py
│   ├── 🐍 locustfile.py
│   ├── 🐍 rollback.py
│   └── 🐍 setup_new_roles.py
├── 🧪 tests/
│   ├── 🐍 conftest.py
│   ├── 🐍 test_add_course.py
│   ├── 🐍 test_add_student_form.py
│   ├── 🐍 test_auth_api_only.py
│   ├── 🐍 test_auth_fix.py
│   ├── 🐍 test_authority_routes.py
│   ├── 🐍 test_bcrypt.py
│   ├── 🐍 test_chat_simple.py
│   ├── 🐍 test_course_search.py
│   ├── 🐍 test_delete_route.py
│   ├── 🐍 test_fee_structure.py
│   ├── 🐍 test_login_signup.py
│   ├── 🐍 test_name_fields.py
│   ├── 🐍 test_parent_all_teachers.py
│   ├── 🐍 test_parent_chat.py
│   ├── 🐍 test_parent_dashboard.py
│   ├── 🐍 test_parent_endpoints.py
│   ├── 🐍 test_parent_teacher_chat.py
│   ├── 🐍 test_refresh_flow.py
│   ├── 🐍 test_signup_api.py
│   ├── 🐍 test_student_auth.py
│   ├── 🐍 test_student_routes.py
│   ├── 🐍 test_teacher_chat.py
│   ├── 🐍 test_teacher_search.py
│   └── 🐍 test_web_basic.py
├── 📄 .env
├── 📄 .env.example
├── 📄 .gitignore
├── 📝 COMPREHENSIVE_FEATURE_DOCUMENTATION.md
├── 📄 Dockerfile
├── 📝 MIGRATION_CHANGELOG.md
├── 📝 README.md
├── 📝 RENDER_DEPLOYMENT.md
├── 📝 admin.md
├── ⚙️ alembic.ini
├── 📝 api_testing.md
├── 🐍 best_structure.py
├── 📄 build.sh
├── 🐍 check_db_enum.py
├── 🐍 check_enum.py
├── 🐍 check_hod.py
├── 🐍 check_special_roles.py
├── 🐍 check_user.py
├── 📝 complete_uidesign.md
├── 🐍 create_special_users.py
├── 📝 csrf.md
├── 📄 debug_output.txt
├── 🐍 debug_signup.py
├── 📝 deployment.md
├── 🧾 docker-compose.yml
├── 📝 enrollment_system.md
├── 📝 finally_check_list.md
├── 🐍 fix_db.py
├── 📝 group.md
├── 📝 guide.md
├── 📝 issue_to_solve.md
├── 📝 issued_by_claud.md
├── 📝 know_about_project.md
├── 📝 lets_go.md
├── 📝 lets_go2.md
├── 📝 logic_feature.md
├── 📄 login_trace.txt
├── 📄 login_trace_utf8.txt
├── 🐍 main.py
├── 📄 makefile
├── 📝 model.md
├── 📝 model_plan.md
├── 📝 new.md
├── 📝 new_roles.md
├── 📄 output.txt
├── 📝 plan.md
├── 📝 plan_implemented.md
├── 📄 plan_to_do.txt
├── 📝 problem.md
├── 📝 production_ready.md
├── 📝 project_detail_emplimenting_plan.md
├── 📝 project_report.md
├── 📝 project_structure.md
├── ⚙️ pytest.ini
├── 📝 quick_Solve_issue_API.md
├── 📝 quickstart.md
├── 🧾 render.yaml
├── 📄 requirements.txt
├── 📝 roadmap_to_10.md
├── 🐍 run.py
├── 🗄️ school.db
├── 📄 school_db.sqlite
├── 📝 security.md
├── 🐍 seed.py
├── 📜 server_error.log
├── 🐍 simulate_login.py
├── 📝 test.md
├── 🐍 test_db_debug.py
├── 🐍 test_signups.py
├── 📝 things_to_add_on security.md
├── 📝 things_we_learn_by_this_project.md
├── 🐍 update_db_enum.py
├── 🐍 verify_changes.py
└── 🐍 verify_login_page.py
