from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc, and_, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.models import Video, VideoProgress, Teacher

class VideosRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, video_id: int) -> Optional[Video]:
        result = await db.execute(
            select(Video).options(
                joinedload(Video.course),
                joinedload(Video.teacher).joinedload(Teacher.user)
            ).filter(Video.id == video_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, video_data: dict) -> Video:
        video = Video(**video_data)
        db.add(video)
        await db.commit()
        await db.refresh(video)
        return video
    
    @staticmethod
    async def update(db: AsyncSession, video: Video, **kwargs) -> Video:
        for key, value in kwargs.items():
            if value is not None and hasattr(video, key):
                setattr(video, key, value)
        await db.commit()
        await db.refresh(video)
        return video
    
    @staticmethod
    async def delete(db: AsyncSession, video: Video):
        await db.delete(video)
        await db.commit()
    
    @staticmethod
    async def get_by_course(db: AsyncSession, course_id: int) -> List[Video]:
        result = await db.execute(
            select(Video).options(
                joinedload(Video.teacher).joinedload(Teacher.user)
            ).filter(
                Video.course_id == course_id
            ).order_by(desc(Video.uploaded_at))
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_by_teacher(db: AsyncSession, teacher_id: int) -> List[Video]:
        result = await db.execute(
            select(Video).options(
                joinedload(Video.course)
            ).filter(
                Video.teacher_id == teacher_id
            ).order_by(desc(Video.uploaded_at))
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def search_videos(db: AsyncSession, query: str, course_id: int = None) -> List[Video]:
        """Search videos by title or description"""
        search_pattern = f"%{query}%"
        
        search_query = select(Video).filter(
            or_(
                Video.title.ilike(search_pattern),
                Video.description.ilike(search_pattern)
            )
        )
        
        if course_id:
            search_query = search_query.filter(Video.course_id == course_id)
        
        result = await db.execute(search_query.order_by(desc(Video.uploaded_at)).limit(50))
        return result.scalars().all()
    
    @staticmethod
    async def get_recent_videos(db: AsyncSession, course_id: int = None, limit: int = 10) -> List[Video]:
        """Get recently uploaded videos"""
        query = select(Video).options(
            joinedload(Video.course),
            joinedload(Video.teacher).joinedload(Teacher.user)
        )
        
        if course_id:
            query = query.filter(Video.course_id == course_id)
        
        result = await db.execute(query.order_by(desc(Video.uploaded_at)).limit(limit))
        return result.scalars().unique().all()

    @staticmethod
    async def mark_as_watched(db: AsyncSession, video_id: int, student_id: int):
        """Mark a video as watched by a student"""
        # Check if already marked
        result = await db.execute(
            select(VideoProgress).filter(
                and_(VideoProgress.video_id == video_id, VideoProgress.student_id == student_id)
            )
        )
        existing = result.scalars().first()
        if not existing:
            progress = VideoProgress(video_id=video_id, student_id=student_id)
            db.add(progress)
            await db.commit()
            return True
        return False

    @staticmethod
    async def get_student_watched_ids(db: AsyncSession, student_id: int) -> List[int]:
        """Get IDs of videos watched by a student"""
        result = await db.execute(
            select(VideoProgress.video_id).filter(VideoProgress.student_id == student_id)
        )
        return result.scalars().all()