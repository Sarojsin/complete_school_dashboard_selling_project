from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from backup.core.database import get_async_db
from backup.dependencies.auth import get_current_authority, get_current_student
from backup.models.models import User
from backup.repositories.fee_repository import FeeRepository
from backup.repositories.student_repository import StudentRepository
from backup.schemas.misc import FeeRecordCreate, FeeRecordUpdate, FeeRecordResponse

router = APIRouter()

# AUTHORITY ENDPOINTS

@router.post("/", response_model=FeeRecordResponse)
async def create_fee_record(
    fee: FeeRecordCreate,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Create fee record (Authority only)"""
    # Verify student exists
    student = await StudentRepository.get_by_id(db, fee.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    created_fee = await FeeRepository.create(db, fee.dict())
    return created_fee

@router.post("/bulk")
async def create_bulk_fees(
    fees: List[FeeRecordCreate],
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Create multiple fee records (Authority only)"""
    if not fees:
        raise HTTPException(status_code=400, detail="No fee records provided")
    
    created_fees = await FeeRepository.create_bulk(db, [f.dict() for f in fees])
    
    return {
        "message": f"Created {len(created_fees)} fee records",
        "fees": created_fees
    }

@router.put("/{fee_id}", response_model=FeeRecordResponse)
async def update_fee_record(
    fee_id: int,
    fee_update: FeeRecordUpdate,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Update fee record (Authority only)"""
    fee = await FeeRepository.get_by_id(db, fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee record not found")
    
    updated_fee = await FeeRepository.update(db, fee, **fee_update.dict(exclude_unset=True))
    return updated_fee

@router.post("/{fee_id}/payment")
async def record_payment(
    fee_id: int,
    amount: float,
    payment_date: date = None,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Record payment for a fee (Authority only)"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    fee = await FeeRepository.record_payment(db, fee_id, amount, payment_date)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee record not found")
    
    return {
        "message": "Payment recorded successfully",
        "fee": fee
    }

@router.delete("/{fee_id}")
async def delete_fee_record(
    fee_id: int,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete fee record (Authority only)"""
    fee = await FeeRepository.get_by_id(db, fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee record not found")
    
    await FeeRepository.delete(db, fee)
    return {"message": "Fee record deleted successfully"}

@router.get("/summary")
async def get_all_fees_summary(
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Get summary of all fees (Authority only)"""
    summary = await FeeRepository.get_all_fees_summary(db)
    return summary

@router.get("/overdue")
async def get_all_overdue_fees(
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all overdue fees (Authority only)"""
    overdue_fees = await FeeRepository.get_overdue_fees(db)
    return overdue_fees

@router.get("/student/{student_id}")
async def get_student_fees(
    student_id: int,
    status: str = None,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Get fees for a specific student (Authority only)"""
    student = await StudentRepository.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    fees = await FeeRepository.get_student_fees(db, student_id, status)
    summary = await FeeRepository.get_fee_summary(db, student_id)
    
    return {
        "student": student,
        "fees": fees,
        "summary": summary
    }

@router.get("/type/{fee_type}")
async def get_fees_by_type(
    fee_type: str,
    current_user: User = Depends(get_current_authority),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all fees of a specific type (Authority only)"""
    fees = await FeeRepository.get_fees_by_type(db, fee_type)
    return fees

# STUDENT ENDPOINTS

@router.get("/my-fees")
async def get_my_fees(
    status: str = None,
    current_user: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's fee records"""
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    fees = await FeeRepository.get_student_fees(db, student.id, status)
    summary = await FeeRepository.get_fee_summary(db, student.id)
    
    return {
        "fees": fees,
        "summary": summary
    }

@router.get("/my-fees/pending")
async def get_my_pending_fees(
    current_user: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's pending fees"""
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    pending_fees = await FeeRepository.get_pending_fees(db, student.id)
    
    return {
        "pending_fees": pending_fees,
        "count": len(pending_fees)
    }

@router.get("/my-fees/overdue")
async def get_my_overdue_fees(
    current_user: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's overdue fees"""
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    overdue_fees = await FeeRepository.get_overdue_fees(db, student.id)
    
    return {
        "overdue_fees": overdue_fees,
        "count": len(overdue_fees)
    }

@router.get("/my-fees/payment-history")
async def get_my_payment_history(
    current_user: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's payment history"""
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    payment_history = await FeeRepository.get_payment_history(db, student.id)
    
    return {
        "payment_history": payment_history
    }