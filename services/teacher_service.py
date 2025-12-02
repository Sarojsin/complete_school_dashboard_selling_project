from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import date, timedelta
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.grade_repository import GradeRepository

class TeacherService:
    def __init__(self, db: Session):
        self.db = db
        self.teacher_repo = TeacherRepository(db)
        self.course_repo = CourseRepository(db)
        self.attendance_repo = AttendanceRepository(db)
        self.grade_repo = GradeRepository(db)

    def get_teacher_dashboard_data(self, teacher_id: int) -> Dict:
        """Get comprehensive dashboard data for a teacher"""
        teacher = self.teacher_repo.get_by_id(teacher_id)
        if not teacher:
            return None
        
        # Get teacher's courses
        courses = self.course_repo.get_by_teacher(teacher_id)
        
        # Course statistics
        course_stats = []
        for course in courses:
            stats = self.attendance_repo.get_course_attendance_summary(course.id)
            avg_grade = self.grade_repo.get_course_average(course.id)
            grade_distribution = self.grade_repo.get_grade_distribution(course.id)
            
            course_stats.append({
                'course': course,
                'attendance_stats': stats,
                'average_grade': avg_grade,
                'grade_distribution': grade_distribution
            })
        
        # Recent activity
        recent_activity = self.get_recent_activity(teacher_id)
        
        # Upcoming deadlines
        upcoming_deadlines = self.get_upcoming_deadlines(teacher_id)
        
        return {
            'teacher': teacher,
            'courses': courses,
            'course_stats': course_stats,
            'recent_activity': recent_activity,
            'upcoming_deadlines': upcoming_deadlines,
            'total_students': self.get_total_students(teacher_id)
        }

    def get_recent_activity(self, teacher_id: int) -> List[Dict]:
        """Get recent activity for a teacher"""
        from repositories.assignment_repository import AssignmentRepository
        from repositories.test_repository import TestRepository
        
        assignment_repo = AssignmentRepository(self.db)
        test_repo = TestRepository(self.db)
        
        recent_assignments = assignment_repo.get_by_teacher(teacher_id)[:5]
        recent_tests = test_repo.get_tests_by_teacher(teacher_id)[:5]
        
        activity = []
        
        for assignment in recent_assignments:
            activity.append({
                'type': 'assignment',
                'title': assignment.title,
                'date': assignment.created_at,
                'course': assignment.course.name,
                'action': 'created'
            })
        
        for test in recent_tests:
            activity.append({
                'type': 'test',
                'title': test.title,
                'date': test.created_at,
                'course': test.course.name,
                'action': 'created'
            })
        
        return sorted(activity, key=lambda x: x['date'], reverse=True)[:10]

    def get_upcoming_deadlines(self, teacher_id: int) -> List[Dict]:
        """Get upcoming deadlines for a teacher"""
        from repositories.assignment_repository import AssignmentRepository
        
        assignment_repo = AssignmentRepository(self.db)
        assignments = assignment_repo.get_by_teacher(teacher_id)
        
        upcoming = []
        for assignment in assignments:
            if assignment.due_date and assignment.due_date.date() >= date.today():
                days_until_due = (assignment.due_date.date() - date.today()).days
                upcoming.append({
                    'type': 'assignment',
                    'title': assignment.title,
                    'due_date': assignment.due_date,
                    'course': assignment.course.name,
                    'days_until_due': days_until_due,
                    'priority': 'high' if days_until_due <= 2 else 'medium'
                })
        
        return sorted(upcoming, key=lambda x: x['due_date'])[:5]

    def get_total_students(self, teacher_id: int) -> int:
        """Get total number of students taught by this teacher"""
        from models.models import Student, Course
        courses = self.course_repo.get_by_teacher(teacher_id)
        
        total_students = 0
        for course in courses:
            # Count students in the same grade as the course
            student_count = self.db.query(Student).filter(
                Student.grade == course.grade
            ).count()
            total_students += student_count
        
        return total_students

    def get_course_analytics(self, course_id: int) -> Dict:
        """Get detailed analytics for a specific course"""
        attendance_summary = self.attendance_repo.get_course_attendance_summary(course_id)
        average_grade = self.grade_repo.get_course_average(course_id)
        grade_distribution = self.grade_repo.get_grade_distribution(course_id)
        
        # Student performance ranking
        grades = self.grade_repo.get_by_course(course_id)
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
        
        ranked_students.sort(key=lambda x: x['percentage'], reverse=True)
        
        return {
            'attendance_summary': attendance_summary,
            'average_grade': average_grade,
            'grade_distribution': grade_distribution,
            'student_ranking': ranked_students,
            'total_assignments': len(grades),
            'top_performer': ranked_students[0] if ranked_students else None,
            'needs_improvement': ranked_students[-1] if ranked_students else None
        }