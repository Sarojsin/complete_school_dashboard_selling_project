"""
Tests for Health Check Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_live_returns_200(self, client: TestClient):
        """Test liveness check endpoint"""
        response = client.get("/health/live")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_health_ready_returns_200_when_db_ok(self, client: TestClient):
        """Test readiness check when database is healthy"""
        response = client.get("/health/ready")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "database" in data["checks"]
        assert data["checks"]["database"]["status"] == "healthy"

    @patch('modules.shared.health.HealthChecker.check_database')
    def test_health_ready_returns_503_when_db_down(self, mock_check_db, client: TestClient):
        """Test readiness check when database is unhealthy"""
        # Mock database check failure
        mock_check_db.return_value = {
            "status": "unhealthy",
            "message": "Database connection failed",
            "response_time": 0.1
        }

        response = client.get("/health/ready")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not ready"
        assert data["checks"]["database"]["status"] == "unhealthy"

    def test_health_endpoints_include_app_info(self, client: TestClient):
        """Test that health endpoints include app information"""
        response = client.get("/health/live")
        data = response.json()

        assert "status" in data

        response = client.get("/health/ready")
        data = response.json()

        assert "status" in data
        assert "app" in data
        assert "checks" in data

    @patch('modules.shared.health.HealthChecker.check_redis')
    def test_health_ready_includes_redis_when_configured(self, mock_check_redis, client: TestClient):
        """Test that Redis health check is included when configured"""
        with patch.dict('os.environ', {'REDIS_URL': 'redis://localhost:6379'}):
            mock_check_redis.return_value = {
                "status": "healthy",
                "message": "Redis connection successful",
                "response_time": 0.05
            }

            response = client.get("/health/ready")

            assert response.status_code == 200
            data = response.json()
            assert "redis" in data["checks"]
            assert data["checks"]["redis"]["status"] == "healthy"

    def test_health_ready_excludes_redis_when_not_configured(self, client: TestClient):
        """Test that Redis health check is not included when not configured"""
        response = client.get("/health/ready")

        assert response.status_code == 200
        data = response.json()

        # Redis should not be in checks if not configured
        redis_check = data["checks"].get("redis")
        if redis_check:
            assert redis_check["status"] in ["not_configured", "not_available"]


class TestHealthChecker:
    """Test HealthChecker class directly"""

    @pytest.mark.asyncio
    async def test_check_database_success(self):
        """Test successful database check"""
        from modules.shared.health import HealthChecker

        checker = HealthChecker()
        result = await checker.check_database()

        assert result["status"] == "healthy"
        assert "response_time" in result
        assert "Database connection successful" in result["message"]

    @pytest.mark.asyncio
    async def test_check_redis_not_configured(self):
        """Test Redis check when not configured"""
        from modules.shared.health import HealthChecker

        checker = HealthChecker()
        result = await checker.check_redis()

        assert result["status"] == "not_configured"
        assert "Redis not configured" in result["message"]

    @pytest.mark.asyncio
    async def test_run_all_checks_includes_database(self):
        """Test that run_all_checks includes database check"""
        from modules.shared.health import HealthChecker

        checker = HealthChecker()
        results = await checker.run_all_checks()

        assert "status" in results
        assert "checks" in results
        assert "database" in results["checks"]
        assert "timestamp" in results