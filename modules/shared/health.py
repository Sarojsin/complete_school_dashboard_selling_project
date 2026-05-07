"""
Health Check Module

Provides comprehensive health checks for database connectivity,
external services, and system status.
"""

import os
import time
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .logger import logger


class HealthChecker:
    """Comprehensive health checking for all system components"""

    def __init__(self):
        self.checks = {
            "database": self.check_database,
            "redis": self.check_redis,
        }

    async def check_database(self) -> Dict[str, Any]:
        """
        Check database connectivity and basic functionality.

        Returns:
            Health check result dictionary
        """
        start_time = time.time()

        try:
            # Import database connection here to avoid circular imports
            from .database import get_async_db

            # Test basic connectivity
            async for db in get_async_db():
                # Simple query to test connection
                result = await db.execute(text("SELECT 1 as test"))
                row = result.first()
                if row and row[0] == 1:
                    response_time = time.time() - start_time
                    return {
                        "status": "healthy",
                        "response_time": round(response_time, 3),
                        "message": "Database connection successful"
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "message": "Database query returned unexpected result"
                    }

        except Exception as e:
            response_time = time.time() - start_time
            logger.error("database_health_check_failed", error=str(e), response_time=response_time)

            return {
                "status": "unhealthy",
                "response_time": round(response_time, 3),
                "message": f"Database connection failed: {str(e)}"
            }

    async def check_redis(self) -> Dict[str, Any]:
        """
        Check Redis connectivity if configured.

        Returns:
            Health check result dictionary
        """
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            return {
                "status": "not_configured",
                "message": "Redis not configured"
            }

        start_time = time.time()

        try:
            # Import redis here to avoid dependency if not used
            import redis.asyncio as redis

            # Parse Redis URL
            # redis://username:password@host:port/db
            url_parts = redis_url.replace("redis://", "").split("/")
            host_port = url_parts[0].split("@")[-1]  # Get host:port part
            host, port = host_port.split(":")

            # Create Redis client
            client = redis.Redis(
                host=host,
                port=int(port),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )

            # Test connection
            await client.ping()

            response_time = time.time() - start_time
            return {
                "status": "healthy",
                "response_time": round(response_time, 3),
                "message": "Redis connection successful"
            }

        except ImportError:
            return {
                "status": "not_available",
                "message": "redis library not installed"
            }

        except Exception as e:
            response_time = time.time() - start_time
            logger.error("redis_health_check_failed", error=str(e), response_time=response_time)

            return {
                "status": "unhealthy",
                "response_time": round(response_time, 3),
                "message": f"Redis connection failed: {str(e)}"
            }

    async def run_all_checks(self) -> Dict[str, Any]:
        """
        Run all health checks and return comprehensive status.

        Returns:
            Dictionary with overall status and individual check results
        """
        results = {}
        overall_status = "healthy"

        for check_name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[check_name] = result

                if result["status"] not in ["healthy", "not_configured", "not_available"]:
                    overall_status = "unhealthy"

            except Exception as e:
                logger.error(f"health_check_error", check=check_name, error=str(e))
                results[check_name] = {
                    "status": "error",
                    "message": f"Check failed: {str(e)}"
                }
                overall_status = "unhealthy"

        return {
            "status": overall_status,
            "checks": results,
            "timestamp": time.time()
        }


# Global health checker instance
health_checker = HealthChecker()