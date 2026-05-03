import pytest
from backup.main import app
from backup.dependencies.auth import get_current_user
from backup.models.models import User

def test_authority_dashboard_authenticated(client, db):
    """Test that authority dashboard is accessible."""
    user = User(full_name="Admin", email="admin@test.com", username="admin", role="authority", hashed_password="hashed")
    db.add(user)
    db.commit()
    
    app.dependency_overrides[get_current_user] = lambda: user
    
    try:
        response = client.get("/authority/dashboard")
        assert response.status_code == 200
        assert "Dashboard" in response.text
    finally:
        app.dependency_overrides.pop(get_current_user)

def test_authority_students_list(client, db):
    """Test authority students list page."""
    user = User(full_name="Admin", email="admin2@test.com", username="admin2", role="authority", hashed_password="hashed")
    db.add(user)
    db.commit()
    
    app.dependency_overrides[get_current_user] = lambda: user
    
    try:
        response = client.get("/authority/students")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(get_current_user)
