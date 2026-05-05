"""
College Account Section Repository

Async CRUD operations for faculty payments.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime
from .models import CollegeFacultyPayment
from .schemas import CollegePaymentCreate, CollegePaymentUpdate


class AccountRepository:
    """Repository for account section operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, data: CollegePaymentCreate, paid_by: int) -> CollegeFacultyPayment:
        """Record a new faculty payment"""
        payment = CollegeFacultyPayment(
            faculty_id=data.faculty_id,
            amount=data.amount,
            month=data.month,
            payment_type=data.payment_type.value,
            payment_method=data.payment_method.value,
            transaction_reference=data.transaction_reference,
            remarks=data.remarks,
            paid_by_user_id=paid_by,
            paid_at=datetime.utcnow()
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int) -> Optional[CollegeFacultyPayment]:
        """Get payment by ID"""
        result = await self.db.execute(
            select(CollegeFacultyPayment).where(CollegeFacultyPayment.id == payment_id)
        )
        return result.scalar_one_or_none()

    async def get_all_payments(
        self,
        faculty_id: Optional[int] = None,
        month: Optional[str] = None,
        payment_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegeFacultyPayment]:
        """Get all payments with filters"""
        query = select(CollegeFacultyPayment)

        if faculty_id is not None:
            query = query.where(CollegeFacultyPayment.faculty_id == faculty_id)
        if month:
            query = query.where(CollegeFacultyPayment.month == month)
        if payment_type:
            query = query.where(CollegeFacultyPayment.payment_type == payment_type)

        query = query.order_by(CollegeFacultyPayment.paid_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_faculty_payments(self, faculty_id: int) -> List[CollegeFacultyPayment]:
        """Get all payments for a specific faculty"""
        result = await self.db.execute(
            select(CollegeFacultyPayment)
            .where(CollegeFacultyPayment.faculty_id == faculty_id)
            .order_by(CollegeFacultyPayment.paid_at.desc())
        )
        return list(result.scalars().all())

    async def get_total_paid(self, faculty_id: int) -> float:
        """Get total amount paid to a faculty member"""
        result = await self.db.execute(
            select(func.sum(CollegeFacultyPayment.amount))
            .where(CollegeFacultyPayment.faculty_id == faculty_id)
        )
        return result.scalar() or 0.0

    async def update_payment(self, payment_id: int, data: CollegePaymentUpdate) -> Optional[CollegeFacultyPayment]:
        """Update payment details (usually only remarks or reference)"""
        payment = await self.get_payment(payment_id)
        if not payment:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)

        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def delete_payment(self, payment_id: int) -> bool:
        """Delete payment record"""
        payment = await self.get_payment(payment_id)
        if payment:
            await self.db.delete(payment)
            await self.db.commit()
            return True
        return False

    async def get_stats(self) -> dict:
        """Get account section statistics"""
        from sqlalchemy import extract

        total = await self.db.execute(select(func.count(CollegeFacultyPayment.id)))
        total_amount = await self.db.execute(select(func.sum(CollegeFacultyPayment.amount)))

        # This month's total
        now = datetime.utcnow()
        current_month_str = now.strftime("%Y-%m")
        month_total = await self.db.execute(
            select(func.sum(CollegeFacultyPayment.amount))
            .where(CollegeFacultyPayment.month == current_month_str)
        )

        # Distinct faculty count
        faculty_count = await self.db.execute(
            select(func.count(CollegeFacultyPayment.faculty_id.distinct()))
        )

        return {
            "total_payments": total.scalar() or 0,
            "total_amount": total_amount.scalar() or 0.0,
            "this_month_total": month_total.scalar() or 0.0,
            "faculty_count": faculty_count.scalar() or 0
        }


__all__ = ["AccountRepository"]
