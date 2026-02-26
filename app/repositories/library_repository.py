from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional, Tuple
from app.models.models import Student
from app.models.library_models import BookLoan, Book
from app.schemas.library_schemas import BookLoanCreate, BookCreate
from datetime import datetime, date, timedelta

class LibraryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_book(self, book_data: BookCreate) -> Book:
        """Create a new book in catalog"""
        db_book = Book(
            **book_data.dict(),
            available_copies=book_data.total_copies,
            added_at=datetime.utcnow()
        )
        
        self.session.add(db_book)
        await self.session.commit()
        await self.session.refresh(db_book)
        return db_book
    
    async def get_all_books(self) -> List[Book]:
        """Get all books in catalog"""
        result = await self.session.execute(
            select(Book).order_by(Book.title)
        )
        return result.scalars().all()
    
    async def search_books(self, query: str) -> List[Book]:
        """Search books by title, author, or ISBN"""
        search_term = f"%{query}%"
        result = await self.session.execute(
            select(Book)
            .where(
                or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term),
                    Book.isbn.ilike(search_term)
                )
            )
            .order_by(Book.title)
        )
        return result.scalars().all()
    
    async def update_book_availability(self, book_id: int, delta: int) -> Optional[Book]:
        """Update available copies (positive for return, negative for issue)"""
        result = await self.session.execute(
            select(Book).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        
        if book:
            book.available_copies = max(0, book.available_copies + delta)
            await self.session.commit()
        
        return book
    
    async def create_loan(self, loan_data: BookLoanCreate) -> BookLoan:
        # Validate book availability before issuing
        if loan_data.book_id:
            book = await self.session.get(Book, loan_data.book_id)
            if not book:
                raise ValueError("Book not found in catalog")
            # Use int() to extract the actual value from the Column
            available = int(book.available_copies) if book.available_copies is not None else 0
            if available <= 0:
                raise ValueError("Book not available for borrowing - no copies left")
        
        due_date = datetime.utcnow().date() + timedelta(days=loan_data.due_days)
        
        db_loan = BookLoan(
            student_id=loan_data.student_id,
            book_id=loan_data.book_id,
            book_title=loan_data.book_title,
            book_author=loan_data.book_author,
            book_isbn=loan_data.book_isbn,
            taken_date=datetime.utcnow().date(),
            due_date=due_date,
            status="borrowed"
        )
        
        # Use atomic transaction - add loan and update availability together
        try:
            self.session.add(db_loan)
            await self.session.flush()  # Get loan ID without committing
            
            # Update book availability if book_id is provided
            if loan_data.book_id:
                await self._update_book_availability_no_commit(loan_data.book_id, -1)
            
            await self.session.commit()
            await self.session.refresh(db_loan)
        except Exception as e:
            await self.session.rollback()
            raise
        
        return db_loan
    
    async def _update_book_availability_no_commit(self, book_id: int, delta: int) -> Optional[Book]:
        """Update available copies without committing (for atomic transactions)"""
        result = await self.session.execute(
            select(Book).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        
        if book:
            book.available_copies = max(0, book.available_copies + delta)
        
        return book
    
    async def return_loan(self, loan_id: int) -> Optional[BookLoan]:
        result = await self.session.execute(
            select(BookLoan).where(BookLoan.id == loan_id)
        )
        loan = result.scalar_one_or_none()
        
        if not loan:
            return None
            
        # Extract values from SQLAlchemy columns
        loan_status = str(loan.status) if loan.status else ""
        if loan_status == "returned":
            raise ValueError("Book has already been returned")
        
        loan.return_date = datetime.utcnow().date()
        loan.status = "returned"
        
        # Calculate fine if overdue
        due_date_val = loan.due_date
        return_date_val = loan.return_date
        if return_date_val and due_date_val and return_date_val > due_date_val:
            days_overdue = (return_date_val - due_date_val).days
            loan.fine_amount = days_overdue * 10  # 10 rupees per day
        
        # Use atomic transaction
        try:
            await self.session.flush()
            
            # Update book availability if book_id is provided
            book_id_val = loan.book_id
            if book_id_val is not None:
                book_id_int = int(book_id_val) if hasattr(book_id_val, '__int__') else book_id_val
                await self._update_book_availability_no_commit(book_id_int, 1)
            
            await self.session.commit()
            await self.session.refresh(loan)
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Failed to return book: {str(e)}")
        
        return loan
    
    async def get_student_loans(self, student_id: int) -> List[BookLoan]:
        result = await self.session.execute(
            select(BookLoan)
            .where(BookLoan.student_id == student_id)
            .order_by(BookLoan.taken_date.desc())
        )
        return result.scalars().all()
    
    async def get_student_history(self, student_id: int) -> List[BookLoan]:
        """Get all loan history for a student including returned books"""
        return await self.get_student_loans(student_id)
    
    async def get_all_loans(self) -> List[BookLoan]:
        result = await self.session.execute(
            select(BookLoan)
            .join(Student, BookLoan.student_id == Student.id)
            .order_by(BookLoan.taken_date.desc())
        )
        return result.scalars().all()
    
    async def get_all_loans_with_student_names(self) -> List[Tuple[BookLoan, str]]:
        """Get all loans with student names for display"""
        result = await self.session.execute(
            select(BookLoan, Student.full_name)
            .join(Student, BookLoan.student_id == Student.id)
            .order_by(BookLoan.taken_date.desc())
        )
        return result.all()
    
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
    
    async def get_library_dashboard_stats(self) -> dict:
        """Get dashboard statistics for library"""
        today = datetime.utcnow().date()
        
        # Total borrowed books
        borrowed_result = await self.session.execute(
            select(func.count(BookLoan.id)).where(BookLoan.status == "borrowed")
        )
        borrowed_count = borrowed_result.scalar() or 0
        
        # Total overdue books
        overdue_result = await self.session.execute(
            select(func.count(BookLoan.id))
            .where(and_(
                BookLoan.status == "borrowed",
                BookLoan.due_date < today
            ))
        )
        overdue_count = overdue_result.scalar() or 0
        
        # Total fines
        fines_result = await self.session.execute(
            select(func.sum(BookLoan.fine_amount)).where(BookLoan.fine_amount > 0)
        )
        total_fines = fines_result.scalar() or 0
        
        # Total books in catalog
        books_result = await self.session.execute(
            select(func.count(Book.id))
        )
        total_books = books_result.scalar() or 0
        
        # Books returned today
        returned_today_result = await self.session.execute(
            select(func.count(BookLoan.id))
            .where(BookLoan.return_date == today)
        )
        returned_today = returned_today_result.scalar() or 0
        
        # Books issued today
        issued_today_result = await self.session.execute(
            select(func.count(BookLoan.id))
            .where(BookLoan.taken_date == today)
        )
        issued_today = issued_today_result.scalar() or 0
        
        return {
            "total_borrowed": borrowed_count,
            "total_overdue": overdue_count,
            "total_fines": total_fines,
            "total_books": total_books,
            "books_returned_today": returned_today,
            "books_issued_today": issued_today
        }
