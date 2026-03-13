"""
Admin Backup & Restore System API

API endpoints for database backup, restore, and backup management.
"""

from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import csv
import io
import json
from pathlib import Path

from app.core.database import get_async_db
from app.models.models import User, Student, Teacher, FeeRecord, Grade, Course
from app.models.exam_models import ExamResult
from app.api.deps.admin import get_current_admin
from app.services.admin_backup_service import AdminBackupService
from app.repositories.admin_backup_repository import AdminBackupRepository


# Create router
router = APIRouter(prefix="/admin/backup", tags=["Admin Backup"])


# ============ BACKUP MODELS ============

class BackupResponse(BaseModel):
    id: int
    filename: str
    size_mb: float
    created_at: str
    backup_type: str  # manual, auto
    status: str  # completed, failed, in_progress


def _serialize_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            return value
    if hasattr(value, "value"):
        return value.value
    return value


def _serialize_rows(rows, fields):
    items = []
    for row in rows:
        item = {}
        for f in fields:
            item[f] = _serialize_value(getattr(row, f, None))
        items.append(item)
    return items


# ============ MANUAL BACKUP ============

@router.post("/create")
async def create_backup(
    backup_type: str = "manual",  # manual, auto
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new database backup"""
    backup = await AdminBackupService.create_backup(
        db=db,
        backup_type=backup_type,
        created_by=current_user.id,
    )
    return {"success": True, "message": "Backup created successfully", "backup": backup}


# ============ BACKUP LIST ============

@router.get("/list")
async def list_backups(
    backup_type: Optional[str] = None,  # manual, auto
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """List all backups"""
    records = await AdminBackupRepository.list_backups(
        db, backup_type=backup_type, skip=skip, limit=limit
    )
    backups = [
        {
            "id": r.id,
            "filename": r.filename,
            "size_mb": round(r.size_bytes / (1024 * 1024), 2),
            "created_at": r.created_at.isoformat(),
            "backup_type": r.backup_type,
            "status": r.status,
        }
        for r in records
    ]
    total_size = sum(r.size_bytes for r in records)
    return {"backups": backups, "total": len(backups), "total_size_mb": round(total_size / (1024 * 1024), 2)}


# ============ DOWNLOAD BACKUP ============

@router.get("/{backup_id}/download")
async def download_backup(
    backup_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Download a backup file"""
    record = await AdminBackupRepository.get_by_id(db, backup_id)
    if not record:
        raise HTTPException(status_code=404, detail="Backup not found")
    file_path = Path(record.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Backup file missing on disk")
    return FileResponse(path=str(file_path), filename=record.filename, media_type="application/octet-stream")


# ============ RESTORE BACKUP ============

@router.post("/{backup_id}/restore")
async def restore_backup(
    backup_id: int,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Restore database from backup"""
    return await AdminBackupService.restore_backup(db, backup_id)


# ============ DELETE BACKUP ============

@router.delete("/{backup_id}")
async def delete_backup(
    backup_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a backup file"""
    return await AdminBackupService.delete_backup(db, backup_id)


# ============ AUTO BACKUP SCHEDULE ============

@router.get("/schedule")
async def get_backup_schedule(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get current backup schedule"""
    schedule = await AdminBackupService.get_backup_schedule(db)
    return schedule


@router.patch("/schedule")
async def update_backup_schedule(
    enabled: Optional[bool] = None,
    frequency: Optional[str] = None,  # daily, weekly, monthly
    time: Optional[str] = None,
    retention_days: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Update backup schedule"""
    schedule = await AdminBackupService.update_backup_schedule(
        db,
        updates={
            "enabled": enabled,
            "frequency": frequency,
            "time": time,
            "retention_days": retention_days,
        },
        updated_by=current_user.id,
    )
    return {"success": True, "message": "Backup schedule updated", "schedule": schedule}


# ============ BACKUP STATUS ============

@router.get("/status")
async def get_backup_status(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get backup system status"""
    return await AdminBackupService.get_backup_status(db)


# ============ EXPORT DATA ============

@router.post("/export")
async def export_data(
    data_type: str,  # users, students, grades, etc.
    format: str = "json",  # json, csv
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Export specific data"""
    export_map = {
        "users": (User, ["id", "email", "username", "full_name", "role", "is_active", "created_at"]),
        "students": (Student, ["id", "user_id", "student_id", "full_name", "grade_level", "section", "enrollment_date"]),
        "teachers": (Teacher, ["id", "user_id", "employee_id", "full_name", "department", "status", "joining_date"]),
        "fees": (FeeRecord, ["id", "student_id", "fee_type", "amount", "paid_amount", "due_date", "payment_date", "status"]),
        "grades": (Grade, ["id", "student_id", "course_id", "grade_type", "score", "max_score", "grade", "date"]),
        "courses": (Course, ["id", "course_code", "course_name", "grade_level", "semester", "teacher_id"]),
        "exam_results": (ExamResult, ["id", "student_id", "course_id", "marks", "max_marks", "grade", "exam_type", "is_published"]),
    }
    if data_type not in export_map:
        raise HTTPException(status_code=400, detail="Unsupported data_type")

    model, fields = export_map[data_type]
    rows = await db.execute(select(model))
    items = _serialize_rows(rows.scalars().all(), fields)

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(fields)
        for item in items:
            writer.writerow([item.get(f, "") for f in fields])
        return {"format": "csv", "data_type": data_type, "content": output.getvalue()}

    return {"format": "json", "data_type": data_type, "records": items}


# ============ IMPORT DATA ============

@router.post("/import")
async def import_data(
    data_type: str,  # users, students, grades, etc.
    file_id: Optional[int] = None,
    file: UploadFile = File(None),
    apply: bool = False,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Import data from file"""
    if not file:
        raise HTTPException(status_code=400, detail="Upload a file to import data")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty file")

    filename = (file.filename or "").lower()
    items = []
    if filename.endswith(".csv"):
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8", errors="ignore")))
        items = list(reader)
    else:
        try:
            payload = json.loads(raw.decode("utf-8"))
            items = payload if isinstance(payload, list) else payload.get("records", [])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")

    import_map = {
        "fees": (FeeRecord, ["student_id", "fee_type", "amount", "paid_amount", "due_date", "payment_date", "status"]),
        "grades": (Grade, ["student_id", "course_id", "grade_type", "score", "max_score", "grade", "date"]),
        "exam_results": (ExamResult, ["student_id", "course_id", "marks", "max_marks", "grade", "exam_type", "is_published"]),
        "courses": (Course, ["course_code", "course_name", "grade_level", "semester", "teacher_id"]),
    }
    if data_type not in import_map:
        raise HTTPException(status_code=400, detail="Unsupported data_type for import")

    model, fields = import_map[data_type]
    if not apply:
        preview = items[:5]
        return {
            "success": True,
            "message": f"Parsed {len(items)} records (preview only). Set apply=true to insert.",
            "preview": preview,
        }

    created = 0
    for item in items:
        payload = {}
        for f in fields:
            if f not in item:
                continue
            value = item[f]
            if value in (None, ""):
                payload[f] = None
                continue
            if f.endswith("_date"):
                try:
                    payload[f] = datetime.fromisoformat(value).date()
                except Exception:
                    payload[f] = None
            elif f in ("amount", "paid_amount", "score", "max_score", "marks"):
                try:
                    payload[f] = float(value)
                except Exception:
                    payload[f] = 0.0
            elif f.endswith("_id"):
                try:
                    payload[f] = int(value)
                except Exception:
                    payload[f] = None
            elif f == "is_published":
                payload[f] = str(value).lower() in ("true", "1", "yes")
            else:
                payload[f] = value
        db.add(model(**payload))
        created += 1
    await db.commit()

    return {"success": True, "message": f"Imported {created} records", "created": created}
