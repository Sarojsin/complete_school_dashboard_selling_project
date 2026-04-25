New Module Structure
We'll use the modules you listed, plus a shared module for common code.

text
modules/
├── shared/                     # Shared across all modules
│   ├── __init__.py
│   ├── base.py                 # Base model, repository, service
│   ├── auth.py                 # JWT, permissions
│   ├── config.py               # Configuration (moved from core)
│   ├── database.py             # DB session
│   ├── exceptions.py           # Common exceptions
│   └── utils.py                # Helpers
│
├── school_authority/
├── school_teacher/
├── school_student/
├── school_parent/
├── school_exam_section/
├── school_account_section/
├── school_library/
├── school_attendance/
├── college_dean/
├── college_hod/
├── college_faculty/
├── college_student/
├── college_registrar/
├── college_exam_section/
├── college_account_section/
├── college_library/
├── college_placement/
├── college_research/
├── college_hostel/
└── college_lab/
Each module will contain these files (if applicable):

models.py

schemas.py

repository.py

service.py

api.py (FastAPI routes)

web.py (Jinja2 routes)

templates/ (HTML files)

tests/ (unit/integration tests)

constants.py, exceptions.py, utils.py (if needed)

Mapping Existing Files to Modules
The mapping is complex because many files contain logic for both school and college, or combine multiple features. Below is a high‑level mapping to guide the script. You'll need to manually split files after the script runs.

Shared Core
app/core/config.py → modules/shared/config.py

app/core/database.py → modules/shared/database.py

app/core/exceptions.py → modules/shared/exceptions.py

app/core/crypto.py → modules/shared/utils.py

app/dependencies/auth.py → modules/shared/auth.py

app/models/base.py → modules/shared/base.py

app/models/models.py (User, Role) → modules/shared/models.py

app/models/chat_models.py → modules/shared/chat.py or keep separate

app/models/group_models.py → modules/shared/groups.py

School Authority
app/models/school/authority.py → modules/school_authority/models.py

app/schemas/authority.py → modules/school_authority/schemas.py

app/repositories/... – no direct authority repo; likely in admin_* repos? We'll assume it's in admin_user_repository.py. You'll need to extract.

app/services/authority_service.py → modules/school_authority/service.py

app/api/endpoints/authority.py → modules/school_authority/api.py

app/web/routers/authority.py → modules/school_authority/web.py

app/templates/authority/ → modules/school_authority/templates/

app/tests/test_authority_routes.py → modules/school_authority/tests/

School Teacher
app/models/school/teacher.py + app/models/attendance.py (if exists) → modules/school_teacher/models.py

app/schemas/teacher.py + app/schemas/attendance.py → modules/school_teacher/schemas.py

app/repositories/teacher_repository.py + app/repositories/attendance_repository.py → modules/school_teacher/repository.py

app/services/teacher_service.py + app/services/attendance_service.py → modules/school_teacher/service.py

app/api/endpoints/teachers.py + app/api/endpoints/attendance.py → modules/school_teacher/api.py

app/web/routers/teacher.py + app/web/routers/attendance.py → modules/school_teacher/web.py

app/templates/teacher/ + app/templates/attendance/ → modules/school_teacher/templates/

app/tests/test_teacher_*.py + test_attendance_*.py → modules/school_teacher/tests/

School Student
app/models/school/student.py → modules/school_student/models.py

app/schemas/student.py → modules/school_student/schemas.py

app/repositories/student_repository.py → modules/school_student/repository.py

app/services/student_service.py → modules/school_student/service.py

app/api/endpoints/students.py → modules/school_student/api.py

app/web/routers/student.py → modules/school_student/web.py

app/templates/student/ → modules/school_student/templates/

app/tests/test_student_*.py → modules/school_student/tests/

School Parent
app/models/school/parent.py → modules/school_parent/models.py

app/schemas/parent.py → modules/school_parent/schemas.py

app/repositories/parent_repository.py → modules/school_parent/repository.py

app/services/parent_service.py → modules/school_parent/service.py

app/api/endpoints/parents.py → modules/school_parent/api.py

app/web/routers/parent.py → modules/school_parent/web.py

app/templates/parent/ → modules/school_parent/templates/

app/tests/test_parent_*.py → modules/school_parent/tests/

