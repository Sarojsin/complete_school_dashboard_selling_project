## services/student_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List
from datetime import date, timedelta
from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.grade_repository import GradeRepository
from repositories.fee_repository import FeeRepository

class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.student_repo = StudentRepository(db)
        self.attendance_repo = AttendanceRepository(db)
        self.grade_repo = GradeRepository(db)
        self.fee_repo = FeeRepository(db)

    async def get_student_dashboard_data(self, student_id: int) -> Dict:
        """Get comprehensive dashboard data for a student"""
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            return None
        
        # Recent grades
        recent_grades = await self.grade_repo.get_recent_grades(student_id, 5)
        
        # Attendance summary
        attendance_summary = await self.attendance_repo.get_student_attendance_summary(student_id)
        
        # Fee summary
        fee_summary = await self.fee_repo.get_fee_summary(student_id)
        
        # Recent attendance
        recent_attendance = await self.attendance_repo.get_recent_attendance(student_id, 5)
        
        # GPA
        gpa = await self.grade_repo.get_student_gpa(student_id)
        
        return {
            'student': student,
            'recent_grades': recent_grades,
            'attendance_summary': attendance_summary,
            'fee_summary': fee_summary,
            'recent_attendance': recent_attendance,
            'gpa': gpa,
            'upcoming_deadlines': await self.get_upcoming_deadlines(student_id)
        }

    async def get_upcoming_deadlines(self, student_id: int) -> List[Dict]:
        """Get upcoming assignments and tests for a student"""
        from repositories.assignment_repository import AssignmentRepository
        from repositories.test_repository import TestRepository
        
        assignment_repo = AssignmentRepository(self.db)
        test_repo = TestRepository(self.db)
        
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            return []
        
        # Upcoming assignments
        upcoming_assignments = await assignment_repo.get_upcoming_assignments(student.grade_level)
        
        # Upcoming tests
        from models.models import Course
        res = await self.db.execute(select(Course).filter(Course.grade_level == student.grade_level))
        courses = res.scalars().all()
        course_ids = [course.id for course in courses]
        
        upcoming_tests = []
        for course_id in course_ids:
            tests = await test_repo.get_available_tests_for_student(student_id, [course_id])
            upcoming_tests.extend(tests)
        
        deadlines = []
        for assignment in upcoming_assignments:
            deadlines.append({
                'type': 'assignment',
                'title': assignment.title,
                'due_date': assignment.due_date,
                'course': assignment.course.course_name if hasattr(assignment.course, 'course_name') else "N/A",
                'priority': 'high' if assignment.due_date.date() - date.today() <= timedelta(days=3) else 'medium'
            })
        
        for test in upcoming_tests:
            deadlines.append({
                'type': 'test',
                'title': test.title,
                'due_date': test.end_time,
                'course': test.course.course_name if hasattr(test.course, 'course_name') else "N/A",
                'priority': 'high' if test.end_time.date() - date.today() <= timedelta(days=1) else 'medium'
            })
        
        return sorted(deadlines, key=lambda x: x['due_date'])[:10]  # Top 10 nearest deadlines

    async def get_academic_progress(self, student_id: int) -> Dict:
        """Get comprehensive academic progress for a student"""
        grades = await self.grade_repo.get_by_student(student_id)
        attendance = await self.attendance_repo.get_by_student(student_id)
        
        # Calculate overall statistics
        total_assignments = len(grades)
        average_score = sum(grade.score for grade in grades) / total_assignments if total_assignments > 0 else 0
        total_max_score = sum(grade.max_score for grade in grades)
        average_percentage = (sum(grade.score for grade in grades) / total_max_score * 100) if total_max_score > 0 else 0
        
        # Attendance statistics
        total_days = len(attendance)
        present_days = len([a for a in attendance if a.status == 'present'])
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Course-wise progress
        course_progress = {}
        for grade in grades:
            course_name = grade.course.course_name if hasattr(grade.course, 'course_name') else "N/A"
            if course_name not in course_progress:
                course_progress[course_name] = {
                    'assignments': 0,
                    'total_score': 0,
                    'max_score': 0
                }
            
            course_progress[course_name]['assignments'] += 1
            course_progress[course_name]['total_score'] += grade.score
            course_progress[course_name]['max_score'] += grade.max_score
        
        # Calculate percentages
        for course in course_progress.values():
            course['percentage'] = (course['total_score'] / course['max_score'] * 100) if course['max_score'] > 0 else 0
        
        return {
            'total_assignments': total_assignments,
            'average_score': average_score,
            'average_percentage': average_percentage,
            'attendance_rate': attendance_rate,
            'course_progress': course_progress,
            'gpa': await self.grade_repo.get_student_gpa(student_id)
        }