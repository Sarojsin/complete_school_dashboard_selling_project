from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BookLoanCreate(BaseModel):
    student_id: int
    book_title: str
    book_author: str
    book_isbn: Optional[str] = None
    due_days: int = 15  # Default 15 days loan period

class BookLoanReturn(BaseModel):
    loan_id: int

class BookLoanResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    book_title: str
    book_author: str
    taken_date: date
    due_date: date
    return_date: Optional[date]
    status: str
    fine_amount: int
    
    class Config:
        orm_mode = True

class LibraryStats(BaseModel):
    total_borrowed: int
    total_overdue: int
    total_fines: int