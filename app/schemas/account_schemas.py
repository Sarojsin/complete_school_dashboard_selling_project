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
    teacher_name: str
    amount: float
    month: str
    payment_type: str
    paid_by_name: str
    paid_at: datetime
    notes: Optional[str]
    
    class Config:
        orm_mode = True

class AccountStats(BaseModel):
    total_teacher_payments: float
    payments_this_month: float
    pending_payments: int