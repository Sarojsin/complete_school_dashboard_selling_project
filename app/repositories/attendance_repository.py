from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, desc, and_, case
from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from app.models.models import Attendance, Student, Course

class AttendanceRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, attendance_id: int) -> Optional[Attendance]:
        result = await db.execute(select(Attendance).filter(Attendance.id == attendance_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_date(db: AsyncSession, student_id: int, course_id: int, 
                    date_value: date) -> Optional[Attendance]:
        result = await db.execute(
            select(Attendance).filter(
                Attendance.student_id == student_id,
                Attendance.course_id == course_id,
                Attendance.date == date_value
            )
        )
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, attendance_data: dict) -> Attendance:
        attendance = Attendance(**attendance_data)
        db.add(attendance)
        await db.commit()
        await db.refresh(attendance)
        return attendance
    
    @staticmethod
    async def create_bulk(db: AsyncSession, attendance_list: List[dict]) -> List[Attendance]:
        """Create multiple attendance records at once"""
        records = [Attendance(**data) for data in attendance_list]
        db.add_all(records)
        await db.commit()
        for record in records:
            await db.refresh(record)
        return records
    
    @staticmethod
    async def update(db: AsyncSession, attendance: Attendance, **kwargs) -> Attendance:
        for key, value in kwargs.items():
            if value is not None and hasattr(attendance, key):
                setattr(attendance, key, value)
        await db.commit()
        await db.refresh(attendance)
        return attendance
    
    @staticmethod
    async def delete(db: AsyncSession, attendance: Attendance):
        await db.delete(attendance)
        await db.commit()
    
    @staticmethod
    async def get_student_attendance(db: AsyncSession, student_id: int, 
                               course_id: int = None) -> List[Attendance]:
        query = select(Attendance).options(
            joinedload(Attendance.course)
        ).filter(Attendance.student_id == student_id)
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        result = await db.execute(query.order_by(desc(Attendance.date)))
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_course_attendance(db: AsyncSession, course_id: int, 
                             date_value: date = None) -> List[Attendance]:
        query = select(Attendance).options(
            joinedload(Attendance.student)
        ).filter(Attendance.course_id == course_id)
        
        if date_value:
            query = query.filter(Attendance.date == date_value)
        
        result = await db.execute(query.order_by(desc(Attendance.date)))
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_attendance_stats(db: AsyncSession, student_id: int, 
                           course_id: int = None) -> Dict:
        """Get attendance statistics for a student"""
        query = select(
            Attendance.status,
            func.count(Attendance.id).label('count')
        ).filter(Attendance.student_id == student_id)
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        result = await db.execute(query.group_by(Attendance.status))
        results = result.all()
        
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
    async def get_date_range_attendance(db: AsyncSession, student_id: int, 
                                  start_date: date, end_date: date) -> List[Attendance]:
        result = await db.execute(
            select(Attendance).filter(
                Attendance.student_id == student_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            ).order_by(Attendance.date)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_missing_attendance_dates(db: AsyncSession, course_id: int, 
                                    student_ids: List[int], 
                                    date_value: date) -> List[int]:
        """Get student IDs who don't have attendance for a specific date"""
        result = await db.execute(
            select(Attendance.student_id).filter(
                Attendance.course_id == course_id,
                Attendance.date == date_value
            )
        )
        recorded_ids = [r[0] for r in result.all()]
        return [sid for sid in student_ids if sid not in recorded_ids]
    
    @staticmethod
    async def get_low_attendance_students(db: AsyncSession, course_id: int, 
                                   threshold: float = 75.0) -> List[Dict]:
        """Get students with attendance below threshold percentage"""
        from app.models.models import CourseEnrollment
        
        res = await db.execute(
            select(Student).join(CourseEnrollment).filter(
                CourseEnrollment.course_id == course_id
            )
        )
        enrolled = res.scalars().all()
        
        low_attendance = []
        for student in enrolled:
            stats = await AttendanceRepository.get_attendance_stats(
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

    @staticmethod
    async def get_teacher_attendance_history(db: AsyncSession, teacher_id: int) -> List[Dict]:
        """Fetch attendance history grouped by date and course for a teacher"""
        # First get all courses for this teacher
        course_stmt = select(Course.id).filter(Course.teacher_id == teacher_id)
        course_result = await db.execute(course_stmt)
        course_ids = [r[0] for r in course_result.all()]
        
        if not course_ids:
            return []
            
        # Group attendance by date and course_id
        stmt = select(
            Attendance.date,
            Attendance.course_id,
            func.count(Attendance.id).label('total'),
            func.sum(case((Attendance.status == 'present', 1), else_=0)).label('present'),
            func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent'),
            func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late')
        ).filter(
            Attendance.course_id.in_(course_ids)
        ).group_by(
            Attendance.date, Attendance.course_id
        ).order_by(
            desc(Attendance.date)
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        history = []
        for row in rows:
            course = await db.get(Course, row.course_id)
            history.append({
                "id": f"{row.course_id}_{row.date}", # Virtual ID
                "date": row.date.strftime("%Y-%m-%d"),
                "day": row.date.strftime("%A"),
                "class": course.grade_level if course else "N/A",
                "subject": course.course_name if course else "N/A",
                "present": int(row.present or 0),
                "absent": int(row.absent or 0),
                "late": int(row.late or 0),
                "percentage": round((int(row.present or 0) / int(row.total or 1)) * 100, 1)
            })
            
        return history

    @staticmethod
    async def get_overall_stats(db: AsyncSession, teacher_id: int) -> Dict:
        """Calculate stats for teacher's attendance dashboard"""
        course_stmt = select(Course.id).filter(Course.teacher_id == teacher_id)
        course_result = await db.execute(course_stmt)
        course_ids = [r[0] for r in course_result.all()]
        
        if not course_ids:
            return {
                "total_students": 0, "present_today": 0, "absent_today": 0, "overall_percentage": 0,
                "present_percentage": 0, "absent_percentage": 0, "late_percentage": 0
            }
            
        today = date.today()
        
        # Today's stats
        today_stmt = select(
            Attendance.status,
            func.count(Attendance.id)
        ).filter(
            Attendance.course_id.in_(course_ids),
            Attendance.date == today
        ).group_by(Attendance.status)
        
        today_res = await db.execute(today_stmt)
        today_stats = {status: count for status, count in today_res.all()}
        
        # Total student count (unique students across all courses)
        from app.models.models import CourseEnrollment
        student_stmt = select(func.count(func.distinct(CourseEnrollment.student_id))).filter(CourseEnrollment.course_id.in_(course_ids))
        student_count = (await db.execute(student_stmt)).scalar() or 0
        
        # All time stats for percentages
        all_stmt = select(
            Attendance.status,
            func.count(Attendance.id)
        ).filter(Attendance.course_id.in_(course_ids)).group_by(Attendance.status)
        
        all_res = await db.execute(all_stmt)
        all_stats = {status: count for status, count in all_res.all()}
        total_records = sum(all_stats.values()) or 1
        
        return {
            "total_students": student_count,
            "present_today": today_stats.get('present', 0),
            "absent_today": today_stats.get('absent', 0),
            "overall_percentage": round((all_stats.get('present', 0) / total_records) * 100, 1),
            "present_percentage": round((all_stats.get('present', 0) / total_records) * 100, 1),
            "absent_percentage": round((all_stats.get('absent', 0) / total_records) * 100, 1),
            "late_percentage": round((all_stats.get('late', 0) / total_records) * 100, 1)
        }
