# School Account Section Schemas
# ==========================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class SchoolFeeBase(BaseModel):
    """Base schema for school fees"""
    student_id: int
    fee_type: str = Field(..., max_length=100)
    amount: float
    due_date: Optional[date] = None
    paid_amount: Optional[float] = 0
    payment_date: Optional[date] = None
    payment_status: str = "pending"
    remarks: Optional[str] = None


class SchoolFeeCreate(SchoolFeeBase):
    """Schema for creating a fee record"""
    pass


class SchoolFeeUpdate(BaseModel):
    """Schema for updating a fee record"""
    amount: Optional[float] = None
    due_date: Optional[date] = None
    paid_amount: Optional[float] = None
    payment_date: Optional[date] = None
    payment_status: Optional[str] = None
    remarks: Optional[str] = None


class SchoolFee(SchoolFeeBase):
    """Schema for fee response"""
    id: int
    
    class Config:
        from_attributes = True


class SchoolFeePayment(BaseModel):
    """Schema for making a payment"""
    student_id: int
    amount: float
    payment_date: date
    payment_method: str = "cash"
    transaction_id: Optional[str] = None
    remarks: Optional[str] = None


class SchoolExpenseBase(BaseModel):
    """Base schema for school expenses"""
    category: str = Field(..., max_length=100)
    amount: float
    description: Optional[str] = None
    expense_date: date
    vendor: Optional[str] = None
    receipt_number: Optional[str] = None


class SchoolExpenseCreate(SchoolExpenseBase):
    """Schema for creating an expense"""
    pass


class SchoolExpenseUpdate(BaseModel):
    """Schema for updating an expense"""
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    expense_date: Optional[date] = None
    vendor: Optional[str] = None
    receipt_number: Optional[str] = None


class SchoolExpense(SchoolExpenseBase):
    """Schema for expense response"""
    id: int
    
    class Config:
        from_attributes = True


class SchoolFinancialSummary(BaseModel):
    """Schema for financial summary"""
    total_fees_collected: float = 0
    total_fees_pending: float = 0
    total_expenses: float = 0
    net_balance: float = 0
    student_count: int = 0
    paid_students: int = 0
    pending_students: int = 0


__all__ = [
    "SchoolFeeBase",
    "SchoolFeeCreate", 
    "SchoolFeeUpdate",
    "SchoolFee",
    "SchoolFeePayment",
    "SchoolExpenseBase",
    "SchoolExpenseCreate",
    "SchoolExpenseUpdate", 
    "SchoolExpense",
    "SchoolFinancialSummary"
]
