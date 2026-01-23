from pydantic import BaseModel
from typing import Optional
from datetime import date

class FeeRecordBase(BaseModel):
    fee_type: str
    amount: float
    due_date: date
    remarks: Optional[str] = None

class FeeRecordCreate(FeeRecordBase):
    student_id: int

class FeeRecordUpdate(BaseModel):
    paid_amount: Optional[float] = None
    payment_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

class FeeRecordResponse(FeeRecordBase):
    id: int
    student_id: int
    paid_amount: float
    payment_date: Optional[date]
    status: str
    
    class Config:
        from_attributes = True
