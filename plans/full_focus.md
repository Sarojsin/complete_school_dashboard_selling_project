You are an expert FastAPI developer. I have a school/college management system that has been refactored from a monolithic backup into a new modular structure. The backup contains all original endpoints, models, schemas, repositories, and services. The new structure is located under modules/ with separate folders for school/, college/, auth/, super_admin/, and shared/. Each module must follow the standard file pattern:

text
modules/<domain>/<module_name>/
├── __init__.py
├── models.py          # SQLAlchemy models – inherit from modules.shared.base.Base
├── schemas.py         # Pydantic models for request/response
├── repository.py      # Async CRUD operations – uses session injected via Depends(get_db)
├── service.py         # Business logic – uses repository and permissions (current_user role)
├── router.py          # FastAPI endpoints – uses Depends(get_current_user) and Depends(get_db)
├── constants.py       # Module constants (optional)
├── exceptions.py      # Module-specific exceptions (optional)
├── utils.py           # Helper functions (optional)
├── templates/         # (not used now – for later React migration)
└── tests/             # Unit/integration tests (optional)
The shared infrastructure is already implemented in:

modules/shared/base.py – declarative base

modules/shared/database.py – async engine and get_db dependency

modules/shared/config.py – settings

modules/shared/models.py – User, Role models

modules/shared/auth.py – password hashing, JWT helpers

modules/shared/dependencies.py – get_current_user, get_current_super_admin

Your task is to complete every module in modules/school/ and modules/college/ (and the auth/super_admin modules if needed) by generating all the missing code files. Use the original backup code (located in backup/) as the source of truth. The backup contains the old endpoints, services, repositories, models, and schemas.

Step‑by‑step instructions
Analyze the backup to understand what functionality belongs to each module. The backup endpoints are documented in backup_all_endpoints.md (attached). Use that to map endpoints to the correct new module.

For each module, follow this pattern:

models.py

Copy the relevant SQLAlchemy model(s) from the backup models.

Change the base class to Base from modules.shared.base.

Use import from modules.shared.base import Base.

Do not create a new engine or session – only define tables.

Use __tablename__ and ensure all columns are correctly typed.

For foreign keys to other modules, use string references (e.g., 'Teacher.id') to avoid circular imports.

schemas.py

Copy the corresponding Pydantic schemas from the backup schemas.

Replace any old imports (e.g., from app.schemas.xxx) with relative imports or from modules.shared.

Use from pydantic import BaseModel and alias orm_mode = True if needed.

repository.py

Implement async CRUD methods for the module’s model(s).

The repository should accept an AsyncSession in its constructor.

All methods must be async def.

Use SQLAlchemy async syntax: await session.execute(select(...)), await session.commit(), etc.

Do not put business logic here – only data access.

service.py

Implement business logic using the repository.

The service constructor should accept the repository (or the session to create the repository).

Methods should be async def.

Add permission checks using the current_user (injected later) – but permissions can also be enforced in the router. For now, include basic if current_user.role not in ... logic.

Use modules.shared.exceptions for custom errors.

router.py

Define FastAPI endpoints (GET, POST, PUT, DELETE) using the service.

Use Depends(get_current_user) to protect endpoints.

Use Depends(get_db) to obtain a database session.

For endpoints that require specific roles (e.g., only authority can delete a course), check the role in the endpoint or service.

Use the shared exception classes to return proper HTTP errors.

Register the router with a prefix (e.g., prefix="/teachers") and tags.

__init__.py – optionally expose the main classes (router, service, etc.).

Handle cross‑module dependencies correctly. For example, a teacher module may need to import Student from school_student. Use absolute imports: from modules.school.student.models import Student. Avoid circular imports by placing imports inside functions if necessary.

Convert all database operations to async. The old code may contain synchronous SQLAlchemy calls – rewrite them to async (e.g., session.query(...) → await session.execute(select(...))).

Update all imports to the new locations. Do not leave any from backup.xxx or from app.xxx imports. Use relative imports for files inside the same module, and absolute imports from other modules.

Implement only the endpoints that belong to the module. For example, the school_teacher module should only contain endpoints related to teacher profiles, not endpoints for courses or grades. Those should be in their own modules (school_courses, school_grades, etc.).

Add missing modules that are not yet created. The following school modules are essential and should be created if missing:

school_authority

school_teacher

school_student

school_parent

school_exam_section

school_account_section

school_library

school_attendance

school_courses

school_assignments

school_grades

school_tests

school_notices

school_groups

school_chat

school_timetable

school_notes

school_videos

For college, create corresponding modules (e.g., college_faculty, college_student, college_hod, college_dean, college_registrar, college_exam_section, college_account_section, college_library, college_placement, college_research, college_hostel, college_lab, college_programs, college_semesters, college_courses).

Generate code for the auth module if it is incomplete. It should include login, refresh token, and signup endpoints. Use the shared User model.

Generate code for the super_admin module with endpoints for system management (users, settings, backups, audit logs, etc.). These should be protected by get_current_super_admin.

Do not copy the old Jinja2 web routes – those are for the backend‑rendered pages and will be replaced by React. Focus only on the REST API endpoints.

After generating the code, provide a summary of which modules were updated or created, and note any assumptions made.

Please generate the code for each module one by one, starting with school_teacher (the pilot module) so I can verify the pattern. After that, continue with the remaining modules in the order listed above.

I will provide the content of the backup files as needed. For now, assume you have access to the backup/ directory. Let me know if you need me to attach specific files.