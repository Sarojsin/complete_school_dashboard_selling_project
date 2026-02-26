from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.models import Teacher, User, Student, FeeRecord
from app.models.account_models import TeacherPayment
from app.schemas.account_schemas import TeacherPaymentCreate, FeePaymentCreate
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
            .options(
                joinedload(TeacherPayment.teacher),
                joinedload(TeacherPayment.payer)
            )
            .where(TeacherPayment.teacher_id == teacher_id)
            .order_by(TeacherPayment.month.desc())
        )
        return result.scalars().all()
    
    async def get_all_payments(self) -> List[TeacherPayment]:
        result = await self.session.execute(
            select(TeacherPayment)
            .options(
                joinedload(TeacherPayment.teacher),
                joinedload(TeacherPayment.payer)
            )
            .order_by(TeacherPayment.paid_at.desc())
        )
        return result.scalars().all()
    
    async def get_all_teachers_with_names(self) -> List[Teacher]:
        """Get all teachers with names for dropdown"""
        result = await self.session.execute(
            select(Teacher).order_by(Teacher.full_name)
        )
        return result.scalars().all()
    
    async def get_all_students_with_names(self) -> List[Student]:
        """Get all students with names for dropdown"""
        result = await self.session.execute(
            select(Student).order_by(Student.full_name)
        )
        return result.scalars().all()
    
    async def get_all_fee_payments(self) -> List[FeeRecord]:
        """Get all fee payment records with student info"""
        result = await self.session.execute(
            select(FeeRecord)
            .join(Student, FeeRecord.student_id == Student.id)
            .order_by(FeeRecord.payment_date.desc())
        )
        return result.scalars().all()
    
    async def record_fee_payment(self, fee_data: FeePaymentCreate, user_id: int) -> FeeRecord:
        """Record a new fee payment"""
        db_fee = FeeRecord(
            student_id=fee_data.student_id,
            fee_type=fee_data.fee_type,
            amount=fee_data.amount,
            paid_amount=fee_data.amount,
            payment_date=datetime.utcnow().date(),
            status="paid",
            remarks=fee_data.remarks
        )
        
        self.session.add(db_fee)
        await self.session.commit()
        await self.session.refresh(db_fee)
        return db_fee
    
    async def get_pending_fees(self) -> List[FeeRecord]:
        """Get all pending/overdue fee records"""
        result = await self.session.execute(
            select(FeeRecord)
            .where(FeeRecord.status.in_(["pending", "overdue"]))
            .order_by(FeeRecord.due_date)
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
    
    async def get_account_dashboard_stats(self) -> dict:
        """Get dashboard statistics for account section"""
        current_month = datetime.utcnow().strftime("%Y-%m")
        
        # Fees collected this month
        fees_result = await self.session.execute(
            select(func.sum(FeeRecord.paid_amount))
            .where(
                and_(
                    FeeRecord.status == "paid",
                    extract('year', FeeRecord.payment_date) == datetime.utcnow().year,
                    extract('month', FeeRecord.payment_date) == datetime.utcnow().month
                )
            )
        )
        fees_collected = fees_result.scalar() or 0
        
        # Teacher payments this month
        payments_result = await self.session.execute(
            select(func.sum(TeacherPayment.amount))
            .where(TeacherPayment.month == current_month)
        )
        teacher_payments = payments_result.scalar() or 0
        
        # Pending fees
        pending_result = await self.session.execute(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount))
            .where(FeeRecord.status.in_(["pending", "overdue"]))
        )
        pending_fees = pending_result.scalar() or 0
        
        # Total fee records
        fee_count_result = await self.session.execute(
            select(func.count(FeeRecord.id))
        )
        total_fee_records = fee_count_result.scalar() or 0
        
        # Total teacher payments
        payment_count_result = await self.session.execute(
            select(func.count(TeacherPayment.id))
        )
        total_teacher_payments_count = payment_count_result.scalar() or 0
        
        # Total teacher payments amount
        payment_sum_result = await self.session.execute(
            select(func.sum(TeacherPayment.amount))
        )
        total_payments_amount = payment_sum_result.scalar() or 0
        
        return {
            "fees_collected_month": fees_collected,
            "teacher_payments_month": teacher_payments,
            "payments_this_month": teacher_payments,
            "pending_fees": pending_fees,
            "pending_payments": pending_fees,
            "total_fee_records": total_fee_records,
            "total_teacher_payments": total_payments_amount,
            "total_teacher_payments_count": total_teacher_payments_count
        }
    
    async def get_monthly_report(self, year: int, month: int) -> dict:
        """Get monthly financial report"""
        month_str = f"{year}-{month:02d}"
        
        # Teacher payments for month
        payments_result = await self.session.execute(
            select(func.sum(TeacherPayment.amount))
            .where(TeacherPayment.month == month_str)
        )
        teacher_payments = payments_result.scalar() or 0
        
        # Fee collections for month
        fees_result = await self.session.execute(
            select(func.sum(FeeRecord.paid_amount))
            .where(
                and_(
                    extract('year', FeeRecord.payment_date) == year,
                    extract('month', FeeRecord.payment_date) == month
                )
            )
        )
        fees_collected = fees_result.scalar() or 0
        
        return {
            "month": month_str,
            "teacher_payments": teacher_payments,
            "fees_collected": fees_collected,
            "net_balance": fees_collected - teacher_payments
        }
