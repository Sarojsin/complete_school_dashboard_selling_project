"""
College Account Section API Routes

API endpoints for college fees and finance.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college.fee import CollegeFee, CollegeFeeRecord
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/account", tags=["College Account"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_account_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get account dashboard"""
    total_fees = await db.execute(select(func.sum(CollegeFeeRecord.amount)))
    total_paid = await db.execute(select(func.sum(CollegeFeeRecord.paid_amount)))
    
    return {
        "total_fees": total_fees.scalar() or 0,
        "total_paid": total_paid.scalar() or 0
    }


@router.get("/fee-structures")
async def get_fee_structures(
    program_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fee structures"""
    query = select(CollegeFee)
    if program_id:
        query = query.where(CollegeFee.program_id == program_id)
    
    result = await db.execute(query)
    fees = result.scalars().all()
    return {"fee_structures": fees}


@router.get("/fee-records")
async def get_fee_records(
    student_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fee records"""
    query = select(CollegeFeeRecord)
    if student_id:
        query = query.where(CollegeFeeRecord.student_id == student_id)
    
    result = await db.execute(query)
    fees = result.scalars().all()
    return {"fee_records": fees}


__all__ = ["router"]
