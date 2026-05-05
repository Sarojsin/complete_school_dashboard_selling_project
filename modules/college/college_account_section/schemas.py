"""
College Account Section Schemas

Pydantic schemas for faculty payment validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class PaymentType(str, Enum):
    SALARY = "salary"
    BONUS = "bonus"
    ALLOWANCE = "allowance"
    REIMBURSEMENT = "reimbursement"


class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    CHECK = "check"
    OTHER = "other"


# ── Payment Schemas ────────────────────────────────────────────────

class CollegePaymentBase(BaseModel):
    faculty_id: int
    amount: float = Field(..., gt=0)
    month: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")  # YYYY-MM
    payment_type: PaymentType = PaymentType.SALARY
    payment_method: PaymentMethod = PaymentMethod.BANK_TRANSFER
    transaction_reference: Optional[str] = None
    remarks: Optional[str] = None


class CollegePaymentCreate(CollegePaymentBase):
    pass


class CollegePaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    payment_method: Optional[PaymentMethod] = None
    transaction_reference: Optional[str] = None
    remarks: Optional[str] = None


class CollegePaymentResponse(CollegePaymentBase):
    id: int
    paid_by_user_id: int
    paid_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Stats Schema ───────────────────────────────────────────────────

class AccountStats(BaseModel):
    total_payments: int
    total_amount: float
    this_month_total: float
    faculty_count: int


__all__ = [
    "CollegePaymentBase",
    "CollegePaymentCreate",
    "CollegePaymentUpdate",
    "CollegePaymentResponse",
    "AccountStats",
    "PaymentType",
    "PaymentMethod",
]