School Exam Section
app/models/exam_models.py + app/models/test_models.py → modules/school_exam_section/models.py

app/schemas/exam_schemas.py + app/schemas/test_schemas.py → modules/school_exam_section/schemas.py

app/repositories/exam_repository.py + app/repositories/test_repository.py → modules/school_exam_section/repository.py

app/services/exam_service.py + app/services/test_service.py → modules/school_exam_section/service.py

app/api/endpoints/exam_section.py + app/api/endpoints/tests.py → modules/school_exam_section/api.py

app/web/routers/exam_section.py → modules/school_exam_section/web.py

app/templates/exam_section/ → modules/school_exam_section/templates/

app/tests/test_exam_*.py + test_test_*.py → modules/school_exam_section/tests/

School Account Section
app/models/account_models.py + app/models/school/fee.py → modules/school_account_section/models.py

app/schemas/account_schemas.py + app/schemas/fee.py → modules/school_account_section/schemas.py

app/repositories/account_repository.py + app/repositories/fee_repository.py + app/repositories/fee_structure_repository.py → modules/school_account_section/repository.py

app/services/account_service.py + app/services/fee_service.py → modules/school_account_section/service.py

app/api/endpoints/account.py + app/api/endpoints/fees.py → modules/school_account_section/api.py

app/web/routers/account.py → modules/school_account_section/web.py

app/templates/account/ → modules/school_account_section/templates/

app/tests/test_account_*.py + test_fee_*.py → modules/school_account_section/tests/

School Library
app/models/library_models.py → modules/school_library/models.py

app/schemas/library_schemas.py → modules/school_library/schemas.py

app/repositories/library_repository.py → modules/school_library/repository.py

app/services/library_service.py → modules/school_library/service.py

app/api/endpoints/library.py → modules/school_library/api.py

app/web/routers/library.py → modules/school_library/web.py

app/templates/library/ → modules/school_library/templates/

app/tests/test_library_*.py → modules/school_library/tests/

School Attendance
Since attendance is often part of teacher, you might merge it. If you want separate:

app/models/attendance.py (if exists) → modules/school_attendance/models.py

app/schemas/attendance.py → modules/school_attendance/schemas.py

app/repositories/attendance_repository.py → modules/school_attendance/repository.py

app/services/attendance_service.py → modules/school_attendance/service.py

app/api/endpoints/attendance.py → modules/school_attendance/api.py

app/web/routers/attendance.py → modules/school_attendance/web.py

app/templates/attendance/ → modules/school_attendance/templates/

College Modules (similar mapping)
You have existing files in app/models/college/, app/api/v1/college/, and some modules in app/modules/college/. These should be moved into the new module structure.

For example:

college_faculty:

app/models/college/faculty.py → modules/college_faculty/models.py

app/schemas/faculty.py (if exists) → modules/college_faculty/schemas.py

app/repositories/faculty_repository.py → modules/college_faculty/repository.py

app/services/faculty_service.py → modules/college_faculty/service.py

app/api/v1/college/faculty.py → modules/college_faculty/api.py

app/web/routers/faculty.py (if exists) → modules/college_faculty/web.py

app/templates/college/faculty/ → modules/college_faculty/templates/

college_student:

app/models/college/student.py → modules/college_student/models.py

app/api/v1/college/students.py → modules/college_student/api.py

etc.

Similar for other college modules.

Automated Migration Script
The following Python script will:

Create all module directories.

Copy files from their old locations to the new module folders.

The script does not merge files – it copies each source file as a separate file in the destination, but you can modify it to append contents (see comments). After running, you'll need to manually merge files inside each module (e.g., combine multiple models.py into one).

Important: Back up your project before running this script! Run it from the project root.

python
import os
import shutil
from pathlib import Path

