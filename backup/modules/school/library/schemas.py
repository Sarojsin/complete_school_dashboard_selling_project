# School Library Schemas
# ==================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    """Base schema for books"""
    isbn: str = Field(..., max_length=20)
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=100)
    publisher: Optional[str] = Field(None, max_length=100)
    category: str = Field(..., max_length=50)
    total_copies: int = Field(default=1, ge=1)
    available_copies: int = Field(default=1, ge=0)
    shelf_location: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = None


class BookCreate(BookBase):
    """Schema for creating a book"""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book"""
    isbn: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=200)
    author: Optional[str] = Field(None, max_length=100)
    publisher: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)
    shelf_location: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = None


class Book(BookBase):
    """Schema for book response"""
    id: int
    
    class Config:
        from_attributes = True


class BookLoanBase(BaseModel):
    """Base schema for book loans"""
    book_id: int
    student_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str = "issued"
    remarks: Optional[str] = None


class BookLoanCreate(BookLoanBase):
    """Schema for creating a book loan"""
    pass


class BookLoanUpdate(BaseModel):
    """Schema for updating a book loan"""
    return_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class BookLoan(BookLoanBase):
    """Schema for book loan response"""
    id: int
    
    class Config:
        from_attributes = True


class BookReservationBase(BaseModel):
    """Base schema for book reservations"""
    book_id: int
    student_id: int
    reservation_date: date
    status: str = "pending"


class BookReservationCreate(BookReservationBase):
    """Schema for creating a reservation"""
    pass


class BookReservation(BookReservationBase):
    """Schema for reservation response"""
    id: int
    
    class Config:
        from_attributes = True


class LibrarySummary(BaseModel):
    """Schema for library summary"""
    total_books: int = 0
    total_copies: int = 0
    available_copies: int = 0
    books_issued: int = 0
    overdue_books: int = 0
    total_students: int = 0


__all__ = [
    "BookBase",
    "BookCreate",
    "BookUpdate",
    "Book",
    "BookLoanBase",
    "BookLoanCreate",
    "BookLoanUpdate",
    "BookLoan",
    "BookReservationBase",
    "BookReservationCreate",
    "BookReservation",
    "LibrarySummary"
]
