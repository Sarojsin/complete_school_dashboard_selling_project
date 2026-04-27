Step-by-Step Migration Plan: Keep Old Files, Build New Modules
Your goal is to keep your existing codebase intact inside an old/ folder while building the new modular system in modules/. This approach gives you a safety net and lets you gradually transition.

1. Backup & Create old/
bash
# Backup the whole project (just in case)
cp -r school_management_system school_management_system_backup

# Create old folder and move all old app content there
mkdir old
mv app old/app
Now your project root looks like:

text
school_management_system/
├── old/
│   └── app/            # all your old code
├── modules/            # your new modules (partially built)
├── tests/
├── scripts/
├── ...
└── main.py (maybe you have a root main.py)
Note: Keep any files that are not part of the old app (like main.py, requirements.txt, docker-compose.yml, etc.) outside old/.

2. Set Up New App Structure
Create a fresh app/ folder that will serve as the entry point for your new modular system. It will contain only the minimal files needed to bootstrap FastAPI.

bash
mkdir -p app/core
touch app/__init__.py
touch app/main.py
app/main.py (initial version):

python
from fastapi import FastAPI
from modules.shared.database import engine
from modules.shared.base import Base

app = FastAPI(title="School & College Management System")

# Import routers from modules (we'll add them later)
# from modules.school_teacher.api import router as teacher_router
# app.include_router(teacher_router, prefix="/api/v1/school")

@app.get("/")
def root():
    return {"message": "Hello World"}
3. Complete Your Modules
Your modules/ folder already has the right structure (20 modules). Now you need to populate each module with the actual code from the old files.

3.1 Module Template
Each module should eventually contain:

text
module_name/
├── __init__.py
├── models.py          # SQLAlchemy models (merged)
├── schemas.py         # Pydantic schemas (merged)
├── repository.py      # Database CRUD
├── service.py         # Business logic
├── api.py             # FastAPI routes
├── web.py             # Jinja2 routes (if you still use templates)
├── constants.py       # (optional)
├── exceptions.py      # (optional)
├── utils.py           # (optional)
├── templates/         # role‑specific HTML templates
└── tests/             # unit/integration tests
3.2 Where to Find Code for Each Module
Use the following mapping to extract code from the old files (now under old/app/).

Module	Old Files (under old/app/)
school_authority	models/school/authority.py, schemas/authority.py, repositories/... (admin_user_repository, admin_* parts), services/authority_service.py, api/endpoints/authority.py, web/routers/authority.py, templates/authority/
school_teacher	models/school/teacher.py, schemas/teacher.py, repositories/teacher_repository.py, services/teacher_service.py, api/endpoints/teachers.py, web/routers/teacher.py, templates/teacher/
school_student	models/school/student.py, schemas/student.py, repositories/student_repository.py, services/student_service.py, api/endpoints/students.py, web/routers/student.py, templates/student/
school_parent	models/school/parent.py, schemas/parent.py, repositories/parent_repository.py, services/parent_service.py, api/endpoints/parents.py, web/routers/parent.py, templates/parent/
school_exam_section	models/exam_models.py, models/test_models.py; schemas/exam_schemas.py; repositories/exam_repository.py, repositories/test_repository.py; services/exam_service.py, services/test_service.py; api/endpoints/exam_section.py, api/endpoints/tests.py; web/routers/exam_section.py; templates/exam_section/
school_account_section	models/account_models.py, models/school/fee.py; schemas/account_schemas.py, schemas/fee.py; repositories/account_repository.py, repositories/fee_repository.py, repositories/fee_structure_repository.py; services/account_service.py, services/admin_finance_service.py (school parts); api/endpoints/account.py, api/endpoints/fees.py; web/routers/account.py; templates/account/
school_library	models/library_models.py, schemas/library_schemas.py, repositories/library_repository.py, services/library_service.py, api/endpoints/library.py, web/routers/library.py, templates/library/
school_attendance	models/attendance.py (if exists), schemas/attendance.py, repositories/attendance_repository.py, services/attendance_service.py, api/endpoints/attendance.py, web/routers/attendance.py, templates/attendance/
college_faculty	models/college/faculty.py, schemas/teacher.py (faculty parts), repositories/admin_user_repository.py (faculty parts), services/admin_user_service.py (faculty parts), api/v1/college/faculty.py, templates/college/faculty/
college_student	models/college/student.py, models/college/enrollment.py; schemas/college_student.py; repositories/student_repository.py (college parts); services/student_service.py (college parts); api/v1/college/students.py; templates/college/student/
college_hod	models/college/department.py, models/department_models.py; schemas/department_schemas.py; repositories/department_repository.py; services/department_service.py; api/v1/college/hod.py; templates/college/hod/
college_dean	This role may not have dedicated models yet. You can start with a minimal module, possibly reusing college_faculty logic with a role flag.
college_registrar	Models from models/college/program.py, semester.py, course.py; schemas from schemas/course.py; repositories from repositories/course_repository.py; new service/api.
college_exam_section	Similar to school exam but with college‑specific grading. Use models/exam_models.py (college parts), services/exam_service.py (college parts), api/v1/college/exams.py (if exists).
college_account_section	models/college/fee.py, repositories/fee_repository.py (college parts), services/admin_finance_service.py (college parts).
college_library	Same as school library but with college context. Could share models, but keep separate module for future divergence.
college_placement	models/college/placement.py – you'll need to build service, api, schemas from scratch.
college_research	models/college/research.py – same, need full implementation.
college_hostel	models/college/hostel.py – same.
college_lab	models/college/lab.py – same.
4. Automated Script to Move and Merge Files
Create a script that moves files into modules and merges them where needed. Since you want to keep old files, the script will copy from old/app/ to modules/. After the script runs, you’ll manually merge duplicates.

