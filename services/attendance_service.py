from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Dict, List
from repositories.attendance_repository import AttendanceRepository

class AttendanceService:
    def __init__(self, db: Session):
        self.db = db
        self.attendance_repo = AttendanceRepository(db)

    def get_monthly_attendance_report(self, student_id: int, year: int, month: int) -> Dict:
        """Generate monthly attendance report for a student"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        attendance_records = self.attendance_repo.get_by_student(student_id, start_date, end_date)
        
        # Calculate statistics
        total_days = (end_date - start_date).days + 1
        present_days = len([r for r in attendance_records if r.status == 'present'])
        absent_days = len([r for r in attendance_records if r.status == 'absent'])
        late_days = len([r for r in attendance_records if r.status == 'late'])
        
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        
        return {
            'student_id': student_id,
            'month': f"{year}-{month:02d}",
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'attendance_rate': round(attendance_rate, 2),
            'records': attendance_records
        }

    def bulk_mark_attendance(self, course_id: int, attendance_date: date, attendance_data: List[Dict]) -> Dict:
        """Mark attendance for multiple students at once"""
        from tables.tables import AttendanceCreate
        
        attendance_list = []
        for data in attendance_data:
            attendance_list.append(
                AttendanceCreate(
                    student_id=data['student_id'],
                    course_id=course_id,
                    date=attendance_date,
                    status=data['status']
                )
            )
        
        records = self.attendance_repo.mark_attendance(attendance_list)
        
        return {
            'message': f'Attendance marked for {len(records)} students',
            'date': attendance_date,
            'course_id': course_id
        }