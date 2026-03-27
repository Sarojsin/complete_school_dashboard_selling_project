Rule File: Moving Code from backup/ to modules/
This document defines the strict rules that must be followed whenever moving code from the old monolithic structure (preserved in backup/) into the new modular architecture under modules/. Following these rules ensures consistency, avoids import errors, and keeps the system maintainable.

1. Directory Structure Conventions
Each module resides under modules/<module_name>/.
The module name should reflect its feature (e.g., school_teacher, auth, shared).

Every module must contain the following files if they exist in the backup:

models.py – SQLAlchemy models

schemas.py – Pydantic schemas (request/response)

repository.py – Database CRUD operations

service.py – Business logic

api.py – FastAPI route handlers (REST endpoints)

web.py – Jinja2 route handlers (if still used)

constants.py – Module‑specific constants (optional)

exceptions.py – Module‑specific exceptions (optional)

utils.py – Helper functions (optional)

templates/ – HTML templates (if any)

tests/ – Unit/integration tests

Exception: The shared/ module may have additional files like base.py, database.py, config.py, etc.

2. Import Rules
All imports must be relative to the module or to modules.shared.

Inside a module, import local files with relative imports:
from .models import Teacher
from .schemas import TeacherCreate

Import from other modules using absolute imports:
from modules.shared.base import Base
from modules.auth.dependencies import get_current_user

Never use absolute imports that start with app. or backup. in the new modules.

Never import from backup/ after the file has been moved.

3. Base Classes and Shared Resources
All SQLAlchemy models must inherit from modules.shared.base.Base.

Database sessions must be obtained via modules.shared.database.get_db (async).

Configuration must be accessed through modules.shared.config.settings.

Common exceptions must be raised from modules.shared.exceptions.

Password hashing and JWT utilities must be used from modules.shared.auth_utils.

4. Moving a Module – Step‑by‑Step
Identify source files in backup/ that belong to the module (use the mapping in model_plan.md).

Copy the files into the module’s folder (preserve file names as needed, but merge multiple files into a single one where appropriate).

Fix imports inside the copied files:

Replace from app.core.config with from modules.shared.config

Replace from app.core.database with from modules.shared.database

Replace from app.models.base with from modules.shared.base

Replace from app.models.models with from modules.shared.models

Replace from app.models.school.xxx with from .models (if the file is models.py)

Replace from app.repositories.xxx with from .repository (if the file is repository.py)

Replace from app.services.xxx with from .service (if the file is service.py)

Replace from app.api.endpoints.xxx with from .api

Replace from app.web.routers.xxx with from .web

Merge multiple source files if necessary (e.g., exam_models.py + test_models.py → models.py). Do this manually, removing duplicates and ensuring all classes are included.

Update models to inherit from the correct Base:

python
from modules.shared.base import Base
class Teacher(Base):
    __tablename__ = "teachers"
    ...
Update repository to use async sessions and proper dependency injection:

python
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Teacher

class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_all(self):
        ...
Update service to accept the repository and use await:

python
from .repository import TeacherRepository
class TeacherService:
    def __init__(self, repo: TeacherRepository):
        self.repo = repo
    async def get_all(self):
        return await self.repo.get_all()
Update API router to use Depends for dependencies:

python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user
from .repository import TeacherRepository
from .service import TeacherService

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/")
async def get_teachers(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    repo = TeacherRepository(db)
    service = TeacherService(repo)
    return await service.get_all()
Remove the original files from backup/ only after the module is fully functional and tested (optional, but keeps the backup clean).

Run the app and test the endpoints.

5. Dependencies Between Modules
If a module needs to use another module’s models or services, import them using absolute imports:
from modules.school_student.models import Student

Avoid circular imports. If two modules need each other, consider moving the shared code to modules/shared/.

6. Common Pitfalls to Avoid
❌ Leaving old imports – always check after copying.

❌ Mixing relative and absolute imports – be consistent.

❌ Forgetting to use async/await – all database operations are async.

❌ Hardcoding secrets – use modules.shared.config.settings.

❌ Copying files without merging – this leaves fragmented logic.

❌ Overwriting existing module files – always merge or review before replacing.

7. Validation After Migration
Before considering a module “ready”, run these checks:

All files in the module have correct imports.

python -c "from modules.<module_name>.models import *" runs without errors.

python -c "from modules.<module_name>.repository import *" works.

The FastAPI app starts (uvicorn app.main:app --reload) with the module’s router registered.

The endpoints respond as expected (use Postman or curl).

Database operations (insert, update, delete) work correctly.

8. Final Cleanup
Once all modules are migrated and the system is stable:

Delete the backup/ folder (or archive it).

Remove any leftover old code that might still be in the Python path.

