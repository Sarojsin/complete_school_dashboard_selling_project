from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_async_db, get_current_user
from app.models.models import User, UserRole
from app.repositories.library_repository import LibraryRepository
from app.services.library_service import LibraryService
from app.schemas.library_schemas import BookLoanCreate, BookLoanResponse

router = APIRouter(prefix="/api/library", tags=["Library"])

@router.post("/loans", response_model=BookLoanResponse)
async def issue_book(
    loan_data: BookLoanCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Only Library Manager can issue books")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    return await service.issue_book(loan_data)

@router.post("/loans/{loan_id}/return", response_model=BookLoanResponse)
async def return_book(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Only Library Manager can return books")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    result = await service.return_book(loan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Loan not found")
    return result

@router.get("/loans", response_model=List[BookLoanResponse])
async def get_all_loans(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.LIBRARY_MANAGER:
        raise HTTPException(status_code=403, detail="Only Library Manager can view all loans")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    return await service.get_all_loans()

@router.get("/loans/student/{student_id}", response_model=List[BookLoanResponse])
async def get_student_loans(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    # Students can view their own loans
    if current_user.role == UserRole.STUDENT and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Can only view own loans")
    
    repo = LibraryRepository(db)
    service = LibraryService(repo)
    return await service.get_student_loans(student_id)
