# School Account Section API Routes
# ================================

from typing import Optional, List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User, UserRole
from .repository import AccountSectionRepository
from .service import AccountSectionService
from .schemas import (
    SchoolFeeCreate,
    SchoolFeeUpdate,
    SchoolFeePayment,
    SchoolExpenseCreate,
    SchoolExpenseUpdate,
    SchoolFeeBulkCreate
)

router = APIRouter(prefix="/account", tags=["School Account Section"], dependencies=[Depends(require_school_portal)])


def get_service(db: AsyncSession = Depends(get_db)) -> AccountSectionService:
    repository = AccountSectionRepository(db)
    return AccountSectionService(repository)


# Fee Endpoints
@router.post("/fees", status_code=201)
async def create_fee(
    data: SchoolFeeCreate,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Create a new fee record"""
    # Only authority or admin can create fees
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create fees")
    result = await service.create_fee(data)
    return result


@router.get("/fees/{fee_id}")
async def get_fee(
    fee_id: int,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Get a fee by ID"""
    fee = await service.get_fee(fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")
    return fee


@router.get("/fees")
async def list_fees(
    student_id: Optional[int] = Query(None),
    payment_status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """List fees with filters"""
    fees = await service.list_fees(student_id, payment_status, skip, limit)
    return {"fees": fees, "count": len(fees)}


@router.put("/fees/{fee_id}")
async def update_fee(
    fee_id: int,
    data: SchoolFeeUpdate,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Update a fee record"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to update fees")
    fee = await service.update_fee(fee_id, data)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")
    return fee


@router.delete("/fees/{fee_id}")
async def delete_fee(
    fee_id: int,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Delete a fee record"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to delete fees")
    success = await service.delete_fee(fee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fee not found")
    return {"message": "Fee deleted successfully"}


@router.post("/fees/{fee_id}/payment")
async def make_payment(
    fee_id: int,
    payment: SchoolFeePayment,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Process payment for a fee"""
    result = await service.make_payment(fee_id, payment)
    if not result:
        raise HTTPException(status_code=404, detail="Fee not found")
    return result


# Bulk Fee Operations
@router.post("/fees/bulk", status_code=201)
async def bulk_create_fees(
    data: SchoolFeeBulkCreate,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Create multiple fee records at once (Authority only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create fees")
    result = await service.bulk_create_fees([f.model_dump() for f in data.fees])
    return result


# Expense Endpoints
@router.post("/expenses", status_code=201)
async def create_expense(
    data: SchoolExpenseCreate,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Create a new expense record"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create expenses")
    result = await service.create_expense(data)
    return result


@router.get("/expenses/{expense_id}")
async def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Get an expense by ID"""
    expense = await service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/expenses")
async def list_expenses(
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """List expenses with filters"""
    expenses = await service.list_expenses(category, start_date, end_date, skip, limit)
    return {"expenses": expenses, "count": len(expenses)}


@router.put("/expenses/{expense_id}")
async def update_expense(
    expense_id: int,
    data: SchoolExpenseUpdate,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Update an expense record"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to update expenses")
    expense = await service.update_expense(expense_id, data)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Delete an expense record"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to delete expenses")
    success = await service.delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


# Financial Summary
@router.get("/summary")
async def get_financial_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    service: AccountSectionService = Depends(get_service)
):
    """Get financial summary"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to view financial summary")
    summary = await service.get_financial_summary(start_date, end_date)
    return summary


__all__ = ["router"]