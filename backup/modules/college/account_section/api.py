# College Account Section API
# ==========================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from modules.shared.database import get_async_db
from backup.modules.college.account_section.repository import AccountSectionRepository
from backup.modules.college.account_section.service import AccountSectionService
from backup.modules.college.account_section.schemas import (
    AccountSectionStaffCreate,
    AccountSectionStaffUpdate,
    AccountSectionStaff,
    FeeStructureCreate,
    FeeStructureUpdate,
    FeeStructure,
    PaymentCreate,
    PaymentUpdate,
    Payment,
    ExpenseCreate,
    ExpenseUpdate,
    Expense,
)

router = APIRouter(prefix="/account-section", tags=["College Account Section"])


def get_service(db: AsyncSession = Depends(get_async_db)) -> AccountSectionService:
    repository = AccountSectionRepository(db)
    return AccountSectionService(repository)


# Staff endpoints
@router.post("/staff", response_model=dict)
async def create_staff(
    data: AccountSectionStaffCreate,
    service: AccountSectionService = Depends(get_service)
):
    return await service.create_staff(data)


@router.get("/staff/{staff_id}", response_model=dict)
async def get_staff(
    staff_id: int,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.get_staff(staff_id)
    if not result:
        raise HTTPException(status_code=404, detail="Staff not found")
    return result


@router.get("/staff", response_model=list)
async def get_all_staff(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: AccountSectionService = Depends(get_service)
):
    return await service.get_all_staff(skip, limit)


@router.put("/staff/{staff_id}", response_model=dict)
async def update_staff(
    staff_id: int,
    data: AccountSectionStaffUpdate,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.update_staff(staff_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Staff not found")
    return result


@router.delete("/staff/{staff_id}")
async def delete_staff(
    staff_id: int,
    service: AccountSectionService = Depends(get_service)
):
    if not await service.delete_staff(staff_id):
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff deleted successfully"}


# Fee Structure endpoints
@router.post("/fee-structure", response_model=dict)
async def create_fee_structure(
    data: FeeStructureCreate,
    service: AccountSectionService = Depends(get_service)
):
    return await service.create_fee_structure(data)


@router.get("/fee-structure/{fee_id}", response_model=dict)
async def get_fee_structure(
    fee_id: int,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.get_fee_structure(fee_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return result


@router.get("/fee-structure", response_model=list)
async def get_all_fee_structures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    program_id: Optional[int] = None,
    service: AccountSectionService = Depends(get_service)
):
    if program_id:
        return await service.get_fee_structures_by_program(program_id)
    return await service.get_all_fee_structures(skip, limit)


@router.put("/fee-structure/{fee_id}", response_model=dict)
async def update_fee_structure(
    fee_id: int,
    data: FeeStructureUpdate,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.update_fee_structure(fee_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return result


@router.delete("/fee-structure/{fee_id}")
async def delete_fee_structure(
    fee_id: int,
    service: AccountSectionService = Depends(get_service)
):
    if not await service.delete_fee_structure(fee_id):
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return {"message": "Fee structure deleted successfully"}


# Payment endpoints
@router.post("/payment", response_model=dict)
async def create_payment(
    data: PaymentCreate,
    service: AccountSectionService = Depends(get_service)
):
    return await service.create_payment(data)


@router.get("/payment/{payment_id}", response_model=dict)
async def get_payment(
    payment_id: int,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.get_payment(payment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result


@router.get("/payment", response_model=list)
async def get_all_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    student_id: Optional[int] = None,
    service: AccountSectionService = Depends(get_service)
):
    if student_id:
        return await service.get_payments_by_student(student_id)
    return await service.get_all_payments(skip, limit)


@router.put("/payment/{payment_id}", response_model=dict)
async def update_payment(
    payment_id: int,
    data: PaymentUpdate,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.update_payment(payment_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result


@router.delete("/payment/{payment_id}")
async def delete_payment(
    payment_id: int,
    service: AccountSectionService = Depends(get_service)
):
    if not await service.delete_payment(payment_id):
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}


# Expense endpoints
@router.post("/expense", response_model=dict)
async def create_expense(
    data: ExpenseCreate,
    service: AccountSectionService = Depends(get_service)
):
    return await service.create_expense(data)


@router.get("/expense/{expense_id}", response_model=dict)
async def get_expense(
    expense_id: int,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.get_expense(expense_id)
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result


@router.get("/expense", response_model=list)
async def get_all_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category: Optional[str] = None,
    service: AccountSectionService = Depends(get_service)
):
    if category:
        return await service.get_expenses_by_category(category)
    return await service.get_all_expenses(skip, limit)


@router.put("/expense/{expense_id}", response_model=dict)
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    service: AccountSectionService = Depends(get_service)
):
    result = await service.update_expense(expense_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result


@router.delete("/expense/{expense_id}")
async def delete_expense(
    expense_id: int,
    service: AccountSectionService = Depends(get_service)
):
    if not await service.delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


# Financial summary
@router.get("/summary", response_model=dict)
async def get_financial_summary(
    service: AccountSectionService = Depends(get_service)
):
    return await service.get_financial_summary()


__all__ = ["router"]
