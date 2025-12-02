from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Note

class NotesRepository:
    @staticmethod
    def get_by_id(db: Session, note_id: int) -> Optional[Note]:
        return db.query(Note).options(
            joinedload(Note.course),
            joinedload(Note.teacher)
        ).filter(Note.id == note_id).first()
    
    @staticmethod
    def create(db: Session, note_data: dict) -> Note:
        note = Note(**note_data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def update(db: Session, note: Note, **kwargs) -> Note:
        for key, value in kwargs.items():
            if value is not None and hasattr(note, key):
                setattr(note, key, value)
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def delete(db: Session, note: Note):
        db.delete(note)
        db.commit()
    
    @staticmethod
    def get_by_course(db: Session, course_id: int) -> List[Note]:
        return db.query(Note).options(
            joinedload(Note.teacher)
        ).filter(
            Note.course_id == course_id
        ).order_by(Note.uploaded_at.desc()).all()
    
    @staticmethod
    def get_by_teacher(db: Session, teacher_id: int) -> List[Note]:
        return db.query(Note).options(
            joinedload(Note.course)
        ).filter(
            Note.teacher_id == teacher_id
        ).order_by(Note.uploaded_at.desc()).all()
    
    @staticmethod
    def search_notes(db: Session, query: str, course_id: int = None) -> List[Note]:
        """Search notes by title or description"""
        search_pattern = f"%{query}%"
        
        search_query = db.query(Note).filter(
            (Note.title.ilike(search_pattern)) |
            (Note.description.ilike(search_pattern))
        )
        
        if course_id:
            search_query = search_query.filter(Note.course_id == course_id)
        
        return search_query.order_by(Note.uploaded_at.desc()).limit(50).all()
    
    @staticmethod
    def get_recent_notes(db: Session, course_id: int = None, limit: int = 10) -> List[Note]:
        """Get recently uploaded notes"""
        query = db.query(Note).options(
            joinedload(Note.course),
            joinedload(Note.teacher)
        )
        
        if course_id:
            query = query.filter(Note.course_id == course_id)
        
        return query.order_by(Note.uploaded_at.desc()).limit(limit).all()