scripts/move_to_modules.py:

python
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Mapping of (source_glob, destination_module, destination_filename)
MOVE_MAP = [
    # School authority
    ("old/app/models/school/authority.py", "school_authority", "models.py"),
    ("old/app/schemas/authority.py", "school_authority", "schemas.py"),
    ("old/app/services/authority_service.py", "school_authority", "service.py"),
    ("old/app/api/endpoints/authority.py", "school_authority", "api.py"),
    ("old/app/web/routers/authority.py", "school_authority", "web.py"),
    ("old/app/templates/authority", "school_authority", "templates"),

    # School teacher
    ("old/app/models/school/teacher.py", "school_teacher", "models.py"),
    ("old/app/schemas/teacher.py", "school_teacher", "schemas.py"),
    ("old/app/repositories/teacher_repository.py", "school_teacher", "repository.py"),
    ("old/app/services/teacher_service.py", "school_teacher", "service.py"),
    ("old/app/api/endpoints/teachers.py", "school_teacher", "api.py"),
    ("old/app/web/routers/teacher.py", "school_teacher", "web.py"),
    ("old/app/templates/teacher", "school_teacher", "templates"),

    # School student
    ("old/app/models/school/student.py", "school_student", "models.py"),
    ("old/app/schemas/student.py", "school_student", "schemas.py"),
    ("old/app/repositories/student_repository.py", "school_student", "repository.py"),
    ("old/app/services/student_service.py", "school_student", "service.py"),
    ("old/app/api/endpoints/students.py", "school_student", "api.py"),
    ("old/app/web/routers/student.py", "school_student", "web.py"),
    ("old/app/templates/student", "school_student", "templates"),

    # School parent
    ("old/app/models/school/parent.py", "school_parent", "models.py"),
    ("old/app/schemas/parent.py", "school_parent", "schemas.py"),
    ("old/app/repositories/parent_repository.py", "school_parent", "repository.py"),
    ("old/app/services/parent_service.py", "school_parent", "service.py"),
    ("old/app/api/endpoints/parents.py", "school_parent", "api.py"),
    ("old/app/web/routers/parent.py", "school_parent", "web.py"),
    ("old/app/templates/parent", "school_parent", "templates"),

    # School exam section (merge multiple)
    ("old/app/models/exam_models.py", "school_exam_section", "models_exam.py"),
    ("old/app/models/test_models.py", "school_exam_section", "models_test.py"),
    ("old/app/schemas/exam_schemas.py", "school_exam_section", "schemas_exam.py"),
    ("old/app/repositories/exam_repository.py", "school_exam_section", "repository_exam.py"),
    ("old/app/repositories/test_repository.py", "school_exam_section", "repository_test.py"),
    ("old/app/services/exam_service.py", "school_exam_section", "service_exam.py"),
    ("old/app/services/test_service.py", "school_exam_section", "service_test.py"),
    ("old/app/api/endpoints/exam_section.py", "school_exam_section", "api.py"),
    ("old/app/web/routers/exam_section.py", "school_exam_section", "web.py"),
    ("old/app/templates/exam_section", "school_exam_section", "templates"),

    # School account section (merge multiple)
    ("old/app/models/account_models.py", "school_account_section", "models_account.py"),
    ("old/app/models/school/fee.py", "school_account_section", "models_fee.py"),
    ("old/app/schemas/account_schemas.py", "school_account_section", "schemas_account.py"),
    ("old/app/schemas/fee.py", "school_account_section", "schemas_fee.py"),
    ("old/app/repositories/account_repository.py", "school_account_section", "repository_account.py"),
    ("old/app/repositories/fee_repository.py", "school_account_section", "repository_fee.py"),
    ("old/app/repositories/fee_structure_repository.py", "school_account_section", "repository_fee_structure.py"),
    ("old/app/services/account_service.py", "school_account_section", "service_account.py"),
    ("old/app/api/endpoints/account.py", "school_account_section", "api.py"),
    ("old/app/web/routers/account.py", "school_account_section", "web.py"),
    ("old/app/templates/account", "school_account_section", "templates"),

    # School library
    ("old/app/models/library_models.py", "school_library", "models.py"),
    ("old/app/schemas/library_schemas.py", "school_library", "schemas.py"),
    ("old/app/repositories/library_repository.py", "school_library", "repository.py"),
    ("old/app/services/library_service.py", "school_library", "service.py"),
    ("old/app/api/endpoints/library.py", "school_library", "api.py"),
    ("old/app/web/routers/library.py", "school_library", "web.py"),
    ("old/app/templates/library", "school_library", "templates"),

    # College faculty
    ("old/app/models/college/faculty.py", "college_faculty", "models.py"),
    ("old/app/schemas/teacher.py", "college_faculty", "schemas_teacher.py"),  # extract faculty parts later
    ("old/app/api/v1/college/faculty.py", "college_faculty", "api.py"),
    ("old/app/templates/college/faculty", "college_faculty", "templates"),

    # College student
    ("old/app/models/college/student.py", "college_student", "models.py"),
    ("old/app/models/college/enrollment.py", "college_student", "models_enrollment.py"),
    ("old/app/api/v1/college/students.py", "college_student", "api.py"),
    ("old/app/templates/college/student", "college_student", "templates"),

    # College hod
    ("old/app/models/college/department.py", "college_hod", "models.py"),
    ("old/app/schemas/department_schemas.py", "college_hod", "schemas.py"),
    ("old/app/repositories/department_repository.py", "college_hod", "repository.py"),
    ("old/app/services/department_service.py", "college_hod", "service.py"),
    ("old/app/api/v1/college/hod.py", "college_hod", "api.py"),
    ("old/app/templates/college/hod", "college_hod", "templates"),

    # College exam section
    ("old/app/models/exam_models.py", "college_exam_section", "models.py"),  # but we need to split school/college parts
    ("old/app/schemas/exam_schemas.py", "college_exam_section", "schemas.py"),
    ("old/app/repositories/exam_repository.py", "college_exam_section", "repository.py"),
    ("old/app/services/exam_service.py", "college_exam_section", "service.py"),
    # etc.

    # College account section
    ("old/app/models/college/fee.py", "college_account_section", "models.py"),
    ("old/app/repositories/fee_repository.py", "college_account_section", "repository.py"),
    ("old/app/services/admin_finance_service.py", "college_account_section", "service.py"),
    ("old/app/api/v1/college/fees.py", "college_account_section", "api.py"),
    ("old/app/templates/college/account", "college_account_section", "templates"),

    # College library
    ("old/app/models/library_models.py", "college_library", "models.py"),
    ("old/app/repositories/library_repository.py", "college_library", "repository.py"),
    ("old/app/services/library_service.py", "college_library", "service.py"),
    ("old/app/api/v1/college/library.py", "college_library", "api.py"),
    ("old/app/templates/college/library", "college_library", "templates"),

    # College placement, research, hostel, lab – only models exist
    ("old/app/models/college/placement.py", "college_placement", "models.py"),
    ("old/app/models/college/research.py", "college_research", "models.py"),
    ("old/app/models/college/hostel.py", "college_hostel", "models.py"),
    ("old/app/models/college/lab.py", "college_lab", "models.py"),
]

