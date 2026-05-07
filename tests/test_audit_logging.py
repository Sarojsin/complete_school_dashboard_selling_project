"""
Tests for Audit Logging System
"""

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.audit import AuditLog
from modules.shared.audit_logger import AuditLogger
from modules.shared.middleware.audit_middleware import AuditLoggingMiddleware


class TestAuditLogModel:
    """Test AuditLog model"""

    def test_audit_log_creation(self):
        """Test AuditLog model can be created"""
        audit_log = AuditLog(
            user_id=1,
            action="CREATE",
            resource_type="test_resource",
            resource_id="123",
            details={"test": "data"}
        )

        assert audit_log.user_id == 1
        assert audit_log.action == "CREATE"
        assert audit_log.resource_type == "test_resource"
        assert audit_log.resource_id == "123"
        assert audit_log.details == {"test": "data"}


class TestAuditLogger:
    """Test AuditLogger functionality"""

    @pytest.fixture
    async def audit_logger(self, async_db):
        """Create audit logger instance"""
        return AuditLogger(async_db)

    @pytest.fixture
    async def sample_user(self, async_db):
        """Create a sample user for testing"""
        from modules.shared.models import User
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed",
            role="admin"
        )
        async_db.add(user)
        await async_db.commit()
        await async_db.refresh(user)
        return user

    @pytest.mark.asyncio
    async def test_log_create(self, audit_logger, sample_user):
        """Test logging a create operation"""
        audit_log = await audit_logger.log_create(
            user_id=sample_user.id,
            resource_type="test_resource",
            resource_id="123",
            new_values={"name": "test", "value": 42}
        )

        assert audit_log.user_id == sample_user.id
        assert audit_log.action == "CREATE"
        assert audit_log.resource_type == "test_resource"
        assert audit_log.resource_id == "123"
        assert audit_log.details["new_values"] == {"name": "test", "value": 42}

    @pytest.mark.asyncio
    async def test_log_update(self, audit_logger, sample_user):
        """Test logging an update operation"""
        old_values = {"name": "old_name", "value": 10}
        new_values = {"name": "new_name", "value": 42}

        audit_log = await audit_logger.log_update(
            user_id=sample_user.id,
            resource_type="test_resource",
            resource_id="123",
            old_values=old_values,
            new_values=new_values
        )

        assert audit_log.user_id == sample_user.id
        assert audit_log.action == "UPDATE"
        assert audit_log.details["old_values"] == old_values
        assert audit_log.details["new_values"] == new_values
        assert "changed_fields" in audit_log.details

    @pytest.mark.asyncio
    async def test_log_delete(self, audit_logger, sample_user):
        """Test logging a delete operation"""
        deleted_values = {"name": "deleted_item", "id": 123}

        audit_log = await audit_logger.log_delete(
            user_id=sample_user.id,
            resource_type="test_resource",
            resource_id="123",
            deleted_values=deleted_values
        )

        assert audit_log.user_id == sample_user.id
        assert audit_log.action == "DELETE"
        assert audit_log.details["deleted_values"] == deleted_values

    @pytest.mark.asyncio
    async def test_log_login(self, audit_logger, sample_user):
        """Test logging a login event"""
        audit_log = await audit_logger.log_login(
            user_id=sample_user.id,
            ip_address="192.168.1.100",
            user_agent="Test Browser"
        )

        assert audit_log.user_id == sample_user.id
        assert audit_log.action == "LOGIN"
        assert audit_log.resource_type == "user"
        assert audit_log.resource_id == str(sample_user.id)
        assert audit_log.ip_address == "192.168.1.100"
        assert audit_log.user_agent == "Test Browser"

    @pytest.mark.asyncio
    async def test_log_logout(self, audit_logger, sample_user):
        """Test logging a logout event"""
        audit_log = await audit_logger.log_logout(
            user_id=sample_user.id
        )

        assert audit_log.user_id == sample_user.id
        assert audit_log.action == "LOGOUT"
        assert audit_log.resource_type == "user"
        assert audit_log.resource_id == str(sample_user.id)

    @pytest.mark.asyncio
    async def test_log_failed_login(self, audit_logger):
        """Test logging a failed login attempt"""
        audit_log = await audit_logger.log_failed_login(
            username="baduser",
            ip_address="192.168.1.100",
            reason="invalid_password"
        )

        assert audit_log.user_id is None
        assert audit_log.action == "FAILED_LOGIN"
        assert audit_log.resource_type == "user"
        assert audit_log.resource_id == "baduser"
        assert audit_log.details["reason"] == "invalid_password"

    @pytest.mark.asyncio
    async def test_log_system_event(self, audit_logger):
        """Test logging a system event"""
        details = {"event": "backup_completed", "size": "1.2GB"}

        audit_log = await audit_logger.log_system_event(
            event_type="backup_completion",
            details=details,
            ip_address="127.0.0.1"
        )

        assert audit_log.user_id is None
        assert audit_log.action == "SYSTEM_EVENT"
        assert audit_log.resource_type == "system"
        assert audit_log.resource_id == "backup_completion"
        assert audit_log.details == details


