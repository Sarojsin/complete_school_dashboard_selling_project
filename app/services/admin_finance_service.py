from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from pydantic import BaseModel

from app.models.models import FeeStructure, FeeRecord
from app.repositories.admin_finance_repository import AdminFinanceRepository
from app.core.exceptions import NotFoundError, ValidationError


class FeeStructureCreateDto(BaseModel):
    grade_level: str
    academic_year: str
    tuition_fee: float = 0.0
    registration_fee: float = 0.0
    library_fee: float = 0.0
    sports_fee: float = 0.0
    lab_fee: float = 0.0
    activity_fee: float = 0.0
    other_charges: float = 0.0
    due_date: date

class FeeStructureUpdateDto(BaseModel):
    tuition_fee: Optional[float] = None
    registration_fee: Optional[float] = None
    library_fee: Optional[float] = None
    sports_fee: Optional[float] = None
    lab_fee: Optional[float] = None
    activity_fee: Optional[float] = None
    other_charges: Optional[float] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class AdminFinanceService:
    """Business logic for Admin Finance operations."""

    @staticmethod
    async def get_fee_structures(
        db: AsyncSession, grade_level: Optional[str], academic_year: Optional[str], status: Optional[str]
    ) -> List[Dict[str, Any]]:
        structures = await AdminFinanceRepository.get_fee_structures(db, grade_level, academic_year, status)
        return [{
            "id": s.id,
            "grade_level": s.grade_level,
            "academic_year": s.academic_year,
            "tuition_fee": s.tuition_fee,
            "registration_fee": s.registration_fee,
            "library_fee": s.library_fee,
            "sports_fee": s.sports_fee,
            "lab_fee": s.lab_fee,
            "activity_fee": s.activity_fee,
            "other_charges": s.other_charges,
            "total_amount": s.total_amount,
            "due_date": s.due_date.isoformat() if s.due_date else None,
            "status": s.status
        } for s in structures]

    @staticmethod
    async def create_fee_structure(db: AsyncSession, data: FeeStructureCreateDto) -> Dict[str, Any]:
        existing = await AdminFinanceRepository.get_fee_structure_by_grade_year(db, data.grade_level, data.academic_year)
        if existing:
            raise ValidationError("Fee structure already exists for this grade and year")
            
        total = (data.tuition_fee + data.registration_fee + data.library_fee + 
                 data.sports_fee + data.lab_fee + data.activity_fee + data.other_charges)
                 
        structure = FeeStructure(
            grade_level=data.grade_level, academic_year=data.academic_year,
            tuition_fee=data.tuition_fee, registration_fee=data.registration_fee,
            library_fee=data.library_fee, sports_fee=data.sports_fee,
            lab_fee=data.lab_fee, activity_fee=data.activity_fee,
            other_charges=data.other_charges, total_amount=total, due_date=data.due_date
        )
        db.add(structure)
        await db.commit()
        await db.refresh(structure)
        return {"success": True, "structure": {"id": structure.id, "total": structure.total_amount}}

    @staticmethod
    async def update_fee_structure(db: AsyncSession, structure_id: int, data: FeeStructureUpdateDto) -> Dict[str, Any]:
        st = await AdminFinanceRepository.get_fee_structure_by_id(db, structure_id)
        if not st:
            raise NotFoundError("Fee structure not found")
            
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(st, field, value)
            
        st.total_amount = (st.tuition_fee + st.registration_fee + st.library_fee + 
                           st.sports_fee + st.lab_fee + st.activity_fee + st.other_charges)
                           
        await db.commit()
        return {"success": True, "message": "Fee structure updated"}

    @staticmethod
    async def get_fee_records(
        db: AsyncSession, status: Optional[str], grade_level: Optional[str], 
        student_id: Optional[int], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        records = await AdminFinanceRepository.get_fee_records(db, status, grade_level, student_id, skip, limit)
        return [{
            "id": r.id,
            "student_id": r.student_id,
            "student_name": r.student.user.full_name if getattr(r.student, 'user', None) else "N/A",
            "grade_level": getattr(r.student, 'grade_level', "N/A"),
            "fee_type": r.fee_type,
            "amount": r.amount,
            "paid_amount": r.paid_amount,
            "due_date": r.due_date.isoformat() if r.due_date else None,
            "payment_date": r.payment_date.isoformat() if r.payment_date else None,
            "status": r.status,
            "remarks": r.remarks
        } for r in records]

    @staticmethod
    async def record_payment(db: AsyncSession, record_id: int, amount: float) -> Dict[str, Any]:
        record = await AdminFinanceRepository.get_fee_record_by_id(db, record_id)
        if not record:
            raise NotFoundError("Fee record not found")
            
        record.paid_amount += amount
        record.payment_date = date.today()
        record.status = "paid" if record.paid_amount >= record.amount else "partial"
        
        await db.commit()
        return {"success": True, "message": "Payment recorded", "paid_amount": record.paid_amount, "status": record.status}

    @staticmethod
    async def refund_payment(db: AsyncSession, record_id: int, amount: float, reason: str) -> Dict[str, Any]:
        record = await AdminFinanceRepository.get_fee_record_by_id(db, record_id)
        if not record:
            raise NotFoundError("Fee record not found")
        if record.status != "paid":
            raise ValidationError("Can only refund paid records")
            
        refund_amount = min(amount, record.paid_amount)
        record.paid_amount -= refund_amount
        record.status = "refunded" if record.paid_amount <= 0 else "partial"
        record.remarks = f"Refund: {reason}"
        
        await db.commit()
        return {"success": True, "message": f"Refund of ${refund_amount} processed"}

    @staticmethod
    async def apply_late_penalty(db: AsyncSession, grace_days: int, penalty_percentage: float) -> Dict[str, Any]:
        cutoff_date = date.today() - timedelta(days=grace_days)
        records = await AdminFinanceRepository.get_overdue_records(db, cutoff_date)
        
        updated_count = 0
        for record in records:
            penalty = record.amount * (penalty_percentage / 100)
            record.amount += penalty
            record.status = "overdue"
            record.remarks = f"Late penalty applied: {penalty_percentage}%"
            updated_count += 1
            
        await db.commit()
        return {"success": True, "message": f"Late penalty applied to {updated_count} records", "records_updated": updated_count}

    @staticmethod
    async def get_financial_summary(db: AsyncSession, start_date: Optional[date], end_date: Optional[date]) -> Dict[str, Any]:
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
            
        stats = await AdminFinanceRepository.get_report_summary_raw(db, start_date, end_date)
        total_collected = stats["total_collected"]
        total_pending = stats["total_pending"]
        col_rate = round((total_collected / (total_collected + total_pending) * 100), 2) if (total_collected + total_pending) > 0 else 0
        
        return {
            "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "summary": {"total_collected": total_collected, "total_pending": total_pending, "collection_rate": col_rate},
            "by_status": stats["status_counts"],
            "by_fee_type": stats["fee_types"]
        }

    @staticmethod
    async def export_financial_report(
        db: AsyncSession, format: str, start_date: Optional[date], end_date: Optional[date]
    ) -> Dict[str, Any]:
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
            
        records = await AdminFinanceRepository.get_report_records(db, start_date, end_date)
        
        if format == "csv":
            csv_lines = ["ID,Student,Fee Type,Amount,Paid,Status,Due Date,Payment Date"]
            for r in records:
                std_name = r.student.user.full_name if getattr(r.student, 'user', None) else 'N/A'
                csv_lines.append(f"{r.id},{std_name},{r.fee_type},{r.amount},{r.paid_amount},{r.status},{r.due_date},{r.payment_date or ''}")
            return {"format": "csv", "data": "\n".join(csv_lines)}
            
        return {
            "format": "json",
            "records": [{
                "id": r.id,
                "student": r.student.user.full_name if getattr(r.student, 'user', None) else "N/A",
                "fee_type": r.fee_type,
                "amount": r.amount,
                "paid_amount": r.paid_amount,
                "status": r.status,
                "due_date": r.due_date.isoformat() if r.due_date else None,
                "payment_date": r.payment_date.isoformat() if r.payment_date else None
            } for r in records]
        }

    @staticmethod
    async def generate_invoice(db: AsyncSession, record_id: int) -> Dict[str, Any]:
        record = await AdminFinanceRepository.get_fee_record_by_id(db, record_id)
        if not record:
            raise NotFoundError("Fee record not found")
            
        return {
            "invoice": {
                "invoice_number": f"INV-{record.id}-{date.today().year}",
                "date_issued": date.today().isoformat(),
                "due_date": record.due_date.isoformat() if record.due_date else None,
                "student": {
                    "id": record.student.id,
                    "name": record.student.user.full_name if getattr(record.student, 'user', None) else "N/A",
                    "grade": getattr(record.student, 'grade_level', "N/A")
                },
                "fee_type": record.fee_type,
                "amount": record.amount,
                "paid_amount": record.paid_amount,
                "balance_due": record.amount - record.paid_amount,
                "status": record.status
            }
        }

    @staticmethod
    async def get_finance_stats(db: AsyncSession) -> Dict[str, Any]:
        stats = await AdminFinanceRepository.get_finance_stats_raw(db)
        tr = stats["total_revenue"]
        pf = stats["pending_fees"]
        rate = round((tr / (tr + pf) * 100), 2) if (tr + pf) > 0 else 0
        
        return {
            "total_revenue": round(tr, 2),
            "pending_fees": round(pf, 2),
            "total_fee_structures": stats["total_structures"],
            "overdue_records": stats["overdue_count"],
            "collection_rate": rate
        }
