import json
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_models import SystemSetting


class AdminSettingsRepository:
    """Persistence for admin and system settings stored as JSON blobs."""

    @staticmethod
    async def get_setting(db: AsyncSession, key: str) -> Optional[SystemSetting]:
        try:
            result = await db.execute(
                select(SystemSetting).where(SystemSetting.key == key)
            )
            return result.scalar_one_or_none()
        except ProgrammingError as exc:
            # Missing table in non-migrated databases.
            if "does not exist" in str(exc).lower():
                try:
                    await db.rollback()
                except Exception:
                    pass
                return None
            raise

    @staticmethod
    async def get_setting_value(db: AsyncSession, key: str, default: Any) -> Any:
        setting = await AdminSettingsRepository.get_setting(db, key)
        if not setting:
            return default
        try:
            return json.loads(setting.value_json)
        except Exception:
            return default

    @staticmethod
    async def upsert_setting(
        db: AsyncSession,
        key: str,
        value: Any,
        updated_by: Optional[int] = None,
    ) -> SystemSetting:
        payload = json.dumps(value)
        try:
            setting = await AdminSettingsRepository.get_setting(db, key)
            if setting is None:
                setting = SystemSetting(
                    key=key,
                    value_json=payload,
                    updated_by=updated_by,
                )
            else:
                setting.value_json = payload
                setting.updated_by = updated_by
                setting.updated_at = datetime.utcnow()
            db.add(setting)
            await db.commit()
            await db.refresh(setting)
            return setting
        except ProgrammingError as exc:
            if "does not exist" not in str(exc).lower():
                raise
            try:
                await db.rollback()
            except Exception:
                pass
            # Attempt to bootstrap missing admin tables and retry once.
            try:
                from app.core.database import ensure_admin_tables

                ensure_admin_tables()
                setting = SystemSetting(
                    key=key,
                    value_json=payload,
                    updated_by=updated_by,
                )
                db.add(setting)
                await db.commit()
                await db.refresh(setting)
                return setting
            except Exception:
                raise