class TestAuditMiddleware:
    """Test audit logging middleware"""

    @pytest.fixture
    def middleware(self):
        """Create middleware instance"""
        return AuditLoggingMiddleware(app=MagicMock())

    def test_exclude_paths(self, middleware):
        """Test that excluded paths are properly identified"""
        assert "/docs" in middleware.exclude_paths
        assert "/health" in middleware.exclude_paths
        assert "/api/normal" not in middleware.exclude_paths

    def test_get_client_ip_forwarded(self, middleware):
        """Test IP extraction from forwarded header"""
        from fastapi import Request
        from unittest.mock import MagicMock

        # Mock request with forwarded header
        mock_request = MagicMock()
        mock_request.headers = {"x-forwarded-for": "192.168.1.100, 10.0.0.1"}
        mock_request.client = None

        ip = middleware._get_client_ip(mock_request)
        assert ip == "192.168.1.100"

    def test_get_client_ip_real_ip(self, middleware):
        """Test IP extraction from real IP header"""
        from unittest.mock import MagicMock

        mock_request = MagicMock()
        mock_request.headers = {"x-real-ip": "10.0.0.50"}
        mock_request.client = None

        ip = middleware._get_client_ip(mock_request)
        assert ip == "10.0.0.50"

    def test_get_client_ip_direct(self, middleware):
        """Test IP extraction from direct client"""
        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_client.host = "203.0.113.1"
        mock_request = MagicMock()
        mock_request.headers = {}
        mock_request.client = mock_client

        ip = middleware._get_client_ip(mock_request)
        assert ip == "203.0.113.1"

    def test_parse_request_details_create(self, middleware):
        """Test parsing POST request details"""
        method = "POST"
        path = "/college/faculty"
        query_params = {}
        body_content = '{"name": "John Doe"}'

        resource_type, resource_id, action = middleware._parse_request_details(
            method, path, query_params, body_content
        )

        assert resource_type == "college_faculty"
        assert resource_id == "new"
        assert action == "CREATE"

    def test_parse_request_details_update(self, middleware):
        """Test parsing PUT request details"""
        method = "PUT"
        path = "/college/faculty/123"
        query_params = {}
        body_content = '{"name": "Jane Doe"}'

        resource_type, resource_id, action = middleware._parse_request_details(
            method, path, query_params, body_content
        )

        assert resource_type == "college_faculty"
        assert resource_id == "123"
        assert action == "UPDATE"

    def test_parse_request_details_delete(self, middleware):
        """Test parsing DELETE request details"""
        method = "DELETE"
        path = "/college/students/456"
        query_params = {}
        body_content = None

        resource_type, resource_id, action = middleware._parse_request_details(
            method, path, query_params, body_content
        )

        assert resource_type == "college_students"
        assert resource_id == "456"
        assert action == "DELETE"

    def test_parse_request_details_query_param_id(self, middleware):
        """Test parsing request with ID in query params"""
        method = "GET"
        path = "/college/courses"
        query_params = {"id": "789"}
        body_content = None

        resource_type, resource_id, action = middleware._parse_request_details(
            method, path, query_params, body_content
        )

        assert resource_type == "college_courses"
        assert resource_id == "789"
        assert action == "ACCESS"


class TestAuditIntegration:
    """Integration tests for audit logging in college endpoints"""

    @pytest.mark.asyncio
    async def test_faculty_creation_audit_log(self, client, create_user_and_token):
        """Test that faculty creation generates audit log"""
        # This would require setting up the full FastAPI test client
        # with middleware enabled
        pass

    @pytest.mark.asyncio
    async def test_enrollment_creation_audit_log(self, client, create_user_and_token):
        """Test that enrollment creation generates audit log"""
        # This would require setting up the full FastAPI test client
        # with middleware enabled
        pass