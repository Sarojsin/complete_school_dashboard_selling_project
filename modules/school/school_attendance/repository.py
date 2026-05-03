"""
School Attendance Repository

Database CRUD operations for school attendance.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
from datetime import date, datetime

from .models import AttendanceSession, AttendanceRecord


class AttendanceRepository:
    """Repository for attendance operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Attendance Session methods
    async def create_session(self, class_id: int, date: date, 
                           subject_id: Optional[int] = None, 
                           taken_by: Optional[int] = None) -> AttendanceSession:
        """Create a new attendance session"""
        session = AttendanceSession(
            class_id=class_id,
            date=date,
            subject_id=subject_id,
            taken_by=taken_by
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session
    
    async def get_session(self, session_id: int) -> Optional[AttendanceSession]:
        """Get attendance session by ID"""
        result = await self.db.execute(
            select(AttendanceSession).where(AttendanceSession.id == session_id)
        )
        return result.scalar_one_or_none()
    
    async def get_session_by_class_and_date(self, class_id: int, 
                                           session_date: date,
                                           subject_id: Optional[int] = None
                                           ) -> Optional[AttendanceSession]:
        """Get session by class, date and optionally subject"""
        query = select(AttendanceSession).where(
            and_(
                AttendanceSession.class_id == class_id,
                AttendanceSession.date == session_date
            )
        )
        if subject_id:
            query = query.where(AttendanceSession.subject_id == subject_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_sessions(self, class_id: Optional[int] = None,
                           date_from: Optional[date] = None,
                           date_to: Optional[date] = None,
                           skip: int = 0, limit: int = 100) -> List[AttendanceSession]:
        """List attendance sessions with filters"""
        query = select(AttendanceSession)
        
        if class_id:
            query = query.where(AttendanceSession.class_id == class_id)
        if date_from:
            query = query.where(AttendanceSession.date >= date_from)
        if date_to:
            query = query.where(AttendanceSession.date <= date_to)
        
        query = query.order_by(AttendanceSession.date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    # Attendance Record methods
    async def create_record(self, session_id: int, student_id: int,
                           status: str, remarks: Optional[str] = None
                           ) -> AttendanceRecord:
        """Create an attendance record"""
        record = AttendanceRecord(
            session_id=session_id,
            student_id=student_id,
            status=status,
            remarks=remarks
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_record(self, record_id: int) -> Optional[AttendanceRecord]:
        """Get attendance record by ID"""
        result = await self.db.execute(
            select(AttendanceRecord).where(AttendanceRecord.id == record_id)
        )
        return result.scalar_one_or_none()
    
    async def get_records_by_session(self, session_id: int) -> List[AttendanceRecord]:
        """Get all records for a session"""
        result = await self.db.execute(
            select(AttendanceRecord).where(AttendanceRecord.session_id == session_id)
        )
        return list(result.scalars().all())
    
    async def get_record_by_student_and_session(self, student_id: int,
                                               session_id: int
                                               ) -> Optional[AttendanceRecord]:
        """Get record for specific student in a session"""
        result = await self.db.execute(
            select(AttendanceRecord).where(
                and_(
                    AttendanceRecord.student_id == student_id,
                    AttendanceRecord.session_id == session_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def update_record(self, record_id: int, status: Optional[str] = None,
                           remarks: Optional[str] = None) -> Optional[AttendanceRecord]:
        """Update an attendance record"""
        record = await self.get_record(record_id)
        if record:
            if status:
                record.status = str(status)
            if remarks is not None:
                record.remarks = str(remarks)
            await self.db.commit()
            await self.db.refresh(record)
        return record
    
    # Summary methods
    async def get_student_attendance_summary(self, student_id: int,
                                            date_from: Optional[date] = None,
                                            date_to: Optional[date] = None
                                            ) -> dict:
        """Get attendance summary for a student"""
        query = select(
            AttendanceRecord.status,
            func.count(AttendanceRecord.id).label('count')
        ).where(AttendanceRecord.student_id == student_id)
        
        if date_from:
            query = query.join(AttendanceSession).where(
                AttendanceSession.date >= date_from
            )
        if date_to:
            query = query.join(AttendanceSession).where(
                AttendanceSession.date <= date_to
            )
        
        query = query.group_by(AttendanceRecord.status)
        result = await self.db.execute(query)
        
        summary: dict = {"present": 0, "absent": 0, "late": 0, "excused": 0, "total": 0, "percentage": 0.0}
        for row in result:
            status = str(row.status)
            count = int(row.count)
            if status in summary:
                summary[status] = count
                summary["total"] += count
        
        if summary["total"] > 0:
            summary["percentage"] = float(round(
                (summary["present"] + summary["late"]) / summary["total"] * 100, 2
            ))
        
        return summary
    
    async def get_class_attendance_summary(self, class_id: int,
                                           session_date: date) -> dict:
        """Get attendance summary for a class on a specific date"""
        # Get session
        session = await self.get_session_by_class_and_date(class_id, session_date)
        if not session:
            return {"total": 0, "present": 0, "absent": 0, "percentage": 0.0}
        
        # Get records
        records = await self.get_records_by_session(int(session.id))
        
        summary: dict = {"total": len(records), "present": 0, "absent": 0, "late": 0, "excused": 0, "percentage": 0.0}
        for record in records:
            status = str(record.status)
            if status in summary:
                summary[status] += 1
        
        if summary["total"] > 0:
            summary["percentage"] = float(round(
                (summary["present"] + summary["late"]) / summary["total"] * 100, 2
            ))
        
        return summary


__all__ = ["AttendanceRepository"]
