from typing import List
from app.repositories.library_repository import LibraryRepository
from app.schemas.library_schemas import BookLoanCreate, BookLoanResponse

class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository
    
    async def issue_book(self, loan_data: BookLoanCreate) -> BookLoanResponse:
        loan = await self.repository.create_loan(loan_data)
        return BookLoanResponse.from_orm(loan)
    
    async def return_book(self, loan_id: int) -> BookLoanResponse:
        loan = await self.repository.return_loan(loan_id)
        return BookLoanResponse.from_orm(loan) if loan else None
    
    async def get_student_loans(self, student_id: int) -> List[BookLoanResponse]:
        loans = await self.repository.get_student_loans(student_id)
        return [BookLoanResponse.from_orm(loan) for loan in loans]
    
    async def get_all_loans(self) -> List[BookLoanResponse]:
        loans = await self.repository.get_all_loans()
        return [BookLoanResponse.from_orm(loan) for loan in loans]
    
    async def get_overdue_loans(self) -> List[BookLoanResponse]:
        loans = await self.repository.get_overdue_loans()
        return [BookLoanResponse.from_orm(loan) for loan in loans]
