"""
School Attendance Service

Business logic for school attendance management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from datetime import date, datetime

from .repository import AttendanceRepository
from .schemas import (
    AttendanceSessionCreate,
    AttendanceRecordCreate,
    AttendanceMarkRequest,
    StudentAttendanceSummary,
    ClassAttendanceSummary,
)


class AttendanceService:
    """Service for attendance business logic"""
    
    def __init__(self, db: AsyncSession):
        self.repository = AttendanceRepository(db)
    
    async def create_session(self, session_data: AttendanceSessionCreate, 
                           teacher_id: int) -> Dict[str, Any]:
        """Create a new attendance session"""
        # Check if session already exists
        existing = await self.repository.get_session_by_class_and_date(
            session_data.class_id,
            session_data.date,
            session_data.subject_id
        )
        if existing:
            return {"error": "Session already exists", "session": existing}
        
        session = await self.repository.create_session(
            class_id=session_data.class_id,
            date=session_data.date,
            subject_id=session_data.subject_id,
            taken_by=teacher_id
        )
        return {"session": session}
    
    async def mark_attendance(self, session_id: int, 
                            mark_request: AttendanceMarkRequest) -> Dict[str, Any]:
        """Mark attendance for a student"""
        # Check if session exists
        session = await self.repository.get_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        # Check if already marked
        existing = await self.repository.get_record_by_student_and_session(
            mark_request.student_id,
            session_id
        )
        if existing:
            return {"error": "Attendance already marked for this student"}
        
        # Create record
        record = await self.repository.create_record(
            session_id=session_id,
            student_id=mark_request.student_id,
            status=mark_request.status,
            remarks=mark_request.remarks
        )
        return {"record": record}
    
    async def bulk_mark_attendance(self, session_id: int,
                                  records: List[AttendanceMarkRequest]
                                  ) -> Dict[str, Any]:
        """Mark attendance for multiple students"""
        session = await self.repository.get_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        created = []
        errors = []
        
        for record in records:
            result = await self.mark_attendance(session_id, record)
            if "error" in result:
                errors.append({"student_id": record.student_id, "error": result["error"]})
            else:
                created.append(record.student_id)
        
        return {
            "created": created,
            "errors": errors,
            "total": len(records)
        }
    
    async def get_student_summary(self, student_id: int,
                                 date_from: Optional[date] = None,
                                 date_to: Optional[date] = None
                                 ) -> StudentAttendanceSummary:
        """Get attendance summary for a student"""
        summary = await self.repository.get_student_attendance_summary(
            student_id, date_from, date_to
        )
        return StudentAttendanceSummary(
            student_id=student_id,
            present=summary.get("present", 0),
            absent=summary.get("absent", 0),
            late=summary.get("late", 0),
            excused=summary.get("excused", 0),
            total=summary.get("total", 0),
            percentage=summary.get("percentage", 0.0)
        )
    
    async def get_class_summary(self, class_id: int,
                               session_date: date) -> ClassAttendanceSummary:
        """Get attendance summary for a class"""
        summary = await self.repository.get_class_attendance_summary(class_id, session_date)
        return ClassAttendanceSummary(
            class_id=class_id,
            date=session_date,
            total_students=summary.get("total", 0),
            present=summary.get("present", 0),
            absent=summary.get("absent", 0),
            late=summary.get("late", 0),
            excused=summary.get("excused", 0),
            attendance_percentage=summary.get("percentage", 0.0)
        )
    
    async def get_session_with_records(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Get session with all attendance records"""
        session = await self.repository.get_session(session_id)
        if not session:
            return None
        
        records = await self.repository.get_records_by_session(session_id)
        
        return {
            "id": session.id,
            "class_id": session.class_id,
            "date": session.date,
            "subject_id": session.subject_id,
            "taken_by": session.taken_by,
            "records": [
                {
                    "id": r.id,
                    "student_id": r.student_id,
                    "status": r.status,
                    "remarks": r.remarks
                }
                for r in records
            ]
        }


__all__ = ["AttendanceService"]
