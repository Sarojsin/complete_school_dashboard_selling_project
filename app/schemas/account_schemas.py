from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeacherPaymentCreate(BaseModel):
    teacher_id: int
    amount: float
    month: str  # YYYY-MM
    payment_type: str = "salary"
    notes: Optional[str] = None

class TeacherPaymentResponse(BaseModel):
    id: int
    teacher_id: int
    amount: float
    month: str
    payment_type: str
    paid_at: datetime
    notes: Optional[str] = None
    teacher_name: Optional[str] = None
    paid_by_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class FeePaymentCreate(BaseModel):
    student_id: int
    fee_type: str
    amount: float
    remarks: Optional[str] = None

class AccountDashboardStats(BaseModel):
    fees_collected_month: float = 0
    teacher_payments_month: float = 0
    pending_fees: float = 0
    total_fee_records: int = 0
    total_teacher_payments: int = 0

class AccountStats(BaseModel):
    total_teacher_payments: float
    payments_this_month: float
    pending_payments: int