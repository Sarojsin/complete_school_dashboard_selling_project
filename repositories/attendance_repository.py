from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from models.models import Attendance, Student, Course

class AttendanceRepository:
    @staticmethod
    def get_by_id(db: Session, attendance_id: int) -> Optional[Attendance]:
        return db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    @staticmethod
    def get_by_date(db: Session, student_id: int, course_id: int, 
                    date_value: date) -> Optional[Attendance]:
        return db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.course_id == course_id,
            Attendance.date == date_value
        ).first()
    
    @staticmethod
    def create(db: Session, attendance_data: dict) -> Attendance:
        attendance = Attendance(**attendance_data)
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    @staticmethod
    def create_bulk(db: Session, attendance_list: List[dict]) -> List[Attendance]:
        """Create multiple attendance records at once"""
        records = [Attendance(**data) for data in attendance_list]
        db.add_all(records)
        db.commit()
        for record in records:
            db.refresh(record)
        return records
    
    @staticmethod
    def update(db: Session, attendance: Attendance, **kwargs) -> Attendance:
        for key, value in kwargs.items():
            if value is not None and hasattr(attendance, key):
                setattr(attendance, key, value)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    @staticmethod
    def delete(db: Session, attendance: Attendance):
        db.delete(attendance)
        db.commit()
    
    @staticmethod
    def get_student_attendance(db: Session, student_id: int, 
                              course_id: int = None) -> List[Attendance]:
        query = db.query(Attendance).options(
            joinedload(Attendance.course)
        ).filter(Attendance.student_id == student_id)
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        return query.order_by(Attendance.date.desc()).all()
    
    @staticmethod
    def get_course_attendance(db: Session, course_id: int, 
                             date_value: date = None) -> List[Attendance]:
        query = db.query(Attendance).options(
            joinedload(Attendance.student)
        ).filter(Attendance.course_id == course_id)
        
        if date_value:
            query = query.filter(Attendance.date == date_value)
        
        return query.order_by(Attendance.date.desc()).all()
    
    @staticmethod
    def get_attendance_stats(db: Session, student_id: int, 
                           course_id: int = None) -> Dict:
        """Get attendance statistics for a student"""
        query = db.query(
            Attendance.status,
            func.count(Attendance.id).label('count')
        ).filter(Attendance.student_id == student_id)
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        results = query.group_by(Attendance.status).all()
        
        stats = {status: count for status, count in results}
        total = sum(stats.values())
        
        return {
            'present': stats.get('present', 0),
            'absent': stats.get('absent', 0),
            'late': stats.get('late', 0),
            'total': total,
            'percentage': (stats.get('present', 0) / total * 100) if total > 0 else 0
        }
    
    @staticmethod
    def get_date_range_attendance(db: Session, student_id: int, 
                                  start_date: date, end_date: date) -> List[Attendance]:
        return db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date).all()
    
    @staticmethod
    def get_missing_attendance_dates(db: Session, course_id: int, 
                                    student_ids: List[int], 
                                    date_value: date) -> List[int]:
        """Get student IDs who don't have attendance for a specific date"""
        recorded = db.query(Attendance.student_id).filter(
            Attendance.course_id == course_id,
            Attendance.date == date_value
        ).all()
        
        recorded_ids = [r[0] for r in recorded]
        return [sid for sid in student_ids if sid not in recorded_ids]
    
    @staticmethod
    def get_low_attendance_students(db: Session, course_id: int, 
                                   threshold: float = 75.0) -> List[Dict]:
        """Get students with attendance below threshold percentage"""
        # Get all students enrolled in the course
        from models.models import CourseEnrollment
        
        enrolled = db.query(Student).join(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).all()
        
        low_attendance = []
        
        for student in enrolled:
            stats = AttendanceRepository.get_attendance_stats(
                db, student.id, course_id
            )
            
            if stats['percentage'] < threshold:
                low_attendance.append({
                    'student': student,
                    'percentage': stats['percentage'],
                    'present': stats['present'],
                    'absent': stats['absent'],
                    'total': stats['total']
                })
        
        return sorted(low_attendance, key=lambda x: x['percentage'])