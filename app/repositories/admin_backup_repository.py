from typing import List, Optional

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_models import BackupRecord


class AdminBackupRepository:
    """CRUD operations for backup records."""

    @staticmethod
    async def create(db: AsyncSession, record: BackupRecord) -> BackupRecord:
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def get_by_id(db: AsyncSession, backup_id: int) -> Optional[BackupRecord]:
        result = await db.execute(
            select(BackupRecord).where(BackupRecord.id == backup_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_backups(
        db: AsyncSession,
        backup_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[BackupRecord]:
        query = select(BackupRecord)
        if backup_type:
            query = query.where(BackupRecord.backup_type == backup_type)
        query = query.order_by(desc(BackupRecord.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def delete(db: AsyncSession, record: BackupRecord) -> None:
        await db.delete(record)
        await db.commit()
