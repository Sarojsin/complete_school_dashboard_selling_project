# School Account Section API Routes
# ================================

from typing import Optional, List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.database import get_async_db
from backup.modules.school.account_section.repository import AccountSectionRepository
from backup.modules.school.account_section.service import AccountSectionService
from backup.modules.school.account_section.schemas import (
    SchoolFeeCreate,
    SchoolFeeUpdate,
    SchoolFeePayment,
    SchoolExpenseCreate,
    SchoolExpenseUpdate
)

router = APIRouter(prefix="/account", tags=["School Account Section"])


def get_service(db: AsyncSession = Depends(get_async_db)) -> AccountSectionService:
    repository = AccountSectionRepository(db)
    return AccountSectionService(repository)


# Fee Endpoints
@router.post("/fees", status_code=201)
async def create_fee(
    data: SchoolFeeCreate,
    service: AccountSectionService = Depends(get_service)
):
    """Create a new fee record"""
    result = await service.create_fee(data)
    return result


@router.get("/fees/{fee_id}")
async def get_fee(
    fee_id: int,
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
    service: AccountSectionService = Depends(get_service)
):
    """List fees with filters"""
    fees = await service.list_fees(student_id, payment_status, skip, limit)
    return {"fees": fees, "count": len(fees)}


@router.put("/fees/{fee_id}")
async def update_fee(
    fee_id: int,
    data: SchoolFeeUpdate,
    service: AccountSectionService = Depends(get_service)
):
    """Update a fee record"""
    fee = await service.update_fee(fee_id, data)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")
    return fee


@router.delete("/fees/{fee_id}")
async def delete_fee(
    fee_id: int,
    service: AccountSectionService = Depends(get_service)
):
    """Delete a fee record"""
    success = await service.delete_fee(fee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fee not found")
    return {"message": "Fee deleted successfully"}


@router.post("/fees/{fee_id}/payment")
async def make_payment(
    fee_id: int,
    payment: SchoolFeePayment,
    service: AccountSectionService = Depends(get_service)
):
    """Process payment for a fee"""
    result = await service.make_payment(fee_id, payment)
    if not result:
        raise HTTPException(status_code=404, detail="Fee not found")
    return result


# Expense Endpoints
@router.post("/expenses", status_code=201)
async def create_expense(
    data: SchoolExpenseCreate,
    service: AccountSectionService = Depends(get_service)
):
    """Create a new expense record"""
    result = await service.create_expense(data)
    return result


@router.get("/expenses/{expense_id}")
async def get_expense(
    expense_id: int,
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
    service: AccountSectionService = Depends(get_service)
):
    """List expenses with filters"""
    expenses = await service.list_expenses(category, start_date, end_date, skip, limit)
    return {"expenses": expenses, "count": len(expenses)}


@router.put("/expenses/{expense_id}")
async def update_expense(
    expense_id: int,
    data: SchoolExpenseUpdate,
    service: AccountSectionService = Depends(get_service)
):
    """Update an expense record"""
    expense = await service.update_expense(expense_id, data)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    service: AccountSectionService = Depends(get_service)
):
    """Delete an expense record"""
    success = await service.delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


# Financial Summary
@router.get("/summary")
async def get_financial_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    service: AccountSectionService = Depends(get_service)
):
    """Get financial summary"""
    summary = await service.get_financial_summary(start_date, end_date)
    return summary


__all__ = ["router"]
