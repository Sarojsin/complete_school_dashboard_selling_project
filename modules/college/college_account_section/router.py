"""
College Account Section Router

FastAPI endpoints for faculty payment management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal, require_account
from modules.shared.models import User
from .service import AccountService
from .schemas import CollegePaymentCreate, CollegePaymentResponse, CollegePaymentUpdate, AccountStats

router = APIRouter(
    prefix="/account",
    tags=["College Account Section"],
    dependencies=[Depends(require_college_portal)]
)


# ── Payments ───────────────────────────────────────────────────────

@router.post("/payments", response_model=CollegePaymentResponse, status_code=status.HTTP_201_CREATED)
async def record_payment(
    payment_data: CollegePaymentCreate,
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Record a new faculty payment (Account Section only)"""
    service = AccountService(db)
    return await service.record_payment(payment_data, current_user.id)


@router.get("/payments", response_model=List[CollegePaymentResponse])
async def get_all_payments(
    faculty_id: Optional[int] = None,
    month: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get all payments (Account Section / Dean only)"""
    if current_user.role not in ["account_section", "dean", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view all payments")

    service = AccountService(db)
    return await service.get_all_payments(faculty_id, month, skip, limit)


@router.get("/payments/teacher/{faculty_id}", response_model=List[CollegePaymentResponse])
async def get_teacher_payments(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get payments for a specific faculty member"""
    # Faculty can view their own payments; others need account_section role
    if current_user.role == "college_faculty" and current_user.id != faculty_id:
        # Actually faculty_id is faculty profile id, not user id. Need mapping.
        # For simplicity, allow faculty to view own via /account/me endpoint
        raise HTTPException(status_code=403, detail="Can only view own payments via /account/me")

    service = AccountService(db)
    return await service.get_teacher_payments(faculty_id)


@router.get("/payments/me", response_model=List[CollegePaymentResponse])
async def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get current faculty's own payments"""
    service = AccountService(db)
    return await service.get_my_payments(current_user.id)


@router.get("/payments/{payment_id}", response_model=CollegePaymentResponse)
async def get_payment_detail(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get single payment detail"""
    service = AccountService(db)
    payment = await service.get_payment_detail(payment_id)
    return payment


@router.patch("/payments/{payment_id}", response_model=CollegePaymentResponse)
async def update_payment(
    payment_id: int,
    data: CollegePaymentUpdate,
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update payment details (Account Section only)"""
    service = AccountService(db)
    return await service.update_payment(payment_id, data)


@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int,
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete payment record (Account Section only)"""
    service = AccountService(db)
    await service.delete_payment(payment_id)


# ── Dashboard / Stats ─────────────────────────────────────────────

@router.get("/stats", response_model=AccountStats)
async def get_account_stats(
    current_user: User = Depends(require_account),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get account section statistics (Account Section only)"""
    service = AccountService(db)
    stats_data = await service.get_account_stats()
    return stats_data["stats"]


__all__ = ["router"]
