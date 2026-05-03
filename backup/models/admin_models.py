"""
Admin Feature Control Models

This module contains models for the admin panel feature control system.
- SystemFeature: Enable/disable features globally
- FeatureRolePermission: Control which roles can access features
- AdminAuditLog: Track admin actions
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backup.core.database import Base
from backup.models.models import UserRole


class FeatureCategory(str, enum.Enum):
    """Categories for organizing features"""
    AUTHENTICATION = "authentication"
    ACADEMIC = "academic"
    STUDENT_MANAGEMENT = "student_management"
    TEACHER_MANAGEMENT = "teacher_management"
    FINANCE = "finance"
    COMMUNICATION = "communication"
    LIBRARY = "library"
    REPORTS = "reports"
    SYSTEM = "system"


class SystemFeature(Base):
    """
    Represents a feature in the system that can be enabled or disabled.
    
    Attributes:
        id: Primary key
        feature_code: Unique identifier (e.g., "STUDENT_ENROLLMENT")
        feature_name: Display name
        feature_category: Category for grouping
        description: What the feature does
        is_enabled: Global on/off switch
        is_global: If True, applies to all roles regardless of role permissions
    """
    __tablename__ = "system_features"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_code = Column(String(100), unique=True, nullable=False, index=True)
    feature_name = Column(String(255), nullable=False)
    feature_category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True, nullable=False)
    is_global = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    role_permissions = relationship(
        "FeatureRolePermission", 
        back_populates="feature", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self):
        return f"<SystemFeature {self.feature_code}: {'enabled' if self.is_enabled else 'disabled'}>"


class FeatureRolePermission(Base):
    """
    Defines what actions a specific role can perform on a feature.
    
    Attributes:
        id: Primary key
        feature_id: Foreign key to SystemFeature
        role: The UserRole this permission applies to
        can_create: Can create/insert
        can_read: Can view/read
        can_update: Can modify/update
        can_delete: Can remove/delete
    """
    __tablename__ = "feature_role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("system_features.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    can_create = Column(Boolean, default=True, nullable=False)
    can_read = Column(Boolean, default=True, nullable=False)
    can_update = Column(Boolean, default=True, nullable=False)
    can_delete = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    feature = relationship("SystemFeature", back_populates="role_permissions")
    
    def __repr__(self):
        return f"<FeatureRolePermission {self.feature.feature_code if self.feature else 'N/A'} for {self.role.value}>"
    
    def has_permission(self, action: str) -> bool:
        """Check if this permission allows the given action"""
        action_map = {
            "create": self.can_create,
            "read": self.can_read,
            "update": self.can_update,
            "delete": self.can_delete,
        }
        return action_map.get(action, False)


class AdminAuditLog(Base):
    """
    Tracks all administrative actions for audit purposes.
    
    Attributes:
        id: Primary key
        admin_user_id: Who performed the action
        action: What was done (enable_feature, disable_feature, etc.)
        feature_code: Which feature was affected
        old_value: Previous value (as JSON string)
        new_value: New value (as JSON string)
        ip_address: IP address of the admin
        timestamp: When the action occurred
    """
    __tablename__ = "admin_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    feature_code = Column(String(100), nullable=True, index=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<AdminAuditLog {self.action} on {self.feature_code} at {self.timestamp}>"


class LoginHistory(Base):
    """
    Tracks successful and failed authentication attempts.

    This powers admin login-history visibility and security analytics.
    """
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    username = Column(String(100), nullable=True, index=True)
    success = Column(Boolean, default=False, nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    failure_reason = Column(String(255), nullable=True)
    token_issued_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User")

    def __repr__(self):
        status = "success" if self.success else "failed"
        return f"<LoginHistory {status} user={self.user_id} at {self.created_at}>"


class FailedLoginAttempt(Base):
    """
    Tracks repeated failed login attempts by username and IP.
    """
    __tablename__ = "failed_login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(50), nullable=True, index=True)
    attempts_count = Column(Integer, default=1, nullable=False)
    last_failure_reason = Column(String(255), nullable=True)
    last_attempt_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<FailedLoginAttempt username={self.username} count={self.attempts_count}>"


class UserSecurityState(Base):
    """
    Stores mutable security controls for users without changing core user schema.
    """
    __tablename__ = "user_security_states"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True)
    is_locked = Column(Boolean, default=False, nullable=False, index=True)
    lock_reason = Column(Text, nullable=True)
    locked_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    locked_at = Column(DateTime, nullable=True)
    force_logout_after = Column(DateTime, nullable=True, index=True)
    force_logout_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<UserSecurityState user={self.user_id} locked={self.is_locked}>"


class SystemSetting(Base):
    """
    Stores mutable system configuration as JSON blobs.

    Example keys:
    - security_settings
    - jwt_settings
    - password_policy
    - ip_whitelist
    - backup_schedule
    - notification_automations
    - broadcast_history
    """
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value_json = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<SystemSetting {self.key}>"


class BackupRecord(Base):
    """
    Tracks backups created by the admin backup system.
    """
    __tablename__ = "backup_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    size_bytes = Column(Integer, default=0, nullable=False)
    backup_type = Column(String(20), default="manual", nullable=False)  # manual, auto
    status = Column(String(20), default="completed", nullable=False)    # completed, failed, in_progress
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<BackupRecord {self.filename} {self.status}>"


# Import UserRole for type hints in other modules
__all__ = [
    "SystemFeature",
    "FeatureRolePermission", 
    "AdminAuditLog",
    "LoginHistory",
    "FailedLoginAttempt",
    "UserSecurityState",
    "SystemSetting",
    "BackupRecord",
    "FeatureCategory",
]
