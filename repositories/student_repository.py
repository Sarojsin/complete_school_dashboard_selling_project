from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Student, User, CourseEnrollment, Course
from datetime import datetime

class StudentRepository:
    @staticmethod
    def get_by_id(db: Session, student_id: int) -> Optional[Student]:
        return db.query(Student).options(joinedload(Student.user)).filter(
            Student.id == student_id
        ).first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Student]:
        return db.query(Student).options(joinedload(Student.user)).filter(
            Student.user_id == user_id
        ).first()
    
    @staticmethod
    def get_by_student_id(db: Session, student_id: str) -> Optional[Student]:
        return db.query(Student).options(joinedload(Student.user)).filter(
            Student.student_id == student_id
        ).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, grade_level: str = None) -> List[Student]:
        query = db.query(Student).options(joinedload(Student.user))
        
        if grade_level:
            query = query.filter(Student.grade_level == grade_level)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, student_data: dict) -> Student:
        student = Student(**student_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def update(db: Session, student: Student, **kwargs) -> Student:
        for key, value in kwargs.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def delete(db: Session, student: Student):
        db.delete(student)
        db.commit()
    
    @staticmethod
    def get_enrolled_courses(db: Session, student_id: int) -> List[Course]:
        return db.query(Course).join(CourseEnrollment).filter(
            CourseEnrollment.student_id == student_id
        ).all()
    
    @staticmethod
    def enroll_in_course(db: Session, student_id: int, course_id: int):
        enrollment = CourseEnrollment(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=datetime.utcnow().date()
        )
        db.add(enrollment)
        db.commit()
        return enrollment
    
    @staticmethod
    def unenroll_from_course(db: Session, student_id: int, course_id: int):
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == student_id,
            CourseEnrollment.course_id == course_id
        ).first()
        
        if enrollment:
            db.delete(enrollment)
            db.commit()
    
    @staticmethod
    def search(db: Session, query: str) -> List[Student]:
        search_pattern = f"%{query}%"
        return db.query(Student).join(User).filter(
            (User.full_name.ilike(search_pattern)) |
            (User.email.ilike(search_pattern)) |
            (Student.student_id.ilike(search_pattern))
        ).limit(50).all()