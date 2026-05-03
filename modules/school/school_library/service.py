# School Library Service
# ==================

from typing import Dict, Any, Optional, List
from datetime import date, timedelta

from .repository import LibraryRepository
from .schemas import (
    BookCreate,
    BookUpdate,
    BookLoanCreate,
    LibrarySummary
)


class LibraryService:
    """Service for school library operations"""
    
    def __init__(self, repository: LibraryRepository):
        self.repository = repository
    
    # Book Operations
    async def create_book(self, data: BookCreate) -> Dict[str, Any]:
        """Create a new book"""
        book = await self.repository.create_book(data.model_dump())
        return {
            "book": {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "available_copies": book.available_copies
            }
        }
    
    async def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get a book by ID"""
        book = await self.repository.get_book(book_id)
        if book:
            return {
                "book": {
                    "id": book.id,
                    "isbn": book.isbn,
                    "title": book.title,
                    "author": book.author,
                    "publisher": book.publisher,
                    "category": book.category,
                    "total_copies": book.total_copies,
                    "available_copies": book.available_copies,
                    "shelf_location": book.shelf_location
                }
            }
        return None
    
    async def list_books(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List books"""
        books = await self.repository.list_books(search, category, skip, limit)
        return [
            {
                "id": b.id,
                "isbn": b.isbn,
                "title": b.title,
                "author": b.author,
                "category": b.category,
                "available_copies": b.available_copies
            }
            for b in books
        ]
    
    async def update_book(self, book_id: int, data: BookUpdate) -> Optional[Dict[str, Any]]:
        """Update a book"""
        update_data = data.model_dump(exclude_unset=True)
        book = await self.repository.update_book(book_id, update_data)
        if book:
            return {"book": {"id": book.id, "title": book.title}}
        return None
    
    async def delete_book(self, book_id: int) -> bool:
        """Delete a book"""
        return await self.repository.delete_book(book_id)
    
    # Book Loan Operations
    async def issue_book(self, data: BookLoanCreate) -> Dict[str, Any]:
        """Issue a book to a student"""
        book = await self.repository.get_book(data.book_id)
        if not book:
            raise ValueError("Book not found")
        
        if book.available_copies <= 0:
            raise ValueError("No copies available")
        
        # Decrease available copies
        book.available_copies = book.available_copies - 1
        
        # Create loan record
        loan_data = data.model_dump()
        loan = await self.repository.create_loan(loan_data)
        
        await self.repository.db.commit()
        
        return {
            "loan": {
                "id": loan.id,
                "book_id": loan.book_id,
                "student_id": loan.student_id,
                "issue_date": loan.issue_date.isoformat(),
                "due_date": loan.due_date.isoformat(),
                "status": loan.status
            }
        }
    
    async def return_book(self, loan_id: int) -> Dict[str, Any]:
        """Return a book"""
        loan = await self.repository.return_book(loan_id, date.today())
        if not loan:
            raise ValueError("Loan not found")
        
        return {
            "loan": {
                "id": loan.id,
                "status": loan.status,
                "return_date": loan.return_date.isoformat()
            }
        }
    
    async def get_student_loans(self, student_id: int) -> List[Dict[str, Any]]:
        """Get loans for a student"""
        loans = await self.repository.list_loans(student_id=student_id)
        return [
            {
                "id": l.id,
                "book_id": l.book_id,
                "issue_date": l.issue_date.isoformat(),
                "due_date": l.due_date.isoformat(),
                "status": l.status
            }
            for l in loans
        ]
    
    async def get_overdue_loans(self) -> List[Dict[str, Any]]:
        """Get overdue loans"""
        loans = await self.repository.get_overdue_loans()
        return [
            {
                "id": l.id,
                "book_id": l.book_id,
                "student_id": l.student_id,
                "due_date": l.due_date.isoformat(),
                "days_overdue": (date.today() - l.due_date).days
            }
            for l in loans
        ]
    
    # Library Summary
    async def get_library_summary(self) -> Dict[str, Any]:
        """Get library summary"""
        return await self.repository.get_library_summary()


__all__ = ["LibraryService"]