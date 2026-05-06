import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient
from typing import Generator

from app.main import app
from modules.shared.base import Base
from modules.shared.database import get_db
from modules.shared.models import User
from modules.school.school_student.models import Student
from modules.school.school_teacher.models import Teacher
from modules.school.school_courses.models import SchoolCourse as Course
from modules.school.school_assignments.models import Assignment, AssignmentSubmission
from modules.school.school_notices.models import Notice
# from modules.school.school_attendance.models import Attendance  # Not needed; skip due to complex deps
from modules.school.school_grades.models import Grade
from modules.school.school_notes.models import Note
from modules.school.school_videos.models import Video
# from modules.school.school_account_section.models import FeeRecord  # Not needed
from modules.school.school_groups.models import Group
# Additional imports to satisfy foreign key dependencies
from modules.school.school_parent.models import SchoolParent
from modules.school.school_authority.models import SchoolAuthority

# Set testing environment variable
os.environ["TESTING"] = "True"

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    print(f"Tables in Base: {list(Base.metadata.tables.keys())}")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine) -> Generator:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

from fastapi.testclient import TestClient

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


