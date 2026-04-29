from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from .models import Note, NoteCategory, NoteView
from modules.school.school_teacher.models import Teacher


class NoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, note_data: dict) -> Note:
        note = Note(**note_data)
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note
    
    async def get(self, note_id: int) -> Optional[Note]:
        result = await self.db.execute(
            select(Note).filter(Note.id == note_id)
        )
        return result.scalars().first()
    
    async def get_by_course(self, course_id: int) -> List[Note]:
        result = await self.db.execute(
            select(Note).filter(
                Note.course_id == course_id,
                Note.is_published == True
            ).order_by(desc(Note.uploaded_at))
        )
        return result.scalars().all()
    
    async def get_by_teacher(self, teacher_id: int) -> List[Note]:
        result = await self.db.execute(
            select(Note).filter(Note.teacher_id == teacher_id).order_by(desc(Note.uploaded_at))
        )
        return result.scalars().all()
    
    async def get_all(self, course_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Note]:
        query = select(Note).order_by(desc(Note.uploaded_at))
        if course_id:
            query = query.filter(Note.course_id == course_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self, note_id: int, note_data: dict) -> Optional[Note]:
        note = await self.get(note_id)
        if note:
            for key, value in note_data.items():
                if value is not None and hasattr(note, key):
                    setattr(note, key, value)
            await self.db.commit()
            await self.db.refresh(note)
        return note
    
    async def delete(self, note_id: int) -> bool:
        note = await self.get(note_id)
        if note:
            await self.db.delete(note)
            await self.db.commit()
            return True
        return False
    
    async def search(self, query: str) -> List[Note]:
        """Search notes by title or description"""
        result = await self.db.execute(
            select(Note).filter(
                (Note.title.ilike(f"%{query}%")) |
                (Note.description.ilike(f"%{query}%"))
            ).order_by(desc(Note.uploaded_at))
        )
        return result.scalars().all()
    
    async def get_recent(self, limit: int = 20) -> List[Note]:
        """Get recent notes"""
        result = await self.db.execute(
            select(Note).order_by(desc(Note.uploaded_at)).limit(limit)
        )
        return result.scalars().all()