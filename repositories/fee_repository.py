from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict
from datetime import date, datetime
from models.models import FeeRecord, Student

class FeeRepository:
    @staticmethod
    def search(db: Session, query: str) -> List[FeeRecord]:
        return db.query(FeeRecord).join(Student).filter(
            or_(
                Student.full_name.ilike(f"%{query}%"),
                Student.student_id.ilike(f"%{query}%"),
                Student.parent_name.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def get_by_id(db: Session, fee_id: int) -> Optional[FeeRecord]:
        return db.query(FeeRecord).filter(FeeRecord.id == fee_id).first()
    
    @staticmethod
    def create(db: Session, fee_data: dict) -> FeeRecord:
        fee = FeeRecord(**fee_data)
        db.add(fee)
        db.commit()
        db.refresh(fee)
        return fee
    
    @staticmethod
    def create_bulk(db: Session, fees_list: List[dict]) -> List[FeeRecord]:
        """Create multiple fee records at once"""
        fees = [FeeRecord(**data) for data in fees_list]
        db.add_all(fees)
        db.commit()
        for fee in fees:
            db.refresh(fee)
        return fees
    
    @staticmethod
    def update(db: Session, fee: FeeRecord, **kwargs) -> FeeRecord:
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
        
        db.commit()
        db.refresh(fee)
        return fee
    
    @staticmethod
    def delete(db: Session, fee: FeeRecord):
        db.delete(fee)
        db.commit()
    
    @staticmethod
    def get_student_fees(db: Session, student_id: int, 
                        status: str = None) -> List[FeeRecord]:
        query = db.query(FeeRecord).filter(FeeRecord.student_id == student_id)
        
        if status:
            query = query.filter(FeeRecord.status == status)
        
        return query.order_by(FeeRecord.due_date.desc()).all()
    
    @staticmethod
    def get_pending_fees(db: Session, student_id: int) -> List[FeeRecord]:
        return db.query(FeeRecord).filter(
            FeeRecord.student_id == student_id,
            FeeRecord.status.in_(['pending', 'partial', 'overdue'])
        ).order_by(FeeRecord.due_date).all()
    
    @staticmethod
    def get_overdue_fees(db: Session, student_id: int = None) -> List[FeeRecord]:
        query = db.query(FeeRecord).filter(
            FeeRecord.due_date < date.today(),
            FeeRecord.status.in_(['pending', 'partial', 'overdue'])
        )
        
        if student_id:
            query = query.filter(FeeRecord.student_id == student_id)
        
        return query.order_by(FeeRecord.due_date).all()
    
    @staticmethod
    def get_fee_summary(db: Session, student_id: int) -> Dict:
        """Get fee summary for a student"""
        fees = db.query(FeeRecord).filter(
            FeeRecord.student_id == student_id
        ).all()
        
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
    def get_all_fees_summary(db: Session) -> Dict:
        """Get summary of all fees in the system"""
        result = db.query(
            func.sum(FeeRecord.amount).label('total_amount'),
            func.sum(FeeRecord.paid_amount).label('total_paid'),
            func.count(FeeRecord.id).label('total_records')
        ).first()
        
        pending = db.query(func.count(FeeRecord.id)).filter(
            FeeRecord.status.in_(['pending', 'partial', 'overdue'])
        ).scalar()
        
        return {
            'total_amount': result.total_amount or 0,
            'total_paid': result.total_paid or 0,
            'total_pending': (result.total_amount or 0) - (result.total_paid or 0),
            'total_records': result.total_records or 0,
            'pending_records': pending or 0
        }
    
    @staticmethod
    def record_payment(db: Session, fee_id: int, amount: float, 
                      payment_date: date = None) -> FeeRecord:
        """Record a payment for a fee"""
        fee = FeeRepository.get_by_id(db, fee_id)
        if not fee:
            return None
        
        new_paid = fee.paid_amount + amount
        
        return FeeRepository.update(
            db, fee,
            paid_amount=new_paid,
            payment_date=payment_date or date.today()
        )
    
    @staticmethod
    def get_payment_history(db: Session, student_id: int) -> List[FeeRecord]:
        """Get all paid fees for a student"""
        return db.query(FeeRecord).filter(
            FeeRecord.student_id == student_id,
            FeeRecord.paid_amount > 0
        ).order_by(FeeRecord.payment_date.desc()).all()
    
    @staticmethod
    def get_fees_by_type(db: Session, fee_type: str) -> List[FeeRecord]:
        """Get all fees of a specific type"""
        return db.query(FeeRecord).filter(
            FeeRecord.fee_type == fee_type
        ).order_by(FeeRecord.due_date.desc()).all()
    
    @staticmethod
    def update_overdue_status(db: Session):
        """Update status of overdue fees (run as scheduled task)"""
        db.query(FeeRecord).filter(
            FeeRecord.due_date < date.today(),
            FeeRecord.status.in_(['pending', 'partial'])
        ).update({'status': 'overdue'}, synchronize_session=False)
        
        db.commit()