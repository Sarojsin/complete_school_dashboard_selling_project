from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, List
from datetime import date, timedelta
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.grade_repository import GradeRepository

class TeacherService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.teacher_repo = TeacherRepository(db)
        self.course_repo = CourseRepository(db)
        self.attendance_repo = AttendanceRepository(db)
        self.grade_repo = GradeRepository(db)

    async def get_teacher_dashboard_data(self, teacher_id: int) -> Dict:
        """Get comprehensive dashboard data for a teacher"""
        teacher = await self.teacher_repo.get_by_id(teacher_id)
        if not teacher:
            return None
        
        # Get teacher's courses
        courses = await self.course_repo.get_all(teacher_id=teacher_id)
        
        # Course statistics
        course_stats = []
        for course in courses:
            stats = await self.attendance_repo.get_course_attendance_summary(course.id)
            avg_grade = await self.grade_repo.get_course_average(course.id)
            grade_distribution = await self.grade_repo.get_grade_distribution(course.id)
            
            course_stats.append({
                'course': course,
                'attendance_stats': stats,
                'average_grade': avg_grade,
                'grade_distribution': grade_distribution
            })
        
        # Recent activity
        # recent_activity = await self.get_recent_activity(teacher_id)
        
        # Upcoming deadlines
        # upcoming_deadlines = await self.get_upcoming_deadlines(teacher_id)
        
        return {
            'teacher': teacher,
            'courses': courses,
            'course_stats': course_stats,
             "student_count": await self.get_total_students(teacher_id),
             "recent_activity": await self.get_recent_activity(teacher_id),
             "upcoming_deadlines": await self.get_upcoming_deadlines(teacher_id)
        }

    async def get_recent_activity(self, teacher_id: int) -> List[Dict]:
        """Get recent activity for a teacher"""
        from repositories.assignment_repository import AssignmentRepository
        from repositories.test_repository import TestRepository
        
        assignment_repo = AssignmentRepository(self.db)
        test_repo = TestRepository(self.db)
        
        recent_assignments = (await assignment_repo.get_by_teacher(teacher_id))[:5]
        recent_tests = (await test_repo.get_tests_by_teacher(teacher_id))[:5]
        
        activity = []
        
        for assignment in recent_assignments:
            activity.append({
                'type': 'assignment',
                'title': assignment.title,
                'date': assignment.created_at,
                'course': assignment.course.course_name if hasattr(assignment.course, 'course_name') else "N/A",
                'action': 'created'
            })
        
        for test in recent_tests:
            activity.append({
                'type': 'test',
                'title': test.title,
                'date': test.created_at,
                'course': test.course.course_name if hasattr(test.course, 'course_name') else "N/A",
                'action': 'created'
            })
        
        return sorted(activity, key=lambda x: x['date'], reverse=True)[:10]

    async def get_upcoming_deadlines(self, teacher_id: int) -> List[Dict]:
        """Get upcoming deadlines for a teacher"""
        from repositories.assignment_repository import AssignmentRepository
        
        assignment_repo = AssignmentRepository(self.db)
        assignments = await assignment_repo.get_by_teacher(teacher_id)
        
        upcoming = []
        for assignment in assignments:
            if assignment.due_date and assignment.due_date.date() >= date.today():
                days_until_due = (assignment.due_date.date() - date.today()).days
                upcoming.append({
                    'type': 'assignment',
                    'title': assignment.title,
                    'due_date': assignment.due_date,
                    'course': assignment.course.course_name if hasattr(assignment.course, 'course_name') else "N/A",
                    'days_until_due': days_until_due,
                    'priority': 'high' if days_until_due <= 2 else 'medium'
                })
        
        return sorted(upcoming, key=lambda x: x['due_date'])[:5]

    async def get_total_students(self, teacher_id: int) -> int:
        """Get total number of students taught by this teacher"""
        from models.models import Student, Course
        courses = await self.course_repo.get_all(teacher_id=teacher_id)
        
        total_students = 0
        for course in courses:
             res = await self.db.execute(select(func.count(Student.id)).filter(Student.grade_level == course.grade_level))
             total_students += res.scalar() or 0
        
        return total_students

    async def get_course_analytics(self, course_id: int) -> Dict:
        """Get detailed analytics for a specific course"""
        attendance_summary = await self.attendance_repo.get_course_attendance_summary(course_id)
        average_grade = await self.grade_repo.get_course_average(course_id)
        grade_distribution = await self.grade_repo.get_grade_distribution(course_id)
        
        # Student performance ranking
        grades = await self.grade_repo.get_by_course(course_id)
        student_performance = {}
        
        for grade in grades:
            student_id = grade.student_id
            if student_id not in student_performance:
                student_performance[student_id] = {
                    'student': grade.student,
                    'total_score': 0,
                    'max_score': 0,
                    'assignments_count': 0
                }
            
            student_performance[student_id]['total_score'] += grade.score
            student_performance[student_id]['max_score'] += grade.max_score
            student_performance[student_id]['assignments_count'] += 1
        
        # Calculate percentages and sort
        ranked_students = []
        for performance in student_performance.values():
            if performance['max_score'] > 0:
                percentage = (performance['total_score'] / performance['max_score']) * 100
                performance['percentage'] = percentage
                ranked_students.append(performance)
        
        ranked_students.sort(key=lambda x: x.get('percentage', 0), reverse=True)
        
        return {
            'attendance_summary': attendance_summary,
            'average_grade': average_grade,
            'grade_distribution': grade_distribution,
            'student_ranking': ranked_students,
            'total_assignments': len(grades),
            'top_performer': ranked_students[0] if ranked_students else None,
            'needs_improvement': ranked_students[-1] if ranked_students else None
        }