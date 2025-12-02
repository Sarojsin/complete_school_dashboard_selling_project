from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Teacher, User, Course

class TeacherRepository:
    @staticmethod
    def get_by_id(db: Session, teacher_id: int) -> Optional[Teacher]:
        return db.query(Teacher).options(joinedload(Teacher.user)).filter(
            Teacher.id == teacher_id
        ).first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Teacher]:
        return db.query(Teacher).options(joinedload(Teacher.user)).filter(
            Teacher.user_id == user_id
        ).first()
    
    @staticmethod
    def get_by_employee_id(db: Session, employee_id: str) -> Optional[Teacher]:
        return db.query(Teacher).options(joinedload(Teacher.user)).filter(
            Teacher.employee_id == employee_id
        ).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, department: str = None) -> List[Teacher]:
        query = db.query(Teacher).options(joinedload(Teacher.user))
        
        if department:
            query = query.filter(Teacher.department == department)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, teacher_data: dict) -> Teacher:
        teacher = Teacher(**teacher_data)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        return teacher
    
    @staticmethod
    def update(db: Session, teacher: Teacher, **kwargs) -> Teacher:
        for key, value in kwargs.items():
            if value is not None and hasattr(teacher, key):
                setattr(teacher, key, value)
        db.commit()
        db.refresh(teacher)
        return teacher
    
    @staticmethod
    def delete(db: Session, teacher: Teacher):
        db.delete(teacher)
        db.commit()
    
    @staticmethod
    def get_teaching_courses(db: Session, teacher_id: int) -> List[Course]:
        return db.query(Course).filter(Course.teacher_id == teacher_id).all()
    
    @staticmethod
    def search(db: Session, query: str) -> List[Teacher]:
        search_pattern = f"%{query}%"
        return db.query(Teacher).join(User).filter(
            (User.full_name.ilike(search_pattern)) |
            (User.email.ilike(search_pattern)) |
            (Teacher.employee_id.ilike(search_pattern)) |
            (Teacher.department.ilike(search_pattern))
        ).limit(50).all()