# College Account Section Schemas
# ==============================

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class AccountSectionStaffBase(BaseModel):
    user_id: int
    full_name: Optional[str] = None
    designation: str = "Account Staff"
    qualification: Optional[str] = None
    phone: Optional[str] = None


class AccountSectionStaffCreate(AccountSectionStaffBase):
    pass


class AccountSectionStaffUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    phone: Optional[str] = None


class AccountSectionStaff(AccountSectionStaffBase):
    id: int
    joining_date: date

    class Config:
        from_attributes = True


class FeeStructureBase(BaseModel):
    program_id: int
    semester: int
    tuition_fee: Decimal = 0
    lab_fee: Decimal = 0
    library_fee: Decimal = 0
    hostel_fee: Decimal = 0
    other_fee: Decimal = 0
    academic_year: str


class FeeStructureCreate(FeeStructureBase):
    pass


class FeeStructureUpdate(BaseModel):
    tuition_fee: Optional[Decimal] = None
    lab_fee: Optional[Decimal] = None
    library_fee: Optional[Decimal] = None
    hostel_fee: Optional[Decimal] = None
    other_fee: Optional[Decimal] = None


class FeeStructure(FeeStructureBase):
    id: int
    total_fee: Decimal

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    student_id: int
    fee_structure_id: int
    amount: Decimal
    payment_date: date
    payment_mode: str  # cash, bank_transfer, online
    transaction_id: Optional[str] = None
    receipt_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    payment_mode: Optional[str] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None


class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    category: str  # salary, infrastructure, supplies, maintenance, etc.
    amount: Decimal
    description: str
    expense_date: date
    vendor: Optional[str] = None
    payment_mode: str = "bank_transfer"
    approved_by: Optional[int] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    vendor: Optional[str] = None


class Expense(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


__all__ = [
    "AccountSectionStaffBase",
    "AccountSectionStaffCreate",
    "AccountSectionStaffUpdate",
    "AccountSectionStaff",
    "FeeStructureBase",
    "FeeStructureCreate",
    "FeeStructureUpdate",
    "FeeStructure",
    "PaymentBase",
    "PaymentCreate",
    "PaymentUpdate",
    "Payment",
    "ExpenseBase",
    "ExpenseCreate",
    "ExpenseUpdate",
    "Expense",
]
