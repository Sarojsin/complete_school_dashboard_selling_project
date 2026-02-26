from typing import List, Optional
from app.repositories.library_repository import LibraryRepository
from app.schemas.library_schemas import BookLoanCreate, BookLoanResponse, BookCreate, BookResponse
from app.models.library_models import BookLoan, Book

class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository
    
    async def issue_book(self, loan_data: BookLoanCreate) -> BookLoanResponse:
        loan = await self.repository.create_loan(loan_data)
        return BookLoanResponse.model_validate(loan)
    
    async def return_book(self, loan_id: int) -> Optional[BookLoanResponse]:
        loan = await self.repository.return_loan(loan_id)
        return BookLoanResponse.model_validate(loan) if loan else None
    
    async def get_student_loans(self, student_id: int) -> List[BookLoanResponse]:
        loans = await self.repository.get_student_loans(student_id)
        return [BookLoanResponse.model_validate(loan) for loan in loans]
    
    async def get_all_loans(self) -> List[BookLoanResponse]:
        loans = await self.repository.get_all_loans()
        return [BookLoanResponse.model_validate(loan) for loan in loans]
    
    async def get_overdue_loans(self) -> List[BookLoanResponse]:
        loans = await self.repository.get_overdue_loans()
        return [BookLoanResponse.model_validate(loan) for loan in loans]
    
    async def get_dashboard_stats(self) -> dict:
        """Get library dashboard statistics"""
        return await self.repository.get_library_dashboard_stats()
    
    async def add_book(self, book_data: BookCreate) -> BookResponse:
        """Add a new book to catalog"""
        book = await self.repository.create_book(book_data)
        return BookResponse.model_validate(book)
    
    async def search_books(self, query: str) -> List[BookResponse]:
        """Search books in catalog"""
        books = await self.repository.search_books(query)
        return [BookResponse.model_validate(book) for book in books]
    
    async def get_all_books(self) -> List[BookResponse]:
        """Get all books in catalog"""
        books = await self.repository.get_all_books()
        return [BookResponse.model_validate(book) for book in books]
    
    async def get_all_loans_with_names(self):
        """Get all loans with student names"""
        return await self.repository.get_all_loans_with_student_names()
    
    async def get_student_history(self, student_id: int) -> List[BookLoan]:
        """Get borrowing history for a student"""
        return await self.repository.get_student_history(student_id)
