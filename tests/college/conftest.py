"""
Async test fixtures for college module testing (pytest-asyncio).
Provides async_db, async_client, and data factories.
"""

import pytest
import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from app.main import app
from modules.shared.database import get_db
from modules.college.database import get_college_async_db
from modules.shared.base import Base as SharedBase
from modules.college.base import CollegeBase
from modules.shared.models import User, UserRole, PortalType

# Import all college backup models to register metadata
# NOTE: Only import models that are needed and have correct FK dependencies.
# Some modules (research, hostel) have FK issues referencing non-existent "faculty" table;
# they are excluded from test DB creation.
from backup.models.college.department import Department
from backup.models.college.program import Program
from backup.models.college.semester import Semester
from backup.models.college.course import CollegeCourse
from backup.models.college.faculty import Faculty
from backup.models.college.student import CollegeStudent
from backup.models.college.enrollment import Enrollment
from backup.models.college.fee import CollegeFee
# Placement models are safe (reference college students, companies)
from backup.models.college.placement import Company, Job, Application, PlacementDrive
# Lab models (reference college_faculty correctly)
from backup.models.college.lab import Lab, LabEquipment, LabSchedule
from modules.college.college_exam_section.models import CollegeExamResult, CollegeExamNotice
from modules.college.college_account_section.models import CollegeFacultyPayment

# Ensure testing flag
os.environ.setdefault("TESTING", "True")

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

AsyncTestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop():
    """Provide event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_db_engine():
    """Create all tables (shared + college) in async in-memory DB"""
    async with async_engine.begin() as conn:
        # Ensure User table is also registered in CollegeBase metadata for FK resolution
        from modules.shared.models import User
        if "users" not in CollegeBase.metadata.tables:
            User.__table__.tometadata(CollegeBase.metadata)
        
        # Create SharedBase tables first (includes User)
        await conn.run_sync(SharedBase.metadata.create_all)
        # Now create CollegeBase tables (including those referencing users)
        await conn.run_sync(CollegeBase.metadata.create_all)
    yield async_engine
    await async_engine.dispose()

@pytest.fixture
async def async_db(async_db_engine):
    """Provides an async database session"""
    async with AsyncTestingSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest.fixture
async def async_client(async_db):
    """Provides an async HTTP client with DB overrides"""
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_college_async_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
async def create_user_and_token(async_db):
    """Factory to create a user and return auth headers"""
    from modules.auth.repository import AuthRepository
    from modules.shared.auth_utils import get_password_hash, create_access_token
    from uuid import uuid4

    async def _create_user(
        email: str = None,
        role: UserRole = UserRole.COLLEGE_STUDENT,
        portal_type: PortalType = PortalType.COLLEGE,
        password: str = "testpass123",
        username: str = None
    ):
        repo = AuthRepository(async_db)
        if email is None:
            email = f"test_{uuid4().hex[:8]}@example.com"
        if username is None:
            username = email.split("@")[0]
        existing = await repo.get_user_by_email(email)
        if existing:
            token = create_access_token(data={"sub": str(existing.id), "role": existing.role.value})
            return existing, {"Authorization": f"Bearer {token}"}
        hashed = get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed,
            full_name=f"Test {role.value}",
            role=role,
            portal_type=portal_type,
            is_active=True,
        )
        async_db.add(user)
        await async_db.commit()
        await async_db.refresh(user)
        token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        return user, {"Authorization": f"Bearer {token}"}
    return _create_user

# College entity fixtures for exam_section tests
@pytest.fixture
async def department(async_db):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    dept = Department(name=f"Computer Science {unique_id}", code=f"CS{unique_id}", description="CS Department")
    async_db.add(dept)
    await async_db.commit()
    await async_db.refresh(dept)
    return dept

@pytest.fixture
async def program(async_db, department):
    prog = Program(name="B.Tech CSE", code="CSE", department_id=department.id)
    async_db.add(prog)
    await async_db.commit()
    await async_db.refresh(prog)
    return prog

@pytest.fixture
async def semester(async_db, program):
    from datetime import date
    sem = Semester(
        name="Semester 1",
        number=1,
        program_id=program.id,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 6, 1)
    )
    async_db.add(sem)
    await async_db.commit()
    await async_db.refresh(sem)
    return sem

@pytest.fixture
async def college_course(async_db, department, semester):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    course = CollegeCourse(
        code=f"CS101_{unique_id}",
        name="Introduction to Programming",
        description="Test course",
        credits=3,
        department_id=department.id,
        semester_id=semester.id
    )
    async_db.add(course)
    await async_db.commit()
    await async_db.refresh(course)
    return course

@pytest.fixture
async def college_student(async_db, department, program, create_user_and_token):
    user, _ = await create_user_and_token(role=UserRole.COLLEGE_STUDENT)
    student = CollegeStudent(
        user_id=user.id,
        roll_number=f"ROLL{user.id}",
        program_id=program.id,
        semester_id=program.id,  # placeholder
        cgpa=0.0,
        total_credits_completed=0
    )
    async_db.add(student)
    await async_db.commit()
    await async_db.refresh(student)
    return student
