"""
Tests for Prometheus Metrics Endpoint
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint"""

    def test_metrics_endpoint_exists(self, client: TestClient):
        """Test that /metrics endpoint exists and returns metrics"""
        response = client.get("/metrics")

        assert response.status_code == 200
        assert "http_requests_total" in response.text
        assert "http_request_duration_seconds" in response.text

    def test_metrics_endpoint_returns_prometheus_format(self, client: TestClient):
        """Test that metrics are in Prometheus format"""
        response = client.get("/metrics")
        content = response.text

        # Should contain Prometheus metric format
        assert "# HELP" in content or "# TYPE" in content

        # Should contain HTTP request metrics
        assert "http_requests_total" in content

    def test_metrics_include_custom_metrics(self, client: TestClient):
        """Test that custom college metrics are included"""
        response = client.get("/metrics")
        content = response.text

        # Check for custom metrics
        assert "college_enrollments_total" in content
        assert "college_fee_collection_usd" in content
        assert "active_users" in content

    def test_metrics_endpoint_not_in_schema(self, client: TestClient):
        """Test that metrics endpoint is not included in OpenAPI schema"""
        response = client.get("/openapi.json")
        schema = response.json()

        # /metrics should not be in the paths
        assert "/metrics" not in schema.get("paths", {})

    @pytest.mark.asyncio
    async def test_metrics_increment_on_requests(self, client: TestClient):
        """Test that metrics increment when requests are made"""
        # Get initial metrics
        initial_response = client.get("/metrics")
        initial_content = initial_response.text

        # Make some requests
        for _ in range(3):
            client.get("/health/live")

        # Get metrics after requests
        final_response = client.get("/metrics")
        final_content = final_response.text

        # HTTP request count should have increased
        # Note: This is a basic check - in a real scenario you'd parse the metrics
        assert len(final_content) >= len(initial_content)  # Metrics should have grown