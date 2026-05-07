"""
Audit Logger Utility

Provides functions for logging audit events throughout the application.
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .audit import AuditLog

logger = logging.getLogger(__name__)

class AuditLogger:
    """Handles audit logging operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_action(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """
        Log an audit event.

        Args:
            user_id: ID of the user performing the action (None for system actions)
            action: Action performed (CREATE, UPDATE, DELETE, LOGIN, etc.)
            resource_type: Type of resource affected (e.g., 'college_faculty')
            resource_id: ID of the specific resource
            details: Additional details about the action (old/new values, etc.)
            ip_address: IP address of the client
            user_agent: User agent string from request
            session_id: Session identifier

        Returns:
            The created AuditLog instance
        """
        audit_log = AuditLog(
            user_id=user_id,
            action=action.upper(),
            resource_type=resource_type,
            resource_id=str(resource_id),
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )

        self.db.add(audit_log)
        await self.db.commit()
        await self.db.refresh(audit_log)

        logger.info(f"Audit log: {action} {resource_type}:{resource_id} by user {user_id}")
        return audit_log

    async def log_create(
        self,
        user_id: Optional[int],
        resource_type: str,
        resource_id: str,
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log a resource creation"""
        return await self.log_action(
            user_id=user_id,
            action="CREATE",
            resource_type=resource_type,
            resource_id=resource_id,
            details={"new_values": new_values},
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )

    async def log_update(
        self,
        user_id: Optional[int],
        resource_type: str,
        resource_id: str,
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log a resource update"""
        return await self.log_action(
            user_id=user_id,
            action="UPDATE",
            resource_type=resource_type,
            resource_id=resource_id,
            details={
                "old_values": old_values,
                "new_values": new_values,
                "changed_fields": list(set(old_values.keys()) | set(new_values.keys()))
            },
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )

    async def log_delete(
        self,
        user_id: Optional[int],
        resource_type: str,
        resource_id: str,
        deleted_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log a resource deletion"""
        return await self.log_action(
            user_id=user_id,
            action="DELETE",
            resource_type=resource_type,
            resource_id=resource_id,
            details={"deleted_values": deleted_values},
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )

    async def log_login(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log a user login"""
        return await self.log_action(
            user_id=user_id,
            action="LOGIN",
            resource_type="user",
            resource_id=str(user_id),
            details={"event": "user_login"},
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )

    async def log_logout(
        self,
        user_id: int,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log a user logout"""
        return await self.log_action(
            user_id=user_id,
            action="LOGOUT",
            resource_type="user",
            resource_id=str(user_id),
            details={"event": "user_logout"},
            session_id=session_id
        )

    async def log_failed_login(
        self,
        username: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        reason: str = "invalid_credentials"
    ) -> AuditLog:
        """Log a failed login attempt"""
        return await self.log_action(
            user_id=None,
            action="FAILED_LOGIN",
            resource_type="user",
            resource_id=username,
            details={"reason": reason, "event": "failed_login_attempt"},
            ip_address=ip_address,
            user_agent=user_agent
        )

    async def log_system_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log a system-level event"""
        return await self.log_action(
            user_id=None,
            action="SYSTEM_EVENT",
            resource_type="system",
            resource_id=event_type,
            details=details,
            ip_address=ip_address
        )


# Global function for easy access
async def log_action(
    db: AsyncSession,
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: str,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    session_id: Optional[str] = None
) -> AuditLog:
    """Convenience function for logging audit events"""
    logger = AuditLogger(db)
    return await logger.log_action(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        session_id=session_id
    )