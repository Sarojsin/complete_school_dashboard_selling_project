"""
College Library Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from datetime import date, timedelta
from backup.models.library_models import Book, BookLoan


class LibraryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_book(self, title: str, author: str, isbn: str,
                        publisher: str = None, total_copies: int = 1) -> Book:
        book = Book(title=title, author=author, isbn=isbn,
                   publisher=publisher, total_copies=total_copies,
                   available_copies=total_copies)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book
    
    async def get_book(self, book_id: int) -> Optional[Book]:
        result = await self.db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()
    
    async def list_books(self, search: str = None, skip: int = 0,
                        limit: int = 100) -> List[Book]:
        query = select(Book)
        if search:
            query = query.where(
                (Book.title.ilike(f"%{search}%")) |
                (Book.author.ilike(f"%{search}%"))
            )
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create_loan(self, book_id: int, user_id: int,
                         due_days: int = 14) -> BookLoan:
        loan = BookLoan(
            book_id=book_id,
            user_id=user_id,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=due_days)
        )
        self.db.add(loan)
        book = await self.get_book(book_id)
        if book and book.available_copies > 0:
            book.available_copies = int(book.available_copies) - 1
        await self.db.commit()
        await self.db.refresh(loan)
        return loan
    
    async def return_book(self, loan_id: int) -> Optional[BookLoan]:
        loan_result = await self.db.execute(
            select(BookLoan).where(BookLoan.id == loan_id)
        )
        loan = loan_result.scalar_one_or_none()
        if loan and not loan.return_date:
            loan.return_date = date.today()
            book = await self.get_book(loan.book_id)
            if book:
                book.available_copies = int(book.available_copies) + 1
            await self.db.commit()
            await self.db.refresh(loan)
        return loan


__all__ = ["LibraryRepository"]
