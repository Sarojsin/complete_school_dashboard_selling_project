from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, func, desc
from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict
from datetime import date, datetime
from models.models import FeeRecord, Student, User

class FeeRepository:
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).options(
                joinedload(FeeRecord.student).joinedload(Student.user)
            ).join(Student).filter(
                or_(
                    Student.full_name.ilike(f"%{query}%"),
                    Student.student_id.ilike(f"%{query}%"),
                    Student.parent_name.ilike(f"%{query}%")
                )
            )
        )
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, fee_id: int) -> Optional[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).options(
                joinedload(FeeRecord.student).joinedload(Student.user)
            ).filter(FeeRecord.id == fee_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, fee_data: dict) -> FeeRecord:
        fee = FeeRecord(**fee_data)
        db.add(fee)
        await db.commit()
        await db.refresh(fee)
        return fee
    
    @staticmethod
    async def create_bulk(db: AsyncSession, fees_list: List[dict]) -> List[FeeRecord]:
        """Create multiple fee records at once"""
        fees = [FeeRecord(**data) for data in fees_list]
        db.add_all(fees)
        await db.commit()
        for fee in fees:
            await db.refresh(fee)
        return fees
    
    @staticmethod
    async def update(db: AsyncSession, fee: FeeRecord, **kwargs) -> FeeRecord:
        for key, value in kwargs.items():
            if value is not None and hasattr(fee, key):
                setattr(fee, key, value)
        
        # Update status based on payment
        if 'paid_amount' in kwargs:
            if fee.paid_amount >= fee.amount:
                fee.status = 'paid'
            elif fee.paid_amount > 0:
                fee.status = 'partial'
            else:
                fee.status = 'pending'
        
        # Check if overdue
        if fee.status != 'paid' and fee.due_date < date.today():
            fee.status = 'overdue'
        
        await db.commit()
        await db.refresh(fee)
        return fee
    
    @staticmethod
    async def delete(db: AsyncSession, fee: FeeRecord):
        await db.delete(fee)
        await db.commit()
    
    @staticmethod
    async def get_student_fees(db: AsyncSession, student_id: int, 
                        status: str = None) -> List[FeeRecord]:
        query = select(FeeRecord).filter(FeeRecord.student_id == student_id)
        
        if status:
            query = query.filter(FeeRecord.status == status)
        
        result = await db.execute(query.order_by(desc(FeeRecord.due_date)))
        return result.scalars().all()
    
    @staticmethod
    async def get_pending_fees(db: AsyncSession, student_id: int) -> List[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).filter(
                FeeRecord.student_id == student_id,
                FeeRecord.status.in_(['pending', 'partial', 'overdue'])
            ).order_by(FeeRecord.due_date)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_overdue_fees(db: AsyncSession, student_id: int = None) -> List[FeeRecord]:
        query = select(FeeRecord).filter(
            FeeRecord.due_date < date.today(),
            FeeRecord.status.in_(['pending', 'partial', 'overdue'])
        )
        
        if student_id:
            query = query.filter(FeeRecord.student_id == student_id)
        
        result = await db.execute(query.order_by(FeeRecord.due_date))
        return result.scalars().all()
    
    @staticmethod
    async def get_fee_summary(db: AsyncSession, student_id: int) -> Dict:
        """Get fee summary for a student"""
        result = await db.execute(select(FeeRecord).filter(FeeRecord.student_id == student_id))
        fees = result.scalars().all()
        
        total_amount = sum(f.amount for f in fees)
        total_paid = sum(f.paid_amount for f in fees)
        total_pending = total_amount - total_paid
        
        pending_count = sum(1 for f in fees if f.status in ['pending', 'partial'])
        overdue_count = sum(1 for f in fees if f.status == 'overdue')
        
        return {
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'pending_count': pending_count,
            'overdue_count': overdue_count
        }
    
    @staticmethod
    async def get_all_fees_summary(db: AsyncSession) -> Dict:
        """Get summary of all fees in the system"""
        res = await db.execute(
            select(
                func.sum(FeeRecord.amount).label('total_amount'),
                func.sum(FeeRecord.paid_amount).label('total_paid'),
                func.count(FeeRecord.id).label('total_records')
            )
        )
        result = res.first()
        
        pen_res = await db.execute(
            select(func.count(FeeRecord.id)).filter(
                FeeRecord.status.in_(['pending', 'partial', 'overdue'])
            )
        )
        pending = pen_res.scalar()
        
        return {
            'total_amount': result.total_amount or 0,
            'total_paid': result.total_paid or 0,
            'total_pending': (result.total_amount or 0) - (result.total_paid or 0),
            'total_records': result.total_records or 0,
            'pending_records': pending or 0
        }
    
    @staticmethod
    async def record_payment(db: AsyncSession, fee_id: int, amount: float, 
                      payment_date: date = None) -> FeeRecord:
        """Record a payment for a fee"""
        fee = await FeeRepository.get_by_id(db, fee_id)
        if not fee:
            return None
        
        new_paid = fee.paid_amount + amount
        
        return await FeeRepository.update(
            db, fee,
            paid_amount=new_paid,
            payment_date=payment_date or date.today()
        )
    
    @staticmethod
    async def get_payment_history(db: AsyncSession, student_id: int) -> List[FeeRecord]:
        """Get all paid fees for a student"""
        result = await db.execute(
            select(FeeRecord).filter(
                FeeRecord.student_id == student_id,
                FeeRecord.paid_amount > 0
            ).order_by(desc(FeeRecord.payment_date))
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_fees_by_type(db: AsyncSession, fee_type: str) -> List[FeeRecord]:
        """Get all fees of a specific type"""
        result = await db.execute(
            select(FeeRecord).filter(
                FeeRecord.fee_type == fee_type
            ).order_by(desc(FeeRecord.due_date))
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_overdue_status(db: AsyncSession):
        """Update status of overdue fees (run as scheduled task)"""
        await db.execute(
            update(FeeRecord).filter(
                FeeRecord.due_date < date.today(),
                FeeRecord.status.in_(['pending', 'partial'])
            ).values(status='overdue')
        )
        await db.commit()