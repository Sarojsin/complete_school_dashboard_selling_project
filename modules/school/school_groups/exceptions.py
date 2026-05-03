# School Groups Exceptions
# ===================

class GroupException(Exception):
    """Base exception for groups module"""
    pass


class GroupNotFoundException(GroupException):
    """Group not found exception"""
    def __init__(self, group_id: int):
        self.group_id = group_id
        super().__init__(f"Group with ID {group_id} not found")


class DuplicateGroupException(GroupException):
    """Duplicate group exception"""
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Group '{name}' already exists")


class GroupFullException(GroupException):
    """Group is at capacity"""
    def __init__(self, group_id: int, capacity: int):
        self.group_id = group_id
        self.capacity = capacity
        super().__init__(f"Group {group_id} has reached capacity of {capacity}")


class MemberNotFoundException(GroupException):
    """Member not found exception"""
    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id
        super().__init__(f"User {user_id} is not a member of group {group_id}")


class DuplicateMemberException(GroupException):
    """Duplicate member exception"""
    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id
        super().__init__(f"User {user_id} is already a member of group {group_id}")


class PostNotFoundException(GroupException):
    """Post not found exception"""
    def __init__(self, post_id: int):
        self.post_id = post_id
        super().__init__(f"Post with ID {post_id} not found")


__all__ = [
    "GroupException",
    "GroupNotFoundException",
    "DuplicateGroupException",
    "GroupFullException",
    "MemberNotFoundException",
    "DuplicateMemberException",
    "PostNotFoundException"
]