from sqlalchemy.orm import Session
from typing import Dict, List
from repositories.grade_repository import GradeRepository

class GradeService:
    def __init__(self, db: Session):
        self.db = db
        self.grade_repo = GradeRepository(db)

    def calculate_class_performance(self, course_id: int) -> Dict:
        """Calculate overall class performance for a course"""
        grades = self.grade_repo.get_by_course(course_id)
        
        if not grades:
            return {
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'grade_distribution': {},
                'total_students': 0
            }
        
        total_score = sum(grade.score for grade in grades)
        total_max_score = sum(grade.max_score for grade in grades)
        average_percentage = (total_score / total_max_score * 100) if total_max_score > 0 else 0
        
        # Grade distribution
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for grade in grades:
            if grade.max_score > 0:
                percentage = (grade.score / grade.max_score) * 100
                letter_grade = self.grade_repo.percentage_to_letter_grade(percentage)
                distribution[letter_grade] += 1
        
        # Student performance
        student_scores = {}
        for grade in grades:
            student_id = grade.student_id
            if student_id not in student_scores:
                student_scores[student_id] = {
                    'student': grade.student,
                    'total_score': 0,
                    'total_max_score': 0,
                    'assignments_count': 0
                }
            
            student_scores[student_id]['total_score'] += grade.score
            student_scores[student_id]['total_max_score'] += grade.max_score
            student_scores[student_id]['assignments_count'] += 1
        
        # Calculate percentages
        for student_data in student_scores.values():
            if student_data['total_max_score'] > 0:
                student_data['percentage'] = (student_data['total_score'] / student_data['total_max_score']) * 100
                student_data['gpa'] = self.grade_repo.percentage_to_gpa(student_data['percentage'])
        
        return {
            'average_score': round(average_percentage, 2),
            'grade_distribution': distribution,
            'student_performance': list(student_scores.values()),
            'total_assignments': len(grades),
            'top_performers': sorted(student_scores.values(), key=lambda x: x.get('percentage', 0), reverse=True)[:5],
            'needs_improvement': sorted(student_scores.values(), key=lambda x: x.get('percentage', 0))[:5]
        }