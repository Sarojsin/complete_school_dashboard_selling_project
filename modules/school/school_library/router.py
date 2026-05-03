# School Library API Routes
# ===================

from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User, UserRole
from .repository import LibraryRepository
from .service import LibraryService
from .schemas import (
    BookCreate,
    BookUpdate,
    BookLoanCreate
)

router = APIRouter(prefix="/library", tags=["School Library"], dependencies=[Depends(require_school_portal)])


def get_service(db: AsyncSession = Depends(get_db)) -> LibraryService:
    repository = LibraryRepository(db)
    return LibraryService(repository)


# Book Endpoints
@router.post("/books", status_code=201)
async def create_book(
    data: BookCreate,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Create a new book"""
    # Only authority or admin can create books
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create books")
    result = await service.create_book(data)
    return result


@router.get("/books/{book_id}")
async def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Get a book by ID"""
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books")
async def list_books(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """List books with filters"""
    books = await service.list_books(search, category, skip, limit)
    return {"books": books, "count": len(books)}


@router.put("/books/{book_id}")
async def update_book(
    book_id: int,
    data: BookUpdate,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Update a book"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to update books")
    book = await service.update_book(book_id, data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Delete a book"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to delete books")
    success = await service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


# Book Loan Endpoints
@router.post("/loans", status_code=201)
async def issue_book(
    data: BookLoanCreate,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Issue a book to a student"""
    try:
        result = await service.issue_book(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/loans/{loan_id}/return")
async def return_book(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Return a book"""
    try:
        result = await service.return_book(loan_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/loans/student/{student_id}")
async def get_student_loans(
    student_id: int,
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Get loans for a student"""
    loans = await service.get_student_loans(student_id)
    return {"loans": loans}


@router.get("/loans/overdue")
async def get_overdue_loans(
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Get overdue loans"""
    loans = await service.get_overdue_loans()
    return {"loans": loans, "count": len(loans)}


# Library Summary
@router.get("/summary")
async def get_library_summary(
    current_user: User = Depends(get_current_user),
    service: LibraryService = Depends(get_service)
):
    """Get library summary"""
    return await service.get_library_summary()


__all__ = ["router"]