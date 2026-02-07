from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from app.models.models import Student
from app.models.library_models import BookLoan
from app.schemas.library_schemas import BookLoanCreate
from datetime import datetime, date, timedelta

class LibraryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_loan(self, loan_data: BookLoanCreate) -> BookLoan:
        due_date = datetime.utcnow().date() + timedelta(days=loan_data.due_days)
        
        db_loan = BookLoan(
            student_id=loan_data.student_id,
            book_title=loan_data.book_title,
            book_author=loan_data.book_author,
            book_isbn=loan_data.book_isbn,
            taken_date=datetime.utcnow().date(),
            due_date=due_date,
            status="borrowed"
        )
        
        self.session.add(db_loan)
        await self.session.commit()
        await self.session.refresh(db_loan)
        return db_loan
    
    async def return_loan(self, loan_id: int) -> BookLoan:
        result = await self.session.execute(
            select(BookLoan).where(BookLoan.id == loan_id)
        )
        loan = result.scalar_one_or_none()
        
        if loan:
            loan.return_date = datetime.utcnow().date()
            loan.status = "returned"
            
            # Calculate fine if overdue
            if loan.return_date > loan.due_date:
                days_overdue = (loan.return_date - loan.due_date).days
                loan.fine_amount = days_overdue * 10  # 10 rupees per day
            
            await self.session.commit()
        
        return loan
    
    async def get_student_loans(self, student_id: int) -> List[BookLoan]:
        result = await self.session.execute(
            select(BookLoan)
            .where(BookLoan.student_id == student_id)
            .order_by(BookLoan.taken_date.desc())
        )
        return result.scalars().all()
    
    async def get_all_loans(self) -> List[BookLoan]:
        result = await self.session.execute(
            select(BookLoan)
            .join(Student, BookLoan.student_id == Student.id)
            .order_by(BookLoan.taken_date.desc())
        )
        return result.scalars().all()
    
    async def get_overdue_loans(self) -> List[BookLoan]:
        today = datetime.utcnow().date()
        result = await self.session.execute(
            select(BookLoan)
            .where(and_(
                BookLoan.status == "borrowed",
                BookLoan.due_date < today
            ))
        )
        return result.scalars().all()
