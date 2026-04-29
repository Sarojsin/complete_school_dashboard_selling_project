# School Notices Exceptions
# ======================

class NoticeException(Exception):
    """Base exception for notices module"""
    pass


class NoticeNotFoundException(NoticeException):
    """Notice not found exception"""
    def __init__(self, notice_id: int):
        self.notice_id = notice_id
        super().__init__(f"Notice with ID {notice_id} not found")


class DuplicateNoticeException(NoticeException):
    """Duplicate notice exception"""
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"Notice with title '{title}' already exists")


class InvalidNoticeTargetException(NoticeException):
    """Invalid notice target exception"""
    def __init__(self, target: str):
        self.target = target
        super().__init__(f"Invalid notice target: {target}")


class NoticeAccessDeniedException(NoticeException):
    """Access denied exception"""
    def __init__(self, notice_id: int, user_id: int):
        self.notice_id = notice_id
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot modify notice {notice_id}")


class InvalidNoticePriorityException(NoticeException):
    """Invalid notice priority exception"""
    def __init__(self, priority: str):
        self.priority = priority
        super().__init__(f"Invalid notice priority: {priority}")


class NoticeExpiredException(NoticeException):
    """Notice expired exception"""
    def __init__(self, notice_id: int):
        self.notice_id = notice_id
        super().__init__(f"Notice {notice_id} has expired")


__all__ = [
    "NoticeException",
    "NoticeNotFoundException",
    "DuplicateNoticeException",
    "InvalidNoticeTargetException",
    "NoticeAccessDeniedException",
    "InvalidNoticePriorityException",
    "NoticeExpiredException"
]