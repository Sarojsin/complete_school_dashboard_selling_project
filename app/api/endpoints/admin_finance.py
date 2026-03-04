"""
Admin Finance & Fee Management API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API endpoints for managing fees, payments, invoices, and financial reports.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminFinanceService`.
- No direct database manipulations in the routing layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin
from app.services.admin_finance_service import (
    AdminFinanceService, FeeStructureCreateDto, FeeStructureUpdateDto
)


# Create router
router = APIRouter(prefix="/admin/finance", tags=["Admin Finance"])


# ============ FEE STRUCTURE MANAGEMENT ============

@router.get("/structures")
async def get_fee_structures(
    grade_level: Optional[str] = None,
    academic_year: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all fee structures"""
    return await AdminFinanceService.get_fee_structures(db, grade_level, academic_year, status)


@router.post("/structures")
async def create_fee_structure(
    structure_data: FeeStructureCreateDto,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new fee structure"""
    return await AdminFinanceService.create_fee_structure(db, structure_data)


@router.patch("/structures/{structure_id}")
async def update_fee_structure(
    structure_id: int,
    structure_data: FeeStructureUpdateDto,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Update a fee structure"""
    return await AdminFinanceService.update_fee_structure(db, structure_id, structure_data)


# ============ FEE RECORDS MANAGEMENT ============

@router.get("/records")
async def get_fee_records(
    status: Optional[str] = None,
    grade_level: Optional[str] = None,
    student_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all fee records with filtering"""
    return await AdminFinanceService.get_fee_records(db, status, grade_level, student_id, skip, limit)


@router.post("/records/pay")
async def record_payment(
    record_id: int,
    amount: float,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Record a payment for a fee record"""
    return await AdminFinanceService.record_payment(db, record_id, amount)


@router.post("/records/refund")
async def refund_payment(
    record_id: int,
    amount: float,
    reason: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Process a refund"""
    return await AdminFinanceService.refund_payment(db, record_id, amount, reason)


# ============ LATE FEE PENALTY ============

@router.post("/penalty/apply")
async def apply_late_penalty(
    grace_days: int = 7,
    penalty_percentage: float = 5.0,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Apply late fee penalty to overdue records"""
    return await AdminFinanceService.apply_late_penalty(db, grace_days, penalty_percentage)


# ============ FINANCIAL REPORTS ============

@router.get("/reports/summary")
async def get_financial_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get financial summary report"""
    return await AdminFinanceService.get_financial_summary(db, start_date, end_date)


@router.get("/reports/export")
async def export_financial_report(
    format: str = "csv",  # csv, json
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Export financial report"""
    return await AdminFinanceService.export_financial_report(db, format, start_date, end_date)


# ============ INVOICE GENERATION ============

@router.get("/invoice/{record_id}")
async def generate_invoice(
    record_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate invoice for a fee record"""
    return await AdminFinanceService.generate_invoice(db, record_id)


# ============ STATISTICS ============

@router.get("/stats")
async def get_finance_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get finance statistics"""
    return await AdminFinanceService.get_finance_stats(db)
