"""
Shared Model Mixins and Base Models

Provides reusable mixins for common model functionality and base model definitions.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from enum import Enum as PyEnum

from .base import Base


# Enums
class UserRole(str, PyEnum):
    """User role enumeration"""
    ADMIN = "admin"  # Maps to SUPER_ADMIN in some contexts
    SUPER_ADMIN = "super_admin"
    SCHOOL_ADMIN = "school_admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"
    AUTHORITY = "authority"
    COLLEGE_STUDENT = "college_student"
    COLLEGE_FACULTY = "college_faculty"
    DEAN = "dean"
    REGISTRAR = "registrar"
    HOD = "hod"
    EXAM_SECTION = "exam_section"
    LIBRARY_MANAGER = "library_manager"
    ACCOUNT_SECTION = "account_section"


class PortalType(str, PyEnum):
    """Portal type enumeration"""
    SCHOOL = "school"
    COLLEGE = "college"


# User Model
class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    portal_type = Column(String(20), nullable=True)  # Added in recent migration
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships (will be added as needed)
    # audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class SoftDeleteMixin:
    """
    Soft delete mixin for models that should support soft deletion.

    Adds is_deleted flag and deleted_at timestamp to prevent hard deletes.
    """
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    async def soft_delete(self, db_session):
        """
        Soft delete this record.

        Sets is_deleted=True and deleted_at timestamp.
        """
        from datetime import datetime
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        await db_session.commit()

    async def restore(self, db_session):
        """
        Restore a soft-deleted record.

        Sets is_deleted=False and clears deleted_at.
        """
        self.is_deleted = False
        self.deleted_at = None
        await db_session.commit()

    @property
    def is_active(self) -> bool:
        """Check if record is active (not soft deleted)"""
        return not self.is_deleted


class UUIDMixin:
    """
    UUID primary key mixin.

    Provides UUID-based primary keys for public-facing resources to prevent enumeration.
    Note: Currently planned for future implementation.
    """
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.id)


class TimestampMixin:
    """
    Timestamp mixin for created_at and updated_at fields.

    Automatically manages creation and update timestamps.
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                       onupdate=func.now(), nullable=False)


class BaseMixin(SoftDeleteMixin, TimestampMixin):
    """
    Combined mixin with soft delete and timestamp functionality.

    Use this for models that need both soft delete and timestamp tracking.
    """
    pass


__all__ = [
    "User",
    "UserRole",
    "PortalType",
    "SoftDeleteMixin",
    "UUIDMixin",
    "TimestampMixin",
    "BaseMixin",
]