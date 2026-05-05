"""
College Account Section Module

Handles faculty payments, salary disbursement, and financial statistics.
"""

from .router import router as account_section_router
from .service import AccountService
from .repository import AccountRepository
from .models import CollegeFacultyPayment
from .schemas import CollegePaymentCreate, CollegePaymentUpdate, CollegePaymentResponse, AccountStats

__all__ = [
    "router",
    "AccountService",
    "AccountRepository",
    "CollegeFacultyPayment",
    "CollegePaymentCreate",
    "CollegePaymentUpdate",
    "CollegePaymentResponse",
    "AccountStats",
]
