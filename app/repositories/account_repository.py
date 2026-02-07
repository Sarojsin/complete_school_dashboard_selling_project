from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from typing import List, Optional
from app.models.models import Teacher, User
from app.models.account_models import TeacherPayment
from app.schemas.account_schemas import TeacherPaymentCreate
from datetime import datetime

class AccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_payment(self, payment_data: TeacherPaymentCreate, user_id: int) -> TeacherPayment:
        db_payment = TeacherPayment(
            **payment_data.dict(),
            paid_by=user_id,
            paid_at=datetime.utcnow()
        )
        
        self.session.add(db_payment)
        await self.session.commit()
        await self.session.refresh(db_payment)
        return db_payment
    
    async def get_teacher_payments(self, teacher_id: int) -> List[TeacherPayment]:
        result = await self.session.execute(
            select(TeacherPayment)
            .where(TeacherPayment.teacher_id == teacher_id)
            .order_by(TeacherPayment.month.desc())
        )
        return result.scalars().all()
    
    async def get_all_payments(self) -> List[TeacherPayment]:
        result = await self.session.execute(
            select(TeacherPayment)
            .join(Teacher, TeacherPayment.teacher_id == Teacher.id)
            .join(User, TeacherPayment.paid_by == User.id)
            .order_by(TeacherPayment.paid_at.desc())
        )
        return result.scalars().all()
    
    async def get_payment_stats(self) -> dict:
        # Total payments
        total_result = await self.session.execute(
            select(func.sum(TeacherPayment.amount))
        )
        total_payments = total_result.scalar() or 0
        
        # This month payments
        current_month = datetime.utcnow().strftime("%Y-%m")
        month_result = await self.session.execute(
            select(func.sum(TeacherPayment.amount))
            .where(TeacherPayment.month == current_month)
        )
        month_payments = month_result.scalar() or 0
        
        return {
            "total_teacher_payments": total_payments,
            "payments_this_month": month_payments,
            "pending_payments": 0  # Could be calculated based on salary expectations
        }
