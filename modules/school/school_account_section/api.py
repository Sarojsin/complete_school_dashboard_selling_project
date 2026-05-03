from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from datetime import datetime, date
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_authority, require_account
from modules.school.school_account_section.models import SchoolFee as Fee, SchoolExpense, SchoolPayment as Payment
from modules.shared.models import User

# Placeholder for StudentRepository
class StudentRepositoryPlaceholder:
    @staticmethod
    async def get_by_user_id(db, user_id):
        from modules.school.school_student.models import SchoolStudent
        result = await db.execute(select(SchoolStudent).where(SchoolStudent.user_id == user_id))
        return result.scalar_one_or_none()

# Alias for backward compatibility
StudentRepository = StudentRepositoryPlaceholder

router = APIRouter()


# Fee Endpoints

@router.post("/fees/")
async def create_fee(
    student_id: int,
    fee_type: str,
    amount: float,
    due_date: str,
    description: Optional[str] = None,
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Create a new fee record (Authority only)"""
    from modules.school.school_account_section.repository import AccountSectionRepository
    # Create fee record using SchoolFee model
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    
    fee = Fee(
        student_id=student_id,
        fee_type=fee_type,
        amount=amount,
        due_date=due_date_obj,
        description=description,
        payment_status="pending"
    )
    db.add(fee)
    await db.commit()
    await db.refresh(fee)
    
    return fee


@router.post("/fees/bulk")
async def bulk_create_fees(
    fees: List[dict],
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    created_fees = []
    errors = []
    
    for fee_data in fees:
        try:
            student_id = fee_data.get("student_id")
            fee_type = fee_data.get("fee_type")
            amount = fee_data.get("amount")
            due_date_str = fee_data.get("due_date")
            description = fee_data.get("description")
            
            if not all([student_id, fee_type, amount, due_date_str]):
                errors.append(f"Missing required fields in record")
                continue
            
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            
            fee = Fee(
                student_id=student_id,
                fee_type=fee_type,
                amount=amount,
                due_date=due_date,
                description=description,
                payment_status="pending"
            )
            db.add(fee)
            created_fees.append(fee)
        except Exception as e:
            errors.append(f"Error: {str(e)}")
    
    await db.commit()
    
    return {
        "created": len(created_fees),
        "errors": errors
    }


@router.get("/fees/summary")
async def get_fees_summary(
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    # Total fees
    total_result = await db.execute(select(func.count(Fee.id)))
    total_fees = total_result.scalar() or 0
    
    # Total amount
    amount_result = await db.execute(select(func.sum(Fee.amount)))
    total_amount = amount_result.scalar() or 0
    
    # Paid
    paid_result = await db.execute(
        select(func.count(Fee.id)).where(Fee.payment_status == "paid")
    )
    paid_count = paid_result.scalar() or 0
    
    # Pending
    pending_result = await db.execute(
        select(func.count(Fee.id)).where(Fee.payment_status == "pending")
    )
    pending_count = pending_result.scalar() or 0
    
    # Overdue
    today = date.today()
    overdue_result = await db.execute(
        select(func.count(Fee.id)).where(
            Fee.payment_status == "pending",
            Fee.due_date < today
        )
    )
    overdue_count = overdue_result.scalar() or 0
    
    return {
        "total_fees": total_fees,
        "total_amount": float(total_amount),
        "paid": paid_count,
        "pending": pending_count,
        "overdue": overdue_count
    }


@router.get("/fees/overdue")
async def get_overdue_fees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    today = date.today()
    
    result = await db.execute(
        select(Fee).where(
            Fee.payment_status == "pending",
            Fee.due_date < today
        ).offset(skip).limit(limit)
    )
    fees = result.scalars().all()
    
    return {"fees": fees, "count": len(fees)}


@router.get("/fees/student/{student_id}")
async def get_student_fees(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    result = await db.execute(
        select(Fee).where(Fee.student_id == student_id)
    )
    fees = result.scalars().all()
    
    return {"student_id": student_id, "fees": fees}


@router.get("/fees/type/{fee_type}")
async def get_fees_by_type(
    fee_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    result = await db.execute(
        select(Fee).where(Fee.fee_type == fee_type).offset(skip).limit(limit)
    )
    fees = result.scalars().all()
    
    return {"fee_type": fee_type, "fees": fees}


# Student my-fees endpoints

@router.get("/fees/student/my")
async def get_my_fees(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    result = await db.execute(
        select(Fee).where(Fee.student_id == student.id)
    )
    fees = result.scalars().all()
    
    return {"fees": fees}


@router.get("/fees/student/my/pending")
async def get_my_pending_fees(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    result = await db.execute(
        select(Fee).where(
            Fee.student_id == student.id,
            Fee.payment_status == "pending"
        )
    )
    fees = result.scalars().all()
    
    return {"fees": fees}


@router.get("/fees/student/my/overdue")
async def get_my_overdue_fees(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    today = date.today()
    result = await db.execute(
        select(Fee).where(
            Fee.student_id == student.id,
            Fee.payment_status == "pending",
            Fee.due_date < today
        )
    )
    fees = result.scalars().all()
    
    return {"fees": fees}


@router.get("/fees/student/my/payment-history")
async def get_my_payment_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fee already imported at module level
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    result = await db.execute(
        select(Fee).where(
            Fee.student_id == student.id,
            Fee.payment_status == "paid"
        )
    )
    fees = result.scalars().all()
    
    return {"payments": fees}


# Account Payments (Teacher salaries)

@router.post("/payments")
async def create_payment(
    teacher_id: int,
    amount: float,
    payment_type: str,
    description: Optional[str] = None,
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    # Payment model - create inline
    
    payment = Payment(
        teacher_id=teacher_id,
        amount=amount,
        payment_type=payment_type,
        description=description,
        payment_date=datetime.utcnow()
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    return payment


@router.get("/payments")
async def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_db)
):
    # Payment model - query only, return empty list placeholder
    
    result = await db.execute(
        select(Payment).offset(skip).limit(limit)
    )
    payments = result.scalars().all()
    
    return {"payments": payments}


@router.get("/payments/teacher/{teacher_id}")
async def get_teacher_payments(
    teacher_id: int,
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_db)
):
    # Payment model - query only
    
    result = await db.execute(
        select(Payment).where(Payment.teacher_id == teacher_id)
    )
    payments = result.scalars().all()
    
    return {"teacher_id": teacher_id, "payments": payments}


@router.get("/stats")
async def get_account_stats(
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_db)
):
    # Use module-level Fee and create placeholder Payment
    
    # Fee stats
    total_fees_result = await db.execute(select(func.sum(Fee.amount)))
    total_fees = total_fees_result.scalar() or 0
    
    # Payment stats
    total_payments_result = await db.execute(select(func.sum(Payment.amount)))
    total_payments = total_payments_result.scalar() or 0
    
    return {
        "total_fees_collected": float(total_fees),
        "total_payments_made": float(total_payments),
        "balance": float(total_fees) - float(total_payments)
    }


__all__ = ["router"]