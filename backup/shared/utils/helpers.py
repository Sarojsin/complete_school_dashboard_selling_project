"""
Common Utility Functions

Helper functions used across the application.
"""

from typing import Any, Dict, Optional
from datetime import datetime, date


def format_date(dt: Optional[datetime | date]) -> str:
    """Format a date or datetime to string"""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d")


def parse_date(date_str: str) -> Optional[date]:
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing special characters"""
    import re
    # Remove special characters except . - _
    return re.sub(r'[^\w\-.]', '_', filename)


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    import re
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def paginate_results(items: list, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_initials(name: str) -> str:
    """Get initials from a name"""
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()
