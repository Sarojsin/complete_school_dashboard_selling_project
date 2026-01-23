from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.models import Note

class NotesRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, note_id: int) -> Optional[Note]:
        result = await db.execute(
            select(Note).options(
                joinedload(Note.course),
                joinedload(Note.teacher)
            ).filter(Note.id == note_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, note_data: dict) -> Note:
        note = Note(**note_data)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    
    @staticmethod
    async def update(db: AsyncSession, note: Note, **kwargs) -> Note:
        for key, value in kwargs.items():
            if value is not None and hasattr(note, key):
                setattr(note, key, value)
        await db.commit()
        await db.refresh(note)
        return note
    
    @staticmethod
    async def delete(db: AsyncSession, note: Note):
        await db.delete(note)
        await db.commit()
    
    @staticmethod
    async def get_by_course(db: AsyncSession, course_id: int) -> List[Note]:
        result = await db.execute(
            select(Note).options(
                joinedload(Note.teacher)
            ).filter(
                Note.course_id == course_id
            ).order_by(desc(Note.uploaded_at))
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_by_teacher(db: AsyncSession, teacher_id: int) -> List[Note]:
        result = await db.execute(
            select(Note).options(
                joinedload(Note.course)
            ).filter(
                Note.teacher_id == teacher_id
            ).order_by(desc(Note.uploaded_at))
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def search_notes(db: AsyncSession, query: str, course_id: int = None) -> List[Note]:
        """Search notes by title or description"""
        search_pattern = f"%{query}%"
        
        search_query = select(Note).filter(
            or_(
                Note.title.ilike(search_pattern),
                Note.description.ilike(search_pattern)
            )
        )
        
        if course_id:
            search_query = search_query.filter(Note.course_id == course_id)
        
        result = await db.execute(search_query.order_by(desc(Note.uploaded_at)).limit(50))
        return result.scalars().all()
    
    @staticmethod
    async def get_recent_notes(db: AsyncSession, course_id: int = None, limit: int = 10) -> List[Note]:
        """Get recently uploaded notes"""
        query = select(Note).options(
            joinedload(Note.course),
            joinedload(Note.teacher)
        )
        
        if course_id:
            query = query.filter(Note.course_id == course_id)
        
        result = await db.execute(query.order_by(desc(Note.uploaded_at)).limit(limit))
        return result.scalars().unique().all()