def copy_files():
    for src_glob, module, dest_name in MOVE_MAP:
        src_path = ROOT / src_glob
        if not src_path.exists():
            print(f"⚠️ Source not found: {src_glob}")
            continue
        dest_dir = ROOT / "modules" / module
        dest_dir.mkdir(parents=True, exist_ok=True)
        if src_path.is_dir():
            # Copy entire directory
            shutil.copytree(src_path, dest_dir / dest_name, dirs_exist_ok=True)
            print(f"📁 Copied {src_glob} -> {module}/{dest_name}")
        else:
            # Copy file
            shutil.copy2(src_path, dest_dir / dest_name)
            print(f"📄 Copied {src_glob} -> {module}/{dest_name}")

if __name__ == "__main__":
    copy_files()
    print("\n✅ Copying done. Now manually merge files and fix imports.")
Run the script:

bash
python scripts/move_to_modules.py
5. Manual Merging
After the script, each module will have one or more files. For modules with multiple models_*.py files (like school_exam_section), you need to merge them into a single models.py. Similarly for schemas, repository, service.

How to merge:

Open both files in your editor.

Copy class definitions from the second file into the first, removing duplicates.

Remove any duplicate imports.

Ensure all classes inherit from the correct Base (import from modules.shared.base).

After merging, delete the extra files (e.g., models_exam.py).

