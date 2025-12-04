from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models.models import Parent, Student
from repositories.student_repository import StudentRepository

class ParentRepository:
    @staticmethod
    def create(db: Session, parent_data: dict) -> Parent:
        parent = Parent(**parent_data)
        db.add(parent)
        db.commit()
        db.refresh(parent)
        return parent
    
    @staticmethod
    def get_by_id(db: Session, parent_id: int) -> Optional[Parent]:
        return db.query(Parent).filter(Parent.id == parent_id).first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Parent]:
        return db.query(Parent).filter(Parent.user_id == user_id).first()
    
    @staticmethod
    def get_children(db: Session, parent_id: int) -> List[Student]:
        """Get all children of a parent"""
        return db.query(Student).filter(Student.parent_id == parent_id).all()
    
    @staticmethod
    def link_child(db: Session, parent_id: int, student_id: int):
        """Link a child to a parent"""
        student = StudentRepository.get_by_id(db, student_id)
        if student:
            student.parent_id = parent_id
            db.commit()
            db.refresh(student)
        return student
    
    @staticmethod
    def update(db: Session, parent: Parent, **kwargs) -> Parent:
        for key, value in kwargs.items():
            if value is not None and hasattr(parent, key):
                setattr(parent, key, value)
        db.commit()
        db.refresh(parent)
        return parent
    
    @staticmethod
    def delete(db: Session, parent: Parent):
        db.delete(parent)
        db.commit()
