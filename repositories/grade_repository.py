from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional, Dict
from models.models import Grade

class GradeRepository:
    @staticmethod
    def get_by_id(db: Session, grade_id: int) -> Optional[Grade]:
        return db.query(Grade).filter(Grade.id == grade_id).first()
    
    @staticmethod
    def create(db: Session, grade_data: dict) -> Grade:
        grade = Grade(**grade_data)
        db.add(grade)
        db.commit()
        db.refresh(grade)
        return grade
    
    @staticmethod
    def create_bulk(db: Session, grades_list: List[dict]) -> List[Grade]:
        """Create multiple grades at once"""
        grades = [Grade(**data) for data in grades_list]
        db.add_all(grades)
        db.commit()
        for grade in grades:
            db.refresh(grade)
        return grades
    
    @staticmethod
    def update(db: Session, grade: Grade, **kwargs) -> Grade:
        for key, value in kwargs.items():
            if value is not None and hasattr(grade, key):
                setattr(grade, key, value)
        db.commit()
        db.refresh(grade)
        return grade
    
    @staticmethod
    def delete(db: Session, grade: Grade):
        db.delete(grade)
        db.commit()
    
    @staticmethod
    def get_student_grades(db: Session, student_id: int, 
                          course_id: int = None) -> List[Grade]:
        query = db.query(Grade).options(
            joinedload(Grade.course)
        ).filter(Grade.student_id == student_id)
        
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        return query.order_by(Grade.date.desc()).all()
    
    @staticmethod
    def get_course_grades(db: Session, course_id: int, 
                         grade_type: str = None) -> List[Grade]:
        query = db.query(Grade).options(
            joinedload(Grade.student)
        ).filter(Grade.course_id == course_id)
        
        if grade_type:
            query = query.filter(Grade.grade_type == grade_type)
        
        return query.order_by(Grade.date.desc()).all()
    
    @staticmethod
    def get_grade_statistics(db: Session, student_id: int, 
                           course_id: int = None) -> Dict:
        """Calculate grade statistics for a student"""
        query = db.query(
            func.avg(Grade.score / Grade.max_score * 100).label('average'),
            func.max(Grade.score / Grade.max_score * 100).label('highest'),
            func.min(Grade.score / Grade.max_score * 100).label('lowest'),
            func.count(Grade.id).label('total_grades')
        ).filter(Grade.student_id == student_id)
        
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        result = query.first()
        
        return {
            'average': round(result.average, 2) if result.average else 0,
            'highest': round(result.highest, 2) if result.highest else 0,
            'lowest': round(result.lowest, 2) if result.lowest else 0,
            'total_grades': result.total_grades or 0
        }
    
    @staticmethod
    def get_class_statistics(db: Session, course_id: int, 
                           grade_type: str = None) -> Dict:
        """Calculate grade statistics for entire class"""
        query = db.query(
            func.avg(Grade.score / Grade.max_score * 100).label('average'),
            func.max(Grade.score / Grade.max_score * 100).label('highest'),
            func.min(Grade.score / Grade.max_score * 100).label('lowest'),
            func.count(func.distinct(Grade.student_id)).label('total_students')
        ).filter(Grade.course_id == course_id)
        
        if grade_type:
            query = query.filter(Grade.grade_type == grade_type)
        
        result = query.first()
        
        return {
            'average': round(result.average, 2) if result.average else 0,
            'highest': round(result.highest, 2) if result.highest else 0,
            'lowest': round(result.lowest, 2) if result.lowest else 0,
            'total_students': result.total_students or 0
        }
    
    @staticmethod
    def get_gpa(db: Session, student_id: int) -> float:
        """Calculate GPA (simplified version)"""
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
        
        grades = db.query(Grade).filter(
            Grade.student_id == student_id,
            Grade.grade.isnot(None)
        ).all()
        
        if not grades:
            return 0.0
        
        total_points = sum(grade_points.get(g.grade, 0) for g in grades)
        return round(total_points / len(grades), 2)
    
    @staticmethod
    def get_grade_distribution(db: Session, course_id: int) -> Dict:
        """Get distribution of letter grades for a course"""
        results = db.query(
            Grade.grade,
            func.count(Grade.id).label('count')
        ).filter(
            Grade.course_id == course_id,
            Grade.grade.isnot(None)
        ).group_by(Grade.grade).all()
        
        return {grade: count for grade, count in results}
    
    @staticmethod
    def get_top_performers(db: Session, course_id: int, limit: int = 10) -> List[Dict]:
        """Get top performing students in a course"""
        results = db.query(
            Grade.student_id,
            func.avg(Grade.score / Grade.max_score * 100).label('average')
        ).filter(
            Grade.course_id == course_id
        ).group_by(
            Grade.student_id
        ).order_by(
            func.avg(Grade.score / Grade.max_score * 100).desc()
        ).limit(limit).all()
        
        top_performers = []
        for student_id, average in results:
            student = db.query(Grade.student).filter(
                Grade.student_id == student_id
            ).first()
            
            if student:
                top_performers.append({
                    'student': student.student,
                    'average': round(average, 2)
                })
        
        return top_performers