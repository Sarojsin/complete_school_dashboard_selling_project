class GroupManagementError(Exception):
    """Base exception for group management errors"""
    pass

class PermissionDeniedError(GroupManagementError):
    """User doesn't have permission to perform action"""
    pass

class NotFoundError(GroupManagementError):
    """Requested resource not found"""
    pass

class ValidationError(GroupManagementError):
    """Validation error for group operations"""
    pass

class DuplicateMemberError(GroupManagementError):
    """User is already a member of the group"""
    pass