# Define the new modules and their source files
# Each entry: module_name -> list of (source_path, destination_file_name)
# Destination file name is relative to module folder (e.g., "models.py")
MAPPING = {
    # Shared core
    "shared": [
        ("app/core/config.py", "config.py"),
        ("app/core/database.py", "database.py"),
        ("app/core/exceptions.py", "exceptions.py"),
        ("app/core/crypto.py", "utils.py"),
        ("app/dependencies/auth.py", "auth.py"),
        ("app/models/base.py", "base.py"),
        ("app/models/models.py", "models.py"),
        ("app/models/chat_models.py", "chat.py"),
        ("app/models/group_models.py", "groups.py"),
    ],
    # School authority
    "school_authority": [
        ("app/models/school/authority.py", "models.py"),
        ("app/schemas/authority.py", "schemas.py"),
        ("app/services/authority_service.py", "service.py"),
        ("app/api/endpoints/authority.py", "api.py"),
        ("app/web/routers/authority.py", "web.py"),
    ],
    # School teacher
    "school_teacher": [
        ("app/models/school/teacher.py", "models.py"),
        ("app/schemas/teacher.py", "schemas.py"),
        ("app/repositories/teacher_repository.py", "repository.py"),
        ("app/services/teacher_service.py", "service.py"),
        ("app/api/endpoints/teachers.py", "api.py"),
        ("app/web/routers/teacher.py", "web.py"),
    ],
    # Add all other modules following the pattern...
    # For brevity, I'll only list a few; you must complete this mapping.
}

def create_module_dirs():
    """Create all module directories."""
    modules = set()
    for module in MAPPING:
        modules.add(module)
    for module in modules:
        Path(f"modules/{module}").mkdir(parents=True, exist_ok=True)
        Path(f"modules/{module}/templates").mkdir(exist_ok=True)
        Path(f"modules/{module}/tests").mkdir(exist_ok=True)

def copy_files():
    """Copy source files to destination module folders."""
    for module, files in MAPPING.items():
        for src, dst in files:
            src_path = Path(src)
            if not src_path.exists():
                print(f"⚠️ Source not found: {src}")
                continue
            dst_path = Path(f"modules/{module}/{dst}")
            # If destination already exists, we need to merge.
            # Here we simply overwrite (last one wins). You may want to append.
            print(f"Copying {src} -> {dst_path}")
            shutil.copy2(src_path, dst_path)

def copy_templates():
    """Copy template directories for each module."""
    # School modules
    template_mapping = {
        "school_authority": "app/templates/authority",
        "school_teacher": "app/templates/teacher",
        "school_student": "app/templates/student",
        "school_parent": "app/templates/parent",
        "school_exam_section": "app/templates/exam_section",
        "school_account_section": "app/templates/account",
        "school_library": "app/templates/library",
        # Add others...
    }
    for module, src_dir in template_mapping.items():
        src = Path(src_dir)
        if src.exists():
            dst = Path(f"modules/{module}/templates")
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"Copied {src_dir} to {dst}")

def copy_tests():
    """Copy test files."""
    # Similar mapping for tests
    pass

if __name__ == "__main__":
    print("Creating module directories...")
    create_module_dirs()
    print("Copying files...")
    copy_files()
    print("Copying templates...")
    copy_templates()
    print("Done! Now manually merge files and fix imports.")
Note: The mapping above is incomplete. You need to add all modules and their source files. You can use the patterns shown to extend it.

Post‑Migration Steps
Merge files inside each module

If a module has multiple files with the same name (e.g., models.py from different sources), you must manually combine their contents into one models.py.

Remove duplicate imports, resolve conflicts.

Fix imports

Update all import statements in the moved files to use relative imports (e.g., from .models import Teacher).

Update external imports (in main.py, other modules) to import from the new module locations.

Update main.py and routers

Replace old route includes with new ones:

python
from modules.school_teacher.api import router as teacher_api_router
app.include_router(teacher_api_router, prefix="/api/v1")
Similarly for web routes.

Remove old folders

After verifying everything works, delete app/api/endpoints/, app/repositories/, app/services/, app/web/routers/, app/models/ (except maybe base), and old template folders.

Test thoroughly

Run your test suite. Many tests will need their imports updated to point to the new modules.

Additional Considerations
Admin features: You have many admin_* files. They likely belong to a central admin module (perhaps shared/admin). Decide if they should be separate modules or merged into school_authority and college_dean.

College modules: Use the existing app/models/college/ and app/api/v1/college/ files as sources.

Templates: Many templates (like base.html, index.html) should stay in the global templates/ folder. Only role‑specific templates move into module folders.

Static files: Keep global static files under static/. Module‑specific static files (if any) can go into module folders.

This migration is a large task, but breaking it down into steps and using the script to do the heavy lifting will make it manageable. Good luck!

