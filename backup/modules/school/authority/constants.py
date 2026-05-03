"""
Authority Module Constants
"""

from enum import Enum


class AuthorityRole(str, Enum):
    """Authority roles in school"""
    PRINCIPAL = "PRINCIPAL"
    VICE_PRINCIPAL = "VICE_PRINCIPAL"
    ADMIN = "ADMIN"
    COORDINATOR = "COORDINATOR"


# Permission scopes
SCOPE_ALL = "all"
SCOPE_DEPARTMENT = "department"
SCOPE_CLASS = "class"


# Default positions
DEFAULT_POSITIONS = [
    "Principal",
    "Vice Principal", 
    "Academic Coordinator",
    "Administrative Officer",
    "Finance Officer",
]
