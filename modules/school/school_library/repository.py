# School Library Repository
# ====================

from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .models import SchoolBook, SchoolBookLoan, SchoolBookReservation


class LibraryRepository:
    """Repository for school library operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Book Operations
    async def create_book(self, data: dict) -> SchoolBook:
        """Create a new book"""
        book = SchoolBook(**data)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book
    
    async def get_book(self, book_id: int) -> Optional[SchoolBook]:
        """Get a book by ID"""
        result = await self.db.execute(
            select(SchoolBook).where(SchoolBook.id == book_id)
        )
        return result.scalar_one_or_none()
    
    async def get_book_by_isbn(self, isbn: str) -> Optional[SchoolBook]:
        """Get a book by ISBN"""
        result = await self.db.execute(
            select(SchoolBook).where(SchoolBook.isbn == isbn)
        )
        return result.scalar_one_or_none()
    
    async def list_books(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolBook]:
        """List books with optional filters"""
        query = select(SchoolBook)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (SchoolBook.title.ilike(search_term)) |
                (SchoolBook.author.ilike(search_term)) |
                (SchoolBook.isbn.ilike(search_term))
            )
        
        if category:
            query = query.where(SchoolBook.category == category)
        
        query = query.offset(skip).limit(limit).order_by(SchoolBook.title)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update_book(self, book_id: int, data: dict) -> Optional[SchoolBook]:
        """Update a book"""
        book = await self.get_book(book_id)
        if book:
            for key, value in data.items():
                if value is not None:
                    setattr(book, key, value)
            await self.db.commit()
            await self.db.refresh(book)
        return book
    
    async def delete_book(self, book_id: int) -> bool:
        """Delete a book"""
        book = await self.get_book(book_id)
        if book:
            await self.db.delete(book)
            await self.db.commit()
            return True
        return False
    
    # Book Loan Operations
    async def create_loan(self, data: dict) -> SchoolBookLoan:
        """Create a new book loan"""
        loan = SchoolBookLoan(**data)
        self.db.add(loan)
        await self.db.commit()
        await self.db.refresh(loan)
        return loan
    
    async def get_loan(self, loan_id: int) -> Optional[SchoolBookLoan]:
        """Get a loan by ID"""
        result = await self.db.execute(
            select(SchoolBookLoan).where(SchoolBookLoan.id == loan_id)
        )
        return result.scalar_one_or_none()
    
    async def list_loans(
        self,
        student_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolBookLoan]:
        """List loans with filters"""
        query = select(SchoolBookLoan)
        
        if student_id:
            query = query.where(SchoolBookLoan.student_id == student_id)
        
        if status:
            query = query.where(SchoolBookLoan.status == status)
        
        query = query.offset(skip).limit(limit).order_by(SchoolBookLoan.issue_date.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def return_book(self, loan_id: int, return_date: date) -> Optional[SchoolBookLoan]:
        """Return a book"""
        loan = await self.get_loan(loan_id)
        if loan:
            loan.return_date = return_date
            loan.status = "returned"
            
            # Increase available copies
            book = await self.get_book(loan.book_id)
            if book:
                book.available_copies = book.available_copies + 1
            
            await self.db.commit()
            await self.db.refresh(loan)
        return loan
    
    async def get_overdue_loans(self) -> List[SchoolBookLoan]:
        """Get overdue loans"""
        today = date.today()
        query = select(SchoolBookLoan).where(
            SchoolBookLoan.status == "issued",
            SchoolBookLoan.due_date < today
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    # Library Summary
    async def get_library_summary(self) -> dict:
        """Get library summary statistics"""
        # Total books and copies
        books_result = await self.db.execute(
            select(
                func.count(SchoolBook.id),
                func.sum(SchoolBook.total_copies),
                func.sum(SchoolBook.available_copies)
            )
        )
        row = books_result.one()
        
        # Books issued
        loans_result = await self.db.execute(
            select(func.count(SchoolBookLoan.id)).where(
                SchoolBookLoan.status == "issued"
            )
        )
        books_issued = loans_result.scalar() or 0
        
        # Overdue books
        today = date.today()
        overdue_result = await self.db.execute(
            select(func.count(SchoolBookLoan.id)).where(
                SchoolBookLoan.status == "issued",
                SchoolBookLoan.due_date < today
            )
        )
        overdue_books = overdue_result.scalar() or 0
        
        return {
            "total_books": row[0] or 0,
            "total_copies": row[1] or 0,
            "available_copies": row[2] or 0,
            "books_issued": books_issued,
            "overdue_books": overdue_books
        }


__all__ = ["LibraryRepository", "SchoolBook", "SchoolBookLoan", "SchoolBookReservation"]