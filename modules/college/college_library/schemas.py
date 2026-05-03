"""
College Library Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    total_copies: int = 1


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    available_copies: int

    class Config:
        from_attributes = True


class LoanBase(BaseModel):
    book_id: int
    user_id: int


class LoanCreate(LoanBase):
    due_days: int = 14


class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    return_date: Optional[date] = None

    class Config:
        from_attributes = True


__all__ = ["BookBase", "BookCreate", "BookResponse", "LoanBase", "LoanCreate", "LoanResponse"]
