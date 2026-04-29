"""
Super Admin Models - System-wide models

Contains SystemSetting, Feature, AuditLog, SystemBackup, and extended admin models.
"""

from modules.shared.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func


class SystemSetting(Base):
    """System settings key-value store"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class SystemFeature(Base):
    """System feature with code, name, and category for granular management"""
    __tablename__ = "system_features"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_code = Column(String(100), unique=True, nullable=False, index=True)
    feature_name = Column(String(200), nullable=False)
    feature_category = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    is_enabled = Column(Boolean, default=True, index=True)
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class FeatureRolePermission(Base):
    """Role-based permissions for features"""
    __tablename__ = "feature_role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, nullable=False, index=True)
    role = Column(String(50), nullable=False, index=True)
    can_create = Column(Boolean, default=False)
    can_read = Column(Boolean, default=True)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)


class Feature(Base):
    """Simple feature toggle system (legacy)"""
    __tablename__ = "features"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    is_enabled = Column(Boolean, default=True)
    description = Column(Text)


class AuditLog(Base):
    """Audit log for tracking user actions"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # No FK to keep it independent
    action = Column(String(200), nullable=False)
    details = Column(JSON)
    ip_address = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class SystemBackup(Base):
    """System backup records"""
    __tablename__ = "system_backups"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(300))
    size_bytes = Column(Integer)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, server_default=func.now())