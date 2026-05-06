"""
Async test fixtures for college module testing (pytest-asyncio).
These fixtures provide an async database session and AsyncClient.
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

# Import both Base classes to create all tables
from modules.shared.base import Base as SharedBase
from modules.college.base import CollegeBase

# Import models to ensure they are registered with metadata
# Shared models
from modules.shared.models import User, UserRole, PortalType

# Backup college models (ensures all college tables are created)
from backup.models.college.department import Department
from backup.models.college.program import Program
from backup.models.college.semester import Semester
from backup.models.college.course import CollegeCourse
from backup.models.college.faculty import Faculty
from backup.models.college.student import CollegeStudent
from backup.models.college.enrollment import Enrollment
from backup.models.college.fee import CollegeFee
from backup.models.college.placement import Company, Job, Application, PlacementDrive
from backup.models.college.research import ResearchProject, Publication, Patent
from backup.models.college.hostel import Hostel, Room, HostelAllocation, HostelComplaint
from backup.models.college.lab import Lab, LabEquipment, LabSchedule

# New college module models
from modules.college.college_exam_section.models import CollegeExamResult, CollegeExamNotice
from modules.college.college_account_section.models import CollegeFacultyPayment
# Other college modules may be added as needed

# Set testing environment
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
    """Create an event loop for the test session (pytest-asyncio)"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_db_engine():
    """Create all tables (shared + college) in async in-memory DB"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SharedBase.metadata.create_all)
        await conn.run_sync(CollegeBase.metadata.create_all)
    yield async_engine
    await async_engine.dispose()

@pytest.fixture
async def async_db(async_db_engine):
    """Provides an async database session (per-test)"""
    async with AsyncTestingSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest.fixture
async def async_client(async_db):
    """Provides an async HTTP client with DB overrides"""
    async def override_get_db():
        yield async_db

    # Override shared and college DB dependencies
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
        password: str = "testpass123"
    ):
        repo = AuthRepository(async_db)
        if email is None:
            email = f"test_{uuid4().hex[:8]}@example.com"
        existing = await repo.get_user_by_email(email)
        if existing:
            token = create_access_token(data={"sub": str(existing.id), "role": existing.role.value})
            return existing, {"Authorization": f"Bearer {token}"}
        hashed = get_password_hash(password)
        user = User(
            email=email,
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

# College-specific entity fixtures for exam_section tests
@pytest.fixture
async def department(async_db):
    dept = Department(name="Computer Science", code="CS", description="CS Department")
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
    sem = Semester(
        name="Semester 1",
        number=1,
        program_id=program.id,
        start_date="2025-01-01",
        end_date="2025-06-01"
    )
    async_db.add(sem)
    await async_db.commit()
    await async_db.refresh(sem)
    return sem

@pytest.fixture
async def college_course(async_db, department, semester):
    course = CollegeCourse(
        code="CS101",
        name="Introduction to Programming",
        department_id=department.id,
        semester_id=semester.id,
        credits=3,
        is_active=True
    )
    async_db.add(course)
    await async_db.commit()
    await async_db.refresh(course)
    return course

@pytest.fixture
async def college_student(async_db, department, program, create_user_and_token):
    """Creates a college student with associated User and profile"""
    user, _ = await create_user_and_token(role=UserRole.COLLEGE_STUDENT)
    student = CollegeStudent(
        user_id=user.id,
        roll_number=f"ROLL{user.id}",
        program_id=program.id,
        semester_id=program.id,  # Using program.id as placeholder; tests can override
        cgpa=0.0,
        total_credits_completed=0
    )
    async_db.add(student)
    await async_db.commit()
    await async_db.refresh(student)
    return student
