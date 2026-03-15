import psutil
import time
import os
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.admin_system_repository import AdminSystemRepository
from app.repositories.admin_settings_repository import AdminSettingsRepository
from app.services.admin_backup_service import AdminBackupService
from app.core.metrics import metrics_collector

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
        snapshot = metrics_collector.snapshot()
        return {
            **snapshot,
            "cache_hit_rate": None,
        }

    @staticmethod
    async def get_backup_status(db: AsyncSession) -> Dict[str, Any]:
        return await AdminBackupService.get_backup_status(db)

    @staticmethod
    async def get_security_status(db: AsyncSession) -> Dict[str, Any]:
        base = await AdminSettingsRepository.get_setting_value(
            db,
            "security_settings",
            {
                "jwt_expiration_minutes": 60,
                "refresh_token_expiration_days": 7,
                "csrf_enabled": True,
                "ip_whitelist_enabled": False,
                "failed_login_attempts_allowed": 5,
                "account_lockout_minutes": 30,
                "two_factor_enabled": False,
            },
        )
        password_policy = await AdminSettingsRepository.get_setting_value(
            db,
            "password_policy",
            {
                "min_length": 8,
                "require_uppercase": True,
                "require_numbers": True,
                "require_special_chars": True,
            },
        )
        base["password_policy"] = password_policy
        return base

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
