from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
import asyncio
import calendar
import os
import shutil
import subprocess

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.admin_models import BackupRecord
from app.repositories.admin_backup_repository import AdminBackupRepository
from app.repositories.admin_settings_repository import AdminSettingsRepository
from app.core.exceptions import ValidationError, NotFoundError


class AdminBackupService:
    """Backup/restore logic with SQLite-first support."""

    _backup_lock = asyncio.Lock()

    DEFAULT_SCHEDULE = {
        "enabled": True,
        "frequency": "daily",
        "time": "02:00",
        "retention_days": 30,
        "last_run": None,
        "next_run": None,
        "last_status": None,
        "last_error": None,
        "last_backup_id": None,
    }

    @staticmethod
    def _project_root() -> Path:
        return Path(__file__).resolve().parents[2]

    @staticmethod
    def _backup_dir() -> Path:
        path = AdminBackupService._project_root() / "backups"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def _db_url():
        return make_url(settings.DATABASE_URL_FIXED)

    @staticmethod
    def _db_backend() -> str:
        return AdminBackupService._db_url().get_backend_name()

    @staticmethod
    def _get_sqlite_db_path() -> Optional[Path]:
        url = AdminBackupService._db_url()
        if url.get_backend_name() != "sqlite":
            return None
        if not url.database:
            return None
        db_path = Path(url.database)
        if not db_path.is_absolute():
            db_path = AdminBackupService._project_root() / db_path
        return db_path

    @staticmethod
    def _get_postgres_info() -> Optional[Dict[str, Optional[str]]]:
        url = AdminBackupService._db_url()
        if url.get_backend_name() not in ("postgresql", "postgres"):
            return None
        if not url.database:
            raise ValidationError("PostgreSQL database name is required for backups")
        return {
            "database": url.database,
            "host": url.host,
            "port": url.port,
            "username": url.username,
            "password": url.password,
        }

    @staticmethod
    def _pg_env(info: Dict[str, Optional[str]]) -> Dict[str, str]:
        env = os.environ.copy()
        if info.get("password"):
            env["PGPASSWORD"] = info["password"]
        return env

    @staticmethod
    def _pg_args(info: Dict[str, Optional[str]]) -> list[str]:
        args: list[str] = []
        if info.get("host"):
            args += ["-h", info["host"]]
        if info.get("port"):
            args += ["-p", str(info["port"])]
        if info.get("username"):
            args += ["-U", info["username"]]
        return args

    @staticmethod
    def _run_command(cmd: list[str], env: Optional[Dict[str, str]] = None) -> None:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            raise ValidationError(f"Command failed: {' '.join(cmd[:1])}. {detail}")

    @staticmethod
    def _ensure_pg_tools(require_restore: bool = False) -> None:
        if not shutil.which("pg_dump"):
            raise ValidationError("pg_dump is not available on this server")
        if require_restore and not shutil.which("pg_restore"):
            raise ValidationError("pg_restore is not available on this server")

    @staticmethod
    def _parse_schedule_time(time_value: Optional[str]) -> tuple[int, int]:
        if not time_value:
            raise ValidationError("Backup schedule time is required")
        parts = time_value.split(":")
        if len(parts) != 2:
            raise ValidationError("Backup time must be in HH:MM format")
        try:
            hour = int(parts[0])
            minute = int(parts[1])
        except ValueError as exc:
            raise ValidationError("Backup time must be numeric HH:MM") from exc
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValidationError("Backup time must be a valid 24-hour time")
        return hour, minute

    @staticmethod
    def _add_months(value: datetime, months: int) -> datetime:
        total_month = value.month - 1 + months
        year = value.year + total_month // 12
        month = total_month % 12 + 1
        day = min(value.day, calendar.monthrange(year, month)[1])
        return value.replace(year=year, month=month, day=day)

    @staticmethod
    def _calculate_next_run(now: datetime, schedule: Dict[str, Any]) -> datetime:
        hour, minute = AdminBackupService._parse_schedule_time(schedule.get("time"))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        frequency = (schedule.get("frequency") or "daily").lower()
        if frequency == "daily":
            if candidate <= now:
                candidate += timedelta(days=1)
            return candidate
        if frequency == "weekly":
            if candidate <= now:
                candidate += timedelta(days=7)
            return candidate
        if frequency == "monthly":
            if candidate <= now:
                candidate = AdminBackupService._add_months(candidate, 1)
            return candidate
        raise ValidationError("Backup frequency must be daily, weekly, or monthly")

    @staticmethod
    async def create_backup(
        db: AsyncSession,
        backup_type: str,
        created_by: Optional[int],
    ) -> Dict[str, Any]:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        status = "completed"
        error_detail = None
        filename = ""
        dest = None

        backend = AdminBackupService._db_backend()
        try:
            if backend == "sqlite":
                db_path = AdminBackupService._get_sqlite_db_path()
                if not db_path or not db_path.exists():
                    raise ValidationError("SQLite database file was not found for backup")
                filename = f"backup_{timestamp}.sqlite"
                dest = AdminBackupService._backup_dir() / filename
                await asyncio.to_thread(shutil.copy2, db_path, dest)
            elif backend in ("postgresql", "postgres"):
                info = AdminBackupService._get_postgres_info()
                if not info:
                    raise ValidationError("PostgreSQL configuration is missing")
                AdminBackupService._ensure_pg_tools()
                filename = f"backup_{timestamp}.dump"
                dest = AdminBackupService._backup_dir() / filename
                cmd = [
                    "pg_dump",
                    "--format=custom",
                    "--no-owner",
                    "--no-privileges",
                    "--file",
                    str(dest),
                ]
                cmd += AdminBackupService._pg_args(info)
                cmd.append(info["database"])
                await asyncio.to_thread(
                    AdminBackupService._run_command,
                    cmd,
                    AdminBackupService._pg_env(info),
                )
            else:
                raise ValidationError("Database backend not supported for backups")
        except Exception as exc:
            status = "failed"
            error_detail = str(exc)

        size_bytes = dest.stat().st_size if dest and dest.exists() else 0
        record = BackupRecord(
            filename=filename or f"backup_{timestamp}.unknown",
            file_path=str(dest) if dest else "",
            size_bytes=size_bytes,
            backup_type=backup_type,
            status=status,
            created_by=created_by,
        )
        record = await AdminBackupRepository.create(db, record)

        if status != "completed":
            raise ValidationError(f"Backup failed: {error_detail or 'unknown error'}")

        return {
            "id": record.id,
            "filename": record.filename,
            "size_mb": round(record.size_bytes / (1024 * 1024), 2),
            "created_at": record.created_at.isoformat(),
            "backup_type": record.backup_type,
            "status": record.status,
        }

    @staticmethod
    async def restore_backup(db: AsyncSession, backup_id: int) -> Dict[str, Any]:
        record = await AdminBackupRepository.get_by_id(db, backup_id)
        if not record:
            raise NotFoundError("Backup not found")

        backup_path = Path(record.file_path)
        if not backup_path.exists():
            raise ValidationError("Backup file missing on disk")

        backend = AdminBackupService._db_backend()
        if backend == "sqlite":
            db_path = AdminBackupService._get_sqlite_db_path()
            if not db_path:
                raise ValidationError("SQLite database path not found")
            await asyncio.to_thread(shutil.copy2, backup_path, db_path)
            return {"success": True, "message": "Restore completed. Restart the app to ensure connections refresh."}

        if backend in ("postgresql", "postgres"):
            info = AdminBackupService._get_postgres_info()
            if not info:
                raise ValidationError("PostgreSQL configuration is missing")
            AdminBackupService._ensure_pg_tools(require_restore=True)
            cmd = [
                "pg_restore",
                "--clean",
                "--if-exists",
                "--no-owner",
                "--no-privileges",
                "--dbname",
                info["database"],
            ]
            cmd += AdminBackupService._pg_args(info)
            cmd.append(str(backup_path))
            await asyncio.to_thread(
                AdminBackupService._run_command,
                cmd,
                AdminBackupService._pg_env(info),
            )
            return {"success": True, "message": "Restore completed successfully"}

        raise ValidationError("Database backend not supported for restore")

    @staticmethod
    async def delete_backup(db: AsyncSession, backup_id: int) -> Dict[str, Any]:
        record = await AdminBackupRepository.get_by_id(db, backup_id)
        if not record:
            raise NotFoundError("Backup not found")

        backup_path = Path(record.file_path)
        if backup_path.exists():
            backup_path.unlink()
        await AdminBackupRepository.delete(db, record)
        return {"success": True, "message": f"Backup {backup_id} deleted"}

    @staticmethod
    async def get_backup_status(db: AsyncSession) -> Dict[str, Any]:
        backups = await AdminBackupRepository.list_backups(db, skip=0, limit=1000)
        total_size = sum(b.size_bytes for b in backups)
        latest = backups[0] if backups else None
        oldest = backups[-1] if backups else None
        schedule = await AdminBackupService.get_backup_schedule(db)
        return {
            "total_backups": len(backups),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_backup": oldest.created_at.isoformat() if oldest else None,
            "latest_backup": latest.created_at.isoformat() if latest else None,
            "auto_backup_enabled": bool(schedule.get("enabled", True)),
            "next_scheduled_backup": schedule.get("next_run"),
            "last_backup_status": schedule.get("last_status"),
            "last_backup_error": schedule.get("last_error"),
            "storage_used_percent": None,
        }

    @staticmethod
    async def get_backup_schedule(db: AsyncSession) -> Dict[str, Any]:
        raw = await AdminSettingsRepository.get_setting_value(
            db, "backup_schedule", AdminBackupService.DEFAULT_SCHEDULE
        )
        if not isinstance(raw, dict):
            return dict(AdminBackupService.DEFAULT_SCHEDULE)
        merged = {**AdminBackupService.DEFAULT_SCHEDULE, **raw}
        return merged

    @staticmethod
    async def update_backup_schedule(
        db: AsyncSession,
        updates: Dict[str, Any],
        updated_by: Optional[int],
    ) -> Dict[str, Any]:
        current = await AdminBackupService.get_backup_schedule(db)
        current.update({k: v for k, v in updates.items() if v is not None})
        if current.get("enabled", True):
            now = datetime.utcnow()
            current["next_run"] = AdminBackupService._calculate_next_run(now, current).isoformat()
        else:
            current["next_run"] = None
        await AdminSettingsRepository.upsert_setting(
            db, "backup_schedule", current, updated_by=updated_by
        )
        return current

    @staticmethod
    async def _apply_retention(db: AsyncSession, retention_days: Optional[int]) -> None:
        if not retention_days or retention_days <= 0:
            return
        cutoff = datetime.utcnow() - timedelta(days=retention_days)
        backups = await AdminBackupRepository.list_backups(db, skip=0, limit=1000)
        for record in backups:
            if record.created_at and record.created_at < cutoff:
                try:
                    backup_path = Path(record.file_path)
                    if backup_path.exists():
                        backup_path.unlink()
                finally:
                    await AdminBackupRepository.delete(db, record)

    @staticmethod
    async def run_scheduled_backup(db: AsyncSession) -> Optional[Dict[str, Any]]:
        async with AdminBackupService._backup_lock:
            schedule = await AdminBackupService.get_backup_schedule(db)
            if not schedule.get("enabled", True):
                return None

            now = datetime.utcnow()
            next_run = schedule.get("next_run")
            next_run_dt = None
            if next_run:
                try:
                    next_run_dt = datetime.fromisoformat(str(next_run))
                except Exception:
                    next_run_dt = None

            if next_run_dt and now < next_run_dt:
                return None

            try:
                backup = await AdminBackupService.create_backup(
                    db=db,
                    backup_type="auto",
                    created_by=None,
                )
                schedule["last_status"] = "success"
                schedule["last_backup_id"] = backup.get("id")
            except Exception as exc:
                schedule["last_status"] = "failed"
                schedule["last_error"] = str(exc)
                backup = None
            finally:
                schedule["last_run"] = now.isoformat()
                schedule["next_run"] = AdminBackupService._calculate_next_run(now, schedule).isoformat()
                await AdminSettingsRepository.upsert_setting(db, "backup_schedule", schedule, updated_by=None)

            await AdminBackupService._apply_retention(db, schedule.get("retention_days"))
            return backup

    @staticmethod
    async def run_scheduled_backup_job() -> None:
        async with AsyncSessionLocal() as db:
            try:
                await AdminBackupService.run_scheduled_backup(db)
            except Exception:
                await db.rollback()
