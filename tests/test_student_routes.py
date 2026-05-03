import pytest
from backup.main import app
from backup.dependencies.auth import get_current_user
from backup.models.models import User, Student

def test_student_dashboard_redirect(client):
    """Test that student dashboard redirects to login when not authenticated."""
    response = client.get("/student/dashboard", follow_redirects=False)
    assert response.status_code in [302, 303, 307]
    assert response.headers["location"].endswith("/login") # Absolute URLs might be used

def test_student_dashboard_authenticated(client, db):
    """Test that student dashboard is accessible when authenticated."""
    # Create a mock user
    user = User(full_name="Test Student", email="student@test.com", username="teststudent", role="student", hashed_password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Override authentication dependency
    app.dependency_overrides[get_current_user] = lambda: user
    
    try:
        response = client.get("/student/dashboard")
        assert response.status_code == 200
        # The dashboard template might use current_user.full_name or similar
        # Since we don't have the student profile yet, it might show dashboard with default values
    finally:
        app.dependency_overrides.pop(get_current_user)

def test_student_profile_with_student_record(client, db):
    """Test student profile page with a student record."""
    user = User(full_name="Profile Student", email="profile@test.com", username="profilestudent", role="student", hashed_password="hashed")
    db.add(user)
    db.flush()
    
    student = Student(user_id=user.id, student_id="S123", grade_level="Grade 10", section="A")
    db.add(student)
    db.commit()
    
    app.dependency_overrides[get_current_user] = lambda: user
    
    try:
        response = client.get("/student/profile")
        assert response.status_code == 200
        assert "Profile Student" in response.text
        assert "S123" in response.text
    finally:
        app.dependency_overrides.pop(get_current_user)
