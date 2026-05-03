"""
College Library API Routes

API endpoints for managing college library books and loans.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime, timedelta

from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.library_models import Book, BookLoan
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/library", tags=["College Library"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_library_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get library dashboard with overview stats"""
    total_books = await db.execute(select(func.count(Book.id)))
    available_books = await db.execute(
        select(func.count(Book.id)).where(Book.available_copies > 0)
    )
    active_loans = await db.execute(
        select(func.count(BookLoan.id)).where(BookLoan.return_date.is_(None))
    )
    
    return {
        "total_books": total_books.scalar() or 0,
        "available_books": available_books.scalar() or 0,
        "active_loans": active_loans.scalar() or 0
    }


@router.get("/books")
async def list_books(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all books in the library"""
    query = select(Book)
    
    if search:
        query = query.where(
            (Book.title.ilike(f"%{search}%")) | 
            (Book.author.ilike(f"%{search}%")) |
            (Book.isbn.ilike(f"%{search}%"))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    books = result.scalars().all()
    
    return {"books": [
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "total_copies": b.total_copies,
            "available_copies": b.available_copies
        }
        for b in books
    ]}


@router.get("/books/{book_id}")
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get book details by ID"""
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publisher": book.publisher,
        "total_copies": book.total_copies,
        "available_copies": book.available_copies
    }


@router.get("/loans")
async def list_loans(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List book loans"""
    query = select(BookLoan)
    
    if status == "active":
        query = query.where(BookLoan.return_date.is_(None))
    elif status == "returned":
        query = query.where(BookLoan.return_date.isnot(None))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    loans = result.scalars().all()
    
    return {"loans": [
        {
            "id": l.id,
            "book_id": l.book_id,
            "user_id": l.user_id,
            "issue_date": str(l.issue_date) if l.issue_date else None,
            "due_date": str(l.due_date) if l.due_date is not None else None,
            "return_date": str(l.return_date) if l.return_date is not None else None
        }
        for l in loans
    ]}


@router.post("/loans/issue")
async def issue_book(
    book_id: int,
    user_id: int,
    due_days: int = 14,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Issue a book to a user"""
    # Check book availability
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if int(book.available_copies) <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Create loan
    loan = BookLoan(
        book_id=book_id,
        user_id=user_id,
        issue_date=datetime.utcnow().date(),
        due_date=(datetime.utcnow() + timedelta(days=due_days)).date()
    )
    db.add(loan)
    
    # Update available copies
    book.available_copies = int(book.available_copies) - 1
    
    await db.commit()
    await db.refresh(loan)
    
    return {"loan": loan, "message": "Book issued successfully"}


@router.post("/loans/{loan_id}/return")
async def return_book(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return a book loan"""
    result = await db.execute(select(BookLoan).where(BookLoan.id == loan_id))
    loan = result.scalar_one_or_none()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Mark as returned
    loan.return_date = datetime.utcnow().date()
    
    # Update available copies
    result = await db.execute(select(Book).where(Book.id == loan.book_id))
    book = result.scalar_one_or_none()
    if book:
        book.available_copies = int(book.available_copies) + 1
    
    await db.commit()
    await db.refresh(loan)
    
    return {"loan": loan, "message": "Book returned successfully"}


__all__ = ["router"]
