"""
Tests for Sentry Error Tracking Integration
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestSentryIntegration:
    """Test Sentry error tracking integration"""

    @patch("modules.shared.sentry.sentry_sdk")
    def test_sentry_init_when_dsn_configured(self, mock_sentry_sdk):
        """Test Sentry initialization when DSN is configured"""
        with patch.dict("os.environ", {"SENTRY_DSN": "https://test@test.ingest.sentry.io/test"}):
            # Re-import to trigger initialization
            import importlib
            import modules.shared.sentry
            importlib.reload(modules.shared.sentry)

            # Verify init was called
            mock_sentry_sdk.init.assert_called_once()

    @patch("modules.shared.sentry.sentry_sdk")
    def test_sentry_not_init_when_no_dsn(self, mock_sentry_sdk):
        """Test Sentry is not initialized when no DSN configured"""
        with patch.dict("os.environ", {}, clear=True):
            # Re-import to trigger initialization
            import importlib
            import modules.shared.sentry
            importlib.reload(modules.shared.sentry)

            # Verify init was not called
            mock_sentry_sdk.init.assert_not_called()

    @patch("modules.shared.sentry.sentry_sdk")
    def test_capture_exception_function(self, mock_sentry_sdk):
        """Test capture_exception function"""
        from modules.shared.sentry import capture_exception

        test_exception = ValueError("Test error")
        capture_exception(test_exception, user_id=123, action="test")

        mock_sentry_sdk.configure_scope.assert_called_once()
        mock_sentry_sdk.capture_exception.assert_called_once_with(test_exception)

    @patch("modules.shared.sentry.sentry_sdk")
    def test_set_user_context(self, mock_sentry_sdk):
        """Test set_user_context function"""
        from modules.shared.sentry import set_user_context

        set_user_context("user123", "user@example.com", "admin")

        mock_sentry_sdk.set_user.assert_called_once_with({
            "id": "user123",
            "email": "user@example.com",
            "role": "admin"
        })

    @patch("modules.shared.sentry.sentry_sdk")
    def test_add_breadcrumb(self, mock_sentry_sdk):
        """Test add_breadcrumb function"""
        from modules.shared.sentry import add_breadcrumb

        add_breadcrumb("Test message", "test", "info", key="value")

        mock_sentry_sdk.add_breadcrumb.assert_called_once_with(
            message="Test message",
            category="test",
            level="info",
            data={"key": "value"}
        )


class TestSentryMiddleware:
    """Test Sentry integration with FastAPI"""

    @patch("modules.shared.sentry.sentry_sdk")
    def test_sentry_enabled_in_app(self, mock_sentry_sdk, client: TestClient):
        """Test that Sentry is configured in the FastAPI app"""
        # This test verifies that the app starts without Sentry-related errors
        # The actual Sentry initialization is tested above
        response = client.get("/health/live")

        assert response.status_code == 200
        # If Sentry was misconfigured, the app might not start properly

    @patch("modules.shared.sentry.sentry_sdk")
    def test_error_capture_on_exception(self, mock_sentry_sdk, client: TestClient):
        """Test that exceptions are captured by Sentry"""
        # This would require an endpoint that raises an exception
        # For now, we verify the Sentry setup is in place

        # Mock an exception in a route that might exist
        # Since we don't have error routes yet, just verify setup
        from modules.shared.sentry import capture_exception

        test_error = RuntimeError("Test error")
        capture_exception(test_error)

        mock_sentry_sdk.configure_scope.assert_called_once()
        mock_sentry_sdk.capture_exception.assert_called_once_with(test_error)


class TestSentryDataFiltering:
    """Test Sentry data filtering functionality"""

    def test_before_send_filter_removes_sensitive_data(self):
        """Test that sensitive data is filtered from Sentry events"""
        from modules.shared.sentry import before_send_filter

        # Mock event with sensitive data
        event = {
            "request": {
                "headers": {
                    "authorization": "Bearer secret-token",
                    "x-api-key": "secret-key",
                    "content-type": "application/json"
                },
                "data": {
                    "password": "secret123",
                    "token": "auth-token",
                    "normal_field": "normal_value"
                }
            },
            "extra": {
                "password": "another-secret",
                "api_key": "key123",
                "normal_data": "keep_this"
            }
        }

        result = before_send_filter(event, None)

        # Sensitive headers should be filtered
        assert result["request"]["headers"]["authorization"] == "[FILTERED]"
        assert result["request"]["headers"]["x-api-key"] == "[FILTERED]"
        assert result["request"]["headers"]["content-type"] == "application/json"

        # Sensitive data should be filtered
        assert result["request"]["data"]["password"] == "[FILTERED]"
        assert result["request"]["data"]["token"] == "[FILTERED]"
        assert result["request"]["data"]["normal_field"] == "normal_value"

        # Extra data should be filtered
        assert result["extra"]["password"] == "[FILTERED]"
        assert result["extra"]["api_key"] == "[FILTERED]"
        assert result["extra"]["normal_data"] == "keep_this"

        # Custom tags should be added
        assert result["tags"]["service"] == "college_management_system"