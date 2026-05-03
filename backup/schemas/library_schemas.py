from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    category: Optional[str] = None
    total_copies: int = 1

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    category: Optional[str]
    total_copies: int
    available_copies: int
    
    class Config:
        from_attributes = True

class BookLoanCreate(BaseModel):
    student_id: int
    book_title: str
    book_author: str
    book_isbn: Optional[str] = None
    book_id: Optional[int] = None
    due_days: int = 15

class BookLoanReturn(BaseModel):
    loan_id: int

class BookLoanResponse(BaseModel):
    id: int
    student_id: int
    book_title: str
    book_author: str
    taken_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str
    fine_amount: int = 0
    student_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class LibraryDashboardStats(BaseModel):
    total_borrowed: int = 0
    total_overdue: int = 0
    total_fines: int = 0
    total_books: int = 0
    books_returned_today: int = 0
    books_issued_today: int = 0

class LibraryStats(BaseModel):
    total_borrowed: int
    total_overdue: int
    total_fines: int