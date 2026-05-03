"""
College Library Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from .repository import LibraryRepository
from .schemas import BookCreate, LoanCreate


class LibraryService:
    def __init__(self, db: AsyncSession):
        self.repository = LibraryRepository(db)
    
    async def create_book(self, data: BookCreate) -> Dict[str, Any]:
        book = await self.repository.create_book(
            title=data.title, author=data.author, isbn=data.isbn,
            publisher=data.publisher, total_copies=data.total_copies
        )
        return {"book": book}
    
    async def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        book = await self.repository.get_book(book_id)
        if book:
            return {"book": book}
        return None
    
    async def list_books(self, search: str = None, skip: int = 0,
                        limit: int = 100) -> Dict[str, Any]:
        books = await self.repository.list_books(search, skip, limit)
        return {"books": books}
    
    async def issue_book(self, data: LoanCreate) -> Dict[str, Any]:
        book = await self.repository.get_book(data.book_id)
        if not book or book.available_copies <= 0:
            return {"error": "Book not available"}
        
        loan = await self.repository.create_loan(
            book_id=data.book_id, user_id=data.user_id, due_days=data.due_days
        )
        return {"loan": loan}
    
    async def return_book(self, loan_id: int) -> Dict[str, Any]:
        loan = await self.repository.return_book(loan_id)
        if loan:
            return {"loan": loan}
        return {"error": "Loan not found"}


__all__ = ["LibraryService"]
