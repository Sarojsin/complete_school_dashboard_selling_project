"""
Auth Integration Tests

Tests for authentication endpoints: login, signup, refresh, me
"""

import pytest
from httpx import AsyncClient
from modules.shared.models import UserRole, PortalType
from tests.factories import create_department, create_faculty


pytestmark = pytest.mark.asyncio


class TestAuthSignup:
    """Signup endpoint integration tests"""

    async def test_student_signup_success(self, async_client):
        """Test successful student signup"""
        payload = {
            "email": "teststudent@example.com",
            "username": "teststudent",
            "password": "StrongPass123!",
            "full_name": "Test Student",
            "portal_type": "college"
        }

        resp = await async_client.post("/api/v1/auth/signup/college/student", json=payload)
        assert resp.status_code == 201

        data = resp.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == payload["email"]
        assert data["user"]["role"] == "college_student"

    async def test_faculty_signup_success(self, async_client, async_db):
        """Test successful faculty signup"""
        # Create department and faculty user first for signup validation
        dept = await create_department(async_db, "Computer Science", "CS")

        payload = {
            "email": "testfaculty@example.com",
            "username": "testfaculty",
            "password": "StrongPass123!",
            "full_name": "Test Faculty",
            "portal_type": "college"
        }

        resp = await async_client.post("/api/v1/auth/signup/college/teacher", json=payload)
        assert resp.status_code == 201

        data = resp.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == payload["email"]
        assert data["user"]["role"] == "college_faculty"

    async def test_signup_duplicate_email(self, async_client):
        """Test signup with duplicate email returns 400"""
        payload = {
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "StrongPass123!",
            "full_name": "User One",
            "portal_type": "college"
        }

        # First signup
        resp1 = await async_client.post("/api/v1/auth/signup/college/student", json=payload)
        assert resp1.status_code == 201

        # Second signup with same email
        payload["username"] = "user2"
        resp2 = await async_client.post("/api/v1/auth/signup/college/student", json=payload)
        assert resp2.status_code == 400

    async def test_signup_weak_password(self, async_client):
        """Test signup with weak password"""
        payload = {
            "email": "weakpass@example.com",
            "username": "weakpass",
            "password": "123",  # Weak password
            "full_name": "Weak Pass User",
            "portal_type": "college"
        }

        resp = await async_client.post("/api/v1/auth/signup/college/student", json=payload)
        assert resp.status_code == 422  # Validation error


class TestAuthLogin:
    """Login endpoint integration tests"""

    async def test_login_success(self, async_client, async_db):
        """Test successful login returns tokens"""
        # Create a user first
        signup_payload = {
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "TestPass123!",
            "full_name": "Login User",
            "portal_type": "college"
        }

        signup_resp = await async_client.post("/api/v1/auth/signup/college/student", json=signup_payload)
        assert signup_resp.status_code == 201

        # Now login
        login_payload = {
            "username": "loginuser",
            "password": "TestPass123!"
        }

        resp = await async_client.post("/api/v1/auth/login-json", json=login_payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    async def test_login_invalid_password(self, async_client, async_db):
        """Test login with invalid password returns 401"""
        # Create a user first
        signup_payload = {
            "email": "invalidpass@example.com",
            "username": "invalidpass",
            "password": "CorrectPass123!",
            "full_name": "Invalid Pass User",
            "portal_type": "college"
        }

        signup_resp = await async_client.post("/api/v1/auth/signup/college/student", json=signup_payload)
        assert signup_resp.status_code == 201

        # Try login with wrong password
        login_payload = {
            "username": "invalidpass",
            "password": "WrongPass123!"
        }

        resp = await async_client.post("/api/v1/auth/login-json", json=login_payload)
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, async_client):
        """Test login with non-existent user returns 401"""
        login_payload = {
            "username": "nonexistent",
            "password": "SomePass123!"
        }

        resp = await async_client.post("/api/v1/auth/login-json", json=login_payload)
        assert resp.status_code == 401


class TestAuthTokens:
    """Token-related tests"""

    async def test_refresh_token_success(self, async_client, async_db):
        """Test refreshing access token"""
        # Create user and login first
        signup_payload = {
            "email": "refreshtest@example.com",
            "username": "refreshtest",
            "password": "TestPass123!",
            "full_name": "Refresh Test User",
            "portal_type": "college"
        }

        signup_resp = await async_client.post("/api/v1/auth/signup/college/student", json=signup_payload)
        assert signup_resp.status_code == 201

        login_payload = {
            "username": "refreshtest",
            "password": "TestPass123!"
        }

        login_resp = await async_client.post("/api/v1/auth/login-json", json=login_payload)
        assert login_resp.status_code == 200

        refresh_token = login_resp.json()["refresh_token"]

        # Refresh token
        refresh_payload = {"refresh_token": refresh_token}
        resp = await async_client.post("/api/v1/auth/refresh", json=refresh_payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "access_token" in data
        assert "token_type" in data

    async def test_refresh_with_invalid_token(self, async_client):
        """Test refreshing with invalid token returns 401"""
        refresh_payload = {"refresh_token": "invalid_token"}
        resp = await async_client.post("/api/v1/auth/refresh", json=refresh_payload)
        assert resp.status_code == 401


class TestAuthMe:
    """Current user endpoint tests"""

    async def test_get_current_user_success(self, async_client, async_db):
        """Test getting current user info"""
        # Create user and login
        signup_payload = {
            "email": "meuser@example.com",
            "username": "meuser",
            "password": "TestPass123!",
            "full_name": "Me User",
            "portal_type": "college"
        }

        signup_resp = await async_client.post("/api/v1/auth/signup/college/student", json=signup_payload)
        assert signup_resp.status_code == 201

        login_payload = {
            "username": "meuser",
            "password": "TestPass123!"
        }

        login_resp = await async_client.post("/api/v1/auth/login-json", json=login_payload)
        assert login_resp.status_code == 200

        access_token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 200

        data = resp.json()
        assert data["email"] == "meuser@example.com"
        assert data["full_name"] == "Me User"
        assert data["role"] == "college_student"

    async def test_get_current_user_invalid_token(self, async_client):
        """Test getting current user with invalid token returns 401"""
        headers = {"Authorization": "Bearer invalid_token"}
        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 401


class TestPortalGuard:
    """Portal guard integration tests"""

    async def test_portal_guard_existing_tests(self, async_client, create_user_and_token):
        """Run existing portal guard tests"""
        # This would run the existing test_portal_guard.py tests
        # For now, just verify college endpoints reject school tokens

        # Create school user
        school_user, school_headers = await create_user_and_token(
            role=UserRole.STUDENT,
            portal_type=PortalType.SCHOOL
        )

        # Try to access college endpoint with school token
        resp = await async_client.get("/api/v1/college/exam_section/notices", headers=school_headers)
        assert resp.status_code == 403  # Should be forbidden

        # Create college user
        college_user, college_headers = await create_user_and_token(
            role=UserRole.COLLEGE_STUDENT,
            portal_type=PortalType.COLLEGE
        )

        # Should work with college token
        resp2 = await async_client.get("/api/v1/college/exam_section/notices", headers=college_headers)
        assert resp2.status_code == 401  # Auth ok but no exam_section role