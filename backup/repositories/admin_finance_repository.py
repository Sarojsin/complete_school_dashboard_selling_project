from typing import List, Dict, Optional, Tuple, Any
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from backup.models.models import FeeStructure, FeeRecord, Student

class AdminFinanceRepository:
    """Handles database queries for the Admin Finance endpoints."""

    @staticmethod
    async def get_fee_structures(
        db: AsyncSession,
        grade_level: Optional[str] = None,
        academic_year: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[FeeStructure]:
        query = select(FeeStructure)
        if grade_level:
            query = query.where(FeeStructure.grade_level == grade_level)
        if academic_year:
            query = query.where(FeeStructure.academic_year == academic_year)
        if status:
            query = query.where(FeeStructure.status == status)
            
        result = await db.execute(query.order_by(FeeStructure.grade_level))
        return list(result.scalars().all())

    @staticmethod
    async def get_fee_structure_by_id(db: AsyncSession, structure_id: int) -> Optional[FeeStructure]:
        result = await db.execute(select(FeeStructure).where(FeeStructure.id == structure_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_fee_structure_by_grade_year(db: AsyncSession, grade: str, year: str) -> Optional[FeeStructure]:
        result = await db.execute(
            select(FeeStructure).where(
                FeeStructure.grade_level == grade,
                FeeStructure.academic_year == year
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_fee_records(
        db: AsyncSession,
        status: Optional[str] = None,
        grade_level: Optional[str] = None,
        student_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[FeeRecord]:
        query = select(FeeRecord).options(selectinload(FeeRecord.student).selectinload(Student.user))
        if status:
            query = query.where(FeeRecord.status == status)
        if grade_level:
            query = query.where(FeeRecord.student.has(Student.grade_level == grade_level))
        if student_id:
            query = query.where(FeeRecord.student_id == student_id)
            
        query = query.offset(skip).limit(limit).order_by(FeeRecord.due_date.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_fee_record_by_id(db: AsyncSession, record_id: int) -> Optional[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).options(selectinload(FeeRecord.student).selectinload(Student.user))
            .where(FeeRecord.id == record_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_overdue_records(db: AsyncSession, cutoff_date: date) -> List[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).where(
                FeeRecord.status == "pending",
                FeeRecord.due_date < cutoff_date
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_report_records(db: AsyncSession, start_date: date, end_date: date) -> List[FeeRecord]:
        result = await db.execute(
            select(FeeRecord).options(selectinload(FeeRecord.student).selectinload(Student.user))
            .where(
                FeeRecord.payment_date >= start_date,
                FeeRecord.payment_date <= end_date
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_finance_stats_raw(db: AsyncSession) -> Dict[str, Any]:
        revenue_r = await db.execute(select(func.sum(FeeRecord.paid_amount)).where(FeeRecord.status == "paid"))
        pending_r = await db.execute(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        )
        structures_r = await db.execute(select(func.count(FeeStructure.id)))
        overdue_r = await db.execute(select(func.count(FeeRecord.id)).where(FeeRecord.status == "overdue"))
        
        return {
            "total_revenue": revenue_r.scalar() or 0.0,
            "pending_fees": pending_r.scalar() or 0.0,
            "total_structures": structures_r.scalar() or 0,
            "overdue_count": overdue_r.scalar() or 0
        }

    @staticmethod
    async def get_report_summary_raw(db: AsyncSession, start: date, end: date) -> Dict[str, Any]:
        collected_r = await db.execute(
            select(func.sum(FeeRecord.paid_amount)).where(
                FeeRecord.status == "paid",
                FeeRecord.payment_date >= start,
                FeeRecord.payment_date <= end
            )
        )
        pending_r = await db.execute(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        )
        
        status_counts = {}
        for st in ["paid", "pending", "overdue", "partial"]:
            count_r = await db.execute(select(func.count(FeeRecord.id)).where(FeeRecord.status == st))
            status_counts[st] = count_r.scalar() or 0
            
        fee_types = {}
        result = await db.execute(select(FeeRecord.fee_type, func.sum(FeeRecord.amount)).group_by(FeeRecord.fee_type))
        for row in result:
            fee_types[row[0]] = float(row[1] or 0)
            
        return {
            "total_collected": collected_r.scalar() or 0.0,
            "total_pending": pending_r.scalar() or 0.0,
            "status_counts": status_counts,
            "fee_types": fee_types
        }
