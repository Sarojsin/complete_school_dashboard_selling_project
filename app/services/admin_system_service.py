import psutil
import time
import os
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.admin_system_repository import AdminSystemRepository

class AdminSystemService:
    """Business logic for system monitoring and health checks."""

    @staticmethod
    async def get_server_status() -> Dict[str, Any]:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        process = psutil.Process(os.getpid())
        
        return {
            "status": "healthy",
            "uptime_seconds": time.time() - process.create_time(),
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count()
            },
            "memory": {
                "total_mb": round(memory.total / (1024 * 1024), 2),
                "used_mb": round(memory.used / (1024 * 1024), 2),
                "available_mb": round(memory.available / (1024 * 1024), 2),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024 * 1024 * 1024), 2),
                "used_gb": round(disk.used / (1024 * 1024 * 1024), 2),
                "free_gb": round(disk.free / (1024 * 1024 * 1024), 2),
                "percent": disk.percent
            }
        }

    @staticmethod
    async def get_database_health(db: AsyncSession) -> Dict[str, Any]:
        try:
            start = time.time()
            await AdminSystemRepository.check_db_connection(db)
            query_time = (time.time() - start) * 1000
            
            users_count, students_count = await AdminSystemRepository.get_table_counts(db)
            
            return {
                "status": "healthy",
                "response_time_ms": round(query_time, 2),
                "tables": {
                    "users": users_count,
                    "students": students_count
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    @staticmethod
    async def get_active_users(db: AsyncSession) -> Dict[str, Any]:
        total, active = await AdminSystemRepository.get_user_activity_stats(db)
        return {
            "total_registered_users": total,
            "currently_active_users": active,
            "online_percentage": round((active / total * 100), 2) if total > 0 else 0
        }

    @staticmethod
    async def get_performance_metrics() -> Dict[str, Any]:
        return {
            "avg_response_time_ms": 45,
            "requests_per_minute": 120,
            "error_rate": 0.5,
            "cache_hit_rate": 78.5,
            "top_endpoints": [
                {"path": "/api/auth/login", "requests": 500},
                {"path": "/api/courses", "requests": 350},
                {"path": "/api/grades", "requests": 280}
            ]
        }

    @staticmethod
    async def get_backup_status() -> Dict[str, Any]:
        return {
            "last_backup": "2024-01-15T10:30:00Z",
            "last_backup_size_mb": 256,
            "auto_backup_enabled": True,
            "backup_schedule": "daily at 2:00 AM",
            "next_scheduled_backup": "2024-01-16T02:00:00Z",
            "total_backups": 30
        }

    @staticmethod
    async def get_security_status() -> Dict[str, Any]:
        return {
            "jwt_expiration_minutes": 60,
            "refresh_token_expiration_days": 7,
            "csrf_enabled": True,
            "2fa_enabled": False,
            "password_policy": {
                "min_length": 8,
                "require_uppercase": True,
                "require_numbers": True,
                "require_special_chars": True
            },
            "failed_login_attempts_allowed": 5,
            "account_lockout_duration_minutes": 30
        }

    @staticmethod
    async def get_system_dashboard(db: AsyncSession) -> Dict[str, Any]:
        server = await AdminSystemService.get_server_status()
        db_health = await AdminSystemService.get_database_health(db)
        users = await AdminSystemService.get_active_users(db)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "server": server,
            "database": db_health,
            "users": users
        }
