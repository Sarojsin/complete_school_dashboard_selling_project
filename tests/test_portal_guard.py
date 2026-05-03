"""
Portal Guard Testing - Backend & Frontend

This test suite verifies that the require_school_portal and require_college_portal
dependencies enforce strict separation between school and college portals.

Backend Scenarios (Automated):
- A: School user cannot access college endpoints (403)
- B: College user cannot access school endpoints (403)
- Positive: School user can access school endpoints (200)
- Positive: College user can access college endpoints (200)

Frontend Scenarios (Manual - see frontend_portal_guard_manual.md):
- C: School user manually navigating to /college/student/dashboard gets redirected
- D: College user manually navigating to /school/student/dashboard gets redirected

Portal Selection Persistence (Manual + JS):
- Verify localStorage 'selectedSystem' persists across page refreshes
- Verify SignupPage uses selectedSystem to set portal_type during signup
"""

import pytest
from app.main import app
from modules.auth.dependencies import get_current_user
from modules.shared.models import PortalType
from modules.shared.exceptions import ForbiddenError

# For mocking user
from types import SimpleNamespace


@pytest.fixture
def mock_school_user():
    """Create a mock user with SCHOOL portal type."""
    return SimpleNamespace(portal_type=PortalType.SCHOOL, id=1, full_name="School User", role="student")


@pytest.fixture
def mock_college_user():
    """Create a mock user with COLLEGE portal type."""
    return SimpleNamespace(portal_type=PortalType.COLLEGE, id=2, full_name="College User", role="student")


def test_school_user_can_access_school_courses(client, mock_school_user):
    """Positive test: School user should have access to school courses endpoint."""
    app.dependency_overrides[get_current_user] = lambda: mock_school_user
    try:
        response = client.get("/api/v1/school/courses/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_college_user_can_access_college_courses(client, mock_college_user):
    """Positive test: College user should have access to college courses endpoint."""
    app.dependency_overrides[get_current_user] = lambda: mock_college_user
    try:
        response = client.get("/api/v1/college/courses/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_school_user_forbidden_from_college_courses(client, mock_school_user):
    """Scenario A: School user must be forbidden from college courses endpoint."""
    app.dependency_overrides[get_current_user] = lambda: mock_school_user
    try:
        response = client.get("/api/v1/college/courses/")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        json = response.json()
        assert "detail" in json
        # Should mention college portal
        detail = json["detail"].lower()
        assert "college" in detail or "portal" in detail, f"Detail message should mention portal mismatch: {json['detail']}"
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_college_user_forbidden_from_school_courses(client, mock_college_user):
    """Scenario B: College user must be forbidden from school courses endpoint."""
    app.dependency_overrides[get_current_user] = lambda: mock_college_user
    try:
        response = client.get("/api/v1/school/courses/")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        json = response.json()
        assert "detail" in json
        # Should mention school portal
        detail = json["detail"].lower()
        assert "school" in detail or "portal" in detail, f"Detail message should mention portal mismatch: {json['detail']}"
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_school_user_forbidden_from_college_student_endpoint(client, mock_school_user):
    """Additional check: college student endpoints are protected."""
    app.dependency_overrides[get_current_user] = lambda: mock_school_user
    try:
        response = client.get("/api/v1/college/students/")
        assert response.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_college_user_forbidden_from_school_student_endpoint(client, mock_college_user):
    """Additional check: school student endpoints are protected."""
    app.dependency_overrides[get_current_user] = lambda: mock_college_user
    try:
        response = client.get("/api/v1/school/students/")
        assert response.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# ---- Direct dependency tests ----

def test_require_portal_directly():
    """Unit test: require_portal function rejects mismatched portal types."""
    from modules.auth.dependencies import require_portal
    from modules.shared.models import PortalType

    # School portal checker
    school_checker = require_portal(PortalType.SCHOOL)
    college_user = SimpleNamespace(portal_type=PortalType.COLLEGE)
    school_user = SimpleNamespace(portal_type=PortalType.SCHOOL)

    with pytest.raises(ForbiddenError):
        school_checker(college_user)
    # Should not raise for school user
    try:
        school_checker(school_user)
    except ForbiddenError:
        pytest.fail("School user should be allowed through require_school_portal")

    # College portal checker
    college_checker = require_portal(PortalType.COLLEGE)
    with pytest.raises(ForbiddenError):
        college_checker(school_user)
    try:
        college_checker(college_user)
    except ForbiddenError:
        pytest.fail("College user should be allowed through require_college_portal")