Example merge for school_exam_section/models.py:

python
# models_exam.py content
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Exam(Base):
    __tablename__ = "exams"
    ...

# models_test.py content
class Test(Base):
    __tablename__ = "tests"
    ...

# After merge:
from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Exam(Base):
    __tablename__ = "exams"
    ...

class Test(Base):
    __tablename__ = "tests"
    ...
Then delete models_exam.py and models_test.py.

Repeat for all modules that have split files.

6. Update Imports Inside Modules
After merging, you need to fix imports inside each module’s files so they import from the correct locations. For example, in school_teacher/repository.py, change:

python
# Old import
from app.models.school.teacher import Teacher
to

python
# New import
from .models import Teacher
Also update imports from shared modules:

python
from modules.shared.base import Base
from modules.shared.database import get_db
You can automate some of this with a script, but manual checking is safer.

7. Update app/main.py to Use Module Routers
Now that each module has an api.py, import them in your new app/main.py:

python
from fastapi import FastAPI
from modules.school_teacher.api import router as school_teacher_router
from modules.school_student.api import router as school_student_router
# ... import all other module routers

app = FastAPI()

app.include_router(school_teacher_router, prefix="/api/v1/school", tags=["School - Teacher"])
app.include_router(school_student_router, prefix="/api/v1/school", tags=["School - Student"])
# ...
8. Handle Templates
Move role‑specific templates from old/app/templates/ into each module’s templates/ folder. Keep global templates like base.html and index.html in a top‑level templates/ folder (outside app/). You can then configure FastAPI to look in both places.

In app/main.py, set up Jinja2 to include module template folders:

python
from fastapi.templating import Jinja2Templates
import os

# Path to global templates
global_templates = Jinja2Templates(directory="templates")

# For module templates, you may need to load them on the fly or add a custom loader.
# Simplest: keep all templates under global templates and move them there.
Since you plan to use React for frontend, you might not need to keep Jinja2 templates. If you’re phasing out templates, you can skip moving them and focus on API endpoints.

9. Test the Application
After all modules are populated and imports fixed, run the application:

bash
uvicorn app.main:app --reload
Visit http://localhost:8000/docs to see if your API endpoints are registered.

Run tests:

bash
pytest tests/
You may need to update test imports to point to the new modules.

10. Gradual Cleanup
Once you’re confident the new system works, you can remove the old code:

bash
# After everything is verified
rm -rf old   # or keep as archive
But you can keep old/ indefinitely as a reference.

Summary Checklist
Backup project.

Create old/ and move app/ into it.

Create new app/ with minimal main.py.

Run the move script to copy files into modules.

Manually merge split files in each module.

Update imports inside modules to use relative imports and modules.shared.

Update app/main.py to import module routers.

Move templates (if still needed).

Run tests and fix any issues.

