"""
Feature Check Middleware

Dependency functions to check if features are enabled and users have permission.
"""

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_async_db
from app.models.models import User
from app.services.feature_service import FeatureService


async def get_current_user_from_request(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """Get current user from request"""
    from app.dependencies.auth import get_current_user
    
    try:
        # Try to get user from the request state (set by auth middleware)
        if hasattr(request.state, "user"):
            return request.state.user
        
        # Otherwise try to get from token
        return await get_current_user(request, db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )


def require_feature(feature_code: str, action: str = "read"):
    """
    Dependency factory to check if a feature is enabled and user has permission.
    
    Usage:
        @router.get("/students", dependencies=[Depends(require_feature("STUDENT_ENROLLMENT", "create"))])
        async def get_students(...):
            ...
    
    Args:
        feature_code: The feature code to check
        action: The action to check (create, read, update, delete)
    
    Returns:
        A dependency function that enforces feature access
    """
    async def check_feature(
        request: Request,
        db: AsyncSession = Depends(get_async_db)
    ) -> User:
        # Get current user
        try:
            current_user = await get_current_user_from_request(request, db)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Check feature access
        await FeatureService.enforce_feature_access(
            db, feature_code, current_user, action
        )
        
        return current_user
    
    return check_feature


def require_feature_optional(feature_code: str, action: str = "read"):
    """
    Optional feature check - returns None if feature is disabled or user doesn't have permission.
    
    Usage:
        @router.get("/students")
        async def get_students(
            user: Optional[User] = Depends(require_feature_optional("STUDENT_ENROLLMENT", "read"))
        ):
            if user is None:
                # Feature is disabled or user doesn't have access
                return {"message": "Feature not available"}
            ...
    
    Args:
        feature_code: The feature code to check
        action: The action to check
    
    Returns:
        A dependency that returns User or None
    """
    async def check_feature_optional(
        request: Request,
        db: AsyncSession = Depends(get_async_db)
    ) -> Optional[User]:
        try:
            current_user = await get_current_user_from_request(request, db)
        except Exception:
            return None
        
        # Check feature access - don't raise exception, just return None
        try:
            await FeatureService.enforce_feature_access(
                db, feature_code, current_user, action
            )
            return current_user
        except HTTPException:
            return None
    
    return check_feature_optional


async def is_feature_enabled(
    feature_code: str,
    db: AsyncSession = Depends(get_async_db)
) -> bool:
    """
    Check if a feature is globally enabled.
    
    Usage:
        @router.get("/students")
        async def get_students(db: AsyncSession = Depends(get_async_db)):
            if not await is_feature_enabled("STUDENT_ENROLLMENT", db):
                return {"message": "Feature disabled"}
            ...
    
    Args:
        feature_code: The feature code to check
        db: Database session
    
    Returns:
        True if feature is enabled, False otherwise
    """
    return await FeatureService.check_feature_enabled(db, feature_code)


class FeatureChecker:
    """
    Class-based feature checker for more complex scenarios.
    
    Usage:
        checker = FeatureChecker("STUDENT_ENROLLMENT")
        
        @router.get("/students")
        async def get_students(
            user: User = Depends(checker.require("create"))
        ):
            ...
    """
    
    def __init__(self, feature_code: str):
        self.feature_code = feature_code
    
    def require(self, action: str = "read"):
        """Require feature access"""
        return require_feature(self.feature_code, action)
    
    def optional(self, action: str = "read"):
        """Optional feature access"""
        return require_feature_optional(self.feature_code, action)
    
    async def is_enabled(self, db: AsyncSession) -> bool:
        """Check if feature is enabled"""
        return await FeatureService.check_feature_enabled(db, self.feature_code)
    
    async def can_access(
        self, 
        db: AsyncSession, 
        user: User, 
        action: str = "read"
    ) -> bool:
        """Check if user can access feature"""
        return await FeatureService.can_access_feature(
            db, self.feature_code, user, action
        )


# Pre-configured feature checkers for common features
class Features:
    """Pre-configured feature checkers"""
    
    # Authentication features
    STUDENT_SIGNUP = FeatureChecker("AUTH_STUDENT_SIGNUP")
    TEACHER_SIGNUP = FeatureChecker("AUTH_TEACHER_SIGNUP")
    PARENT_SIGNUP = FeatureChecker("AUTH_PARENT_SIGNUP")
    PASSWORD_RESET = FeatureChecker("AUTH_PASSWORD_RESET")
    
    # Academic features
    COURSES = FeatureChecker("ACADEMIC_COURSES")
    ASSIGNMENTS = FeatureChecker("ACADEMIC_ASSIGNMENTS")
    ATTENDANCE = FeatureChecker("ACADEMIC_ATTENDANCE")
    GRADES = FeatureChecker("ACADEMIC_GRADES")
    EXAMS = FeatureChecker("ACADEMIC_EXAMS")
    TESTS = FeatureChecker("ACADEMIC_TESTS")
    VIDEOS = FeatureChecker("ACADEMIC_VIDEOS")
    NOTES = FeatureChecker("ACADEMIC_NOTES")
    
    # Student management
    STUDENT_ENROLLMENT = FeatureChecker("STUDENT_ENROLLMENT")
    STUDENT_PROFILE_EDIT = FeatureChecker("STUDENT_PROFILE_EDIT")
    STUDENT_VIEW_OTHER = FeatureChecker("STUDENT_VIEW_OTHER")
    
    # Teacher management
    TEACHER_CREATE = FeatureChecker("TEACHER_CREATE")
    TEACHER_ASSIGN_COURSES = FeatureChecker("TEACHER_ASSIGN_COURSES")
    TEACHER_VIEW_STUDENTS = FeatureChecker("TEACHER_VIEW_STUDENTS")
    
    # Finance
    FEE_STRUCTURE = FeatureChecker("FINANCE_FEE_STRUCTURE")
    FEE_PAYMENT = FeatureChecker("FINANCE_PAYMENT")
    FINANCIAL_REPORTS = FeatureChecker("FINANCE_REPORTS")
    
    # Communication
    NOTICES = FeatureChecker("COMM_NOTICES")
    GROUPS = FeatureChecker("COMM_GROUPS")
    CHAT = FeatureChecker("COMM_CHAT")
    PARENT_PORTAL = FeatureChecker("COMM_PARENT_PORTAL")
    
    # Library
    LIBRARY_BOOKS = FeatureChecker("LIBRARY_BOOKS")
    LIBRARY_ISSUE_RETURN = FeatureChecker("LIBRARY_ISSUE_RETURN")
    
    # Reports
    STUDENT_ANALYTICS = FeatureChecker("REPORTS_STUDENT_ANALYTICS")
    ATTENDANCE_ANALYTICS = FeatureChecker("REPORTS_ATTENDANCE_ANALYTICS")
