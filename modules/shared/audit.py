"""
Audit Logging Module

Provides comprehensive audit logging for all database operations.
Tracks user actions, resource changes, and system events.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.shared.database import Base

class AuditLog(Base):
    """
    Audit log model for tracking all state-changing operations.

    Captures CREATE, UPDATE, DELETE operations with full context.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for system operations
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
    resource_type = Column(String(100), nullable=False)  # e.g., "college_faculty", "school_student"
    resource_id = Column(String(100), nullable=False)  # String to handle UUIDs and composite keys
    details = Column(JSON, nullable=True)  # Old values, new values, metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    session_id = Column(String(255), nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationship to user (optional)
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', resource='{self.resource_type}:{self.resource_id}', user_id={self.user_id})>"


# Add back reference to User model
# This will be added when the User model is imported
def _add_audit_relationship():
    """Add audit_logs relationship to User model"""
    try:
        from modules.shared.models import User
        if not hasattr(User, 'audit_logs'):
            User.audit_logs = relationship("AuditLog", back_populates="user")
    except ImportError:
        # User model not available yet
        pass


# Initialize relationships when module is imported
_add_audit_relationship()