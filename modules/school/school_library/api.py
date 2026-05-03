from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_library
from modules.school.school_library.models import SchoolBook, SchoolBookLoan, SchoolBookReservation
from modules.shared.models import User

router = APIRouter()


@router.post("/loans")
async def issue_book(
    student_id: int,
    book_id: int,
    due_date: str,
    current_user: User = Depends(require_library),
    db: AsyncSession = Depends(get_db)
):
    """Issue a book to a student (Library Manager only)"""
    # Use SchoolBookLoan model
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    
    # Check if book is available (not already on loan)
    result = await db.execute(
        select(SchoolBookLoan).where(
            SchoolBookLoan.book_id == book_id,
            SchoolBookLoan.return_date == None
        )
    )
    existing_loan = result.scalars().first()
    if existing_loan:
        raise HTTPException(status_code=400, detail="Book is already on loan")
    
    # Create loan
    loan = SchoolBookLoan(
        student_id=student_id,
        book_id=book_id,
        issue_date=datetime.utcnow().date(),
        due_date=due_date_obj,
        return_date=None,
        status="issued"
    )
    db.add(loan)
    await db.commit()
    await db.refresh(loan)
    
    return loan


@router.post("/loans/{loan_id}/return")
async def return_book(
    loan_id: int,
    current_user: User = Depends(require_library),
    db: AsyncSession = Depends(get_db)
):
    """Mark a book as returned (Library Manager only)"""
    # Use SchoolBookLoan model
    result = await db.execute(
        select(SchoolBookLoan).where(SchoolBookLoan.id == loan_id)
    )
    loan = result.scalars().first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    loan.return_date = datetime.utcnow().date()
    loan.status = "returned"
    await db.commit()
    await db.refresh(loan)
    
    return loan


@router.get("/loans")
async def get_all_loans(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_library),
    db: AsyncSession = Depends(get_db)
):
    """Get all book loans (Library Manager only)"""
    # Use SchoolBookLoan model
    result = await db.execute(
        select(SchoolBookLoan).offset(skip).limit(limit)
    )
    loans = result.scalars().all()
    
    return {"loans": loans}


@router.get("/loans/student/{student_id}")
async def get_student_loans(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get loans for a specific student"""
    # Use SchoolBookLoan model
    result = await db.execute(
        select(SchoolBookLoan).where(SchoolBookLoan.student_id == student_id)
    )
    loans = result.scalars().all()
    
    return {"student_id": student_id, "loans": loans}


# Additional endpoints for students

@router.get("/my-loans")
async def get_my_loans(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's book loans"""
    # Use SchoolBookLoan model
    result = await db.execute(
        select(SchoolBookLoan).where(SchoolBookLoan.student_id == student.id)
    )
    loans = result.scalars().all()
    
    return {"loans": loans}


__all__ = ["router"]