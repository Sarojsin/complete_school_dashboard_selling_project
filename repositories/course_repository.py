from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Course, Teacher, Student, CourseEnrollment

class CourseRepository:
    @staticmethod
    def get_by_id(db: Session, course_id: int) -> Optional[Course]:
        return db.query(Course).options(
            joinedload(Course.teacher).joinedload(Teacher.user)
        ).filter(Course.id == course_id).first()
    
    @staticmethod
    def get_by_code(db: Session, course_code: str) -> Optional[Course]:
        return db.query(Course).filter(Course.course_code == course_code).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, 
                grade_level: str = None, teacher_id: int = None) -> List[Course]:
        query = db.query(Course).options(
            joinedload(Course.teacher).joinedload(Teacher.user)
        )
        
        if grade_level:
            query = query.filter(Course.grade_level == grade_level)
        
        if teacher_id:
            query = query.filter(Course.teacher_id == teacher_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, course_data: dict) -> Course:
        course = Course(**course_data)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def update(db: Session, course: Course, **kwargs) -> Course:
        for key, value in kwargs.items():
            if value is not None and hasattr(course, key):
                setattr(course, key, value)
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def delete(db: Session, course: Course):
        db.delete(course)
        db.commit()
    
    @staticmethod
    def get_enrolled_students(db: Session, course_id: int) -> List[Student]:
        return db.query(Student).join(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).all()
    
    @staticmethod
    def get_enrollment_count(db: Session, course_id: int) -> int:
        return db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).count()
    
    @staticmethod
    def search(db: Session, query: str) -> List[Course]:
        search_pattern = f"%{query}%"
        return db.query(Course).filter(
            (Course.course_name.ilike(search_pattern)) |
            (Course.course_code.ilike(search_pattern)) |
            (Course.description.ilike(search_pattern))
        ).limit(50).all()