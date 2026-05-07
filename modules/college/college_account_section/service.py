"""
College Account Section Service

Business logic for faculty payment management.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .repository import AccountRepository
from .schemas import CollegePaymentCreate, CollegePaymentUpdate, CollegePaymentResponse, AccountStats
from modules.shared.exceptions import NotFoundError, ForbiddenError, ValidationError


class AccountService:
    """Service for account section operations"""

    def __init__(self, db: AsyncSession):
        self.repository = AccountRepository(db)

    # ── Payments ────────────────────────────────────────────────────

    async def record_payment(self, data: CollegePaymentCreate, recorded_by: int) -> Dict[str, Any]:
        """Record a new faculty payment"""
        try:
            payment = await self.repository.create_payment(data, recorded_by)
            return {"payment": CollegePaymentResponse.model_validate(payment)}
        except ValueError as e:
            raise ValidationError(str(e))

    async def get_all_payments(
        self,
        faculty_id: Optional[int] = None,
        month: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegePaymentResponse]:
        """Get all payments (Account Section or Dean only)"""
        payments = await self.repository.get_all_payments(faculty_id, month, skip, limit)
        return [CollegePaymentResponse.model_validate(p) for p in payments]

    async def get_teacher_payments(self, faculty_id: int) -> List[CollegePaymentResponse]:
        """Get payments for a specific faculty member"""
        payments = await self.repository.get_faculty_payments(faculty_id)
        # Convert to response schema
        return [CollegePaymentResponse.model_validate(p) for p in payments]

    async def get_my_payments(self, user_id: int) -> List[CollegePaymentResponse]:
        """Get current faculty's own payments"""
        from backup.models.college.faculty import Faculty
        # Get faculty profile for user
        result = await self.repository.db.execute(
            select(Faculty).where(Faculty.user_id == user_id)
        )
        faculty = result.scalar_one_or_none()
        if not faculty:
            raise NotFoundError("Faculty profile not found for current user")
        payments = await self.repository.get_faculty_payments(faculty.id)
        return [CollegePaymentResponse.model_validate(p) for p in payments]

    async def get_payment_detail(self, payment_id: int) -> Dict[str, Any]:
        """Get single payment detail"""
        payment = await self.repository.get_payment(payment_id)
        if not payment:
            raise NotFoundError("Payment record not found")
        return {"payment": CollegePaymentResponse.model_validate(payment)}

    async def update_payment(self, payment_id: int, data: CollegePaymentUpdate) -> Dict[str, Any]:
        """Update payment (e.g., add transaction reference, correct remarks)"""
        payment = await self.repository.update_payment(payment_id, data)
        if not payment:
            raise NotFoundError("Payment record not found")
        return {"payment": CollegePaymentResponse.model_validate(payment)}

    async def delete_payment(self, payment_id: int) -> Dict[str, str]:
        """Delete payment record (Account Section only)"""
        success = await self.repository.delete_payment(payment_id)
        if not success:
            raise NotFoundError("Payment record not found")
        return {"message": "Payment record deleted successfully"}

    async def get_account_stats(self) -> Dict[str, Any]:
        """Get account section dashboard statistics"""
        stats = await self.repository.get_stats()
        return {"stats": AccountStats(**stats)}


__all__ = ["AccountService"]
