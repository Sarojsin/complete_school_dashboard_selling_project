# School Notices Utils
# =================

from datetime import datetime, date
from typing import List, Optional
from .constants import NOTICE_PRIORITY_URGENT, NOTICE_STATUS_PUBLISHED


def is_notice_active(published_at: Optional[datetime], expires_at: Optional[datetime]) -> bool:
    """Check if notice is currently active"""
    now = datetime.utcnow()
    
    if published_at and now < published_at:
        return False
    
    if expires_at and now > expires_at:
        return False
    
    return True


def calculate_notice_age(created_at: datetime) -> int:
    """Calculate days since notice was created"""
    now = datetime.utcnow()
    delta = now - created_at
    return delta.days


def should_send_notification(priority: str, status: str) -> bool:
    """Determine if notification should be sent"""
    if status != NOTICE_STATUS_PUBLISHED:
        return False
    
    # Always send for urgent, high priority
    if priority in [NOTICE_PRIORITY_URGENT, NOTICE_PRIORITY_URGENT]:
        return True
    
    return True


def format_notice_expiry(expires_at: Optional[date]) -> str:
    """Format expiry date for display"""
    if expires_at is None:
        return "No expiry"
    
    days_left = (expires_at - date.today()).days
    
    if days_left < 0:
        return "Expired"
    elif days_left == 0:
        return "Expires today"
    elif days_left == 1:
        return "Expires tomorrow"
    elif days_left < 7:
        return f"Expires in {days_left} days"
    elif days_left < 30:
        weeks = days_left // 7
        return f"Expires in {weeks} weeks"
    else:
        months = days_left // 30
        return f"Expires in {months} months"


def filter_notices_by_target(notices: List[dict], target: str) -> List[dict]:
    """Filter notices by target audience"""
    if target == "all":
        return notices
    
    return [n for n in notices if target in n.get("targets", [])]


def get_notice_summary(notice: dict) -> str:
    """Get notice summary for display"""
    title = notice.get("title", "")
    priority = notice.get("priority", "low")
    category = notice.get("category", "general")
    
    priority_emoji = {
        "urgent": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }
    
    emoji = priority_emoji.get(priority, "⚪")
    return f"{emoji} [{category.upper()}] {title}"


__all__ = [
    "is_notice_active",
    "calculate_notice_age",
    "should_send_notification",
    "format_notice_expiry",
    "filter_notices_by_target",
    "get_notice_summary"
]