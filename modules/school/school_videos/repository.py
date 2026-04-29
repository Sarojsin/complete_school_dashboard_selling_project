from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc
from typing import List, Optional
from .models import Video, VideoProgress

class VideosRepository:
    @staticmethod
    async def create(db: AsyncSession, video_data: dict) -> Video:
        video = Video(**video_data)
        db.add(video)
        await db.commit()
        await db.refresh(video)
        return video

    @staticmethod
    async def get_by_id(db: AsyncSession, video_id: int) -> Optional[Video]:
        result = await db.execute(select(Video).filter(Video.id == video_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_course(db: AsyncSession, course_id: int) -> List[Video]:
        result = await db.execute(select(Video).filter(Video.course_id == course_id, Video.is_published == True))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_teacher(db: AsyncSession, teacher_id: int) -> List[Video]:
        result = await db.execute(select(Video).filter(Video.teacher_id == teacher_id))
        return list(result.scalars().all())

    @staticmethod
    async def get_all(db: AsyncSession, course_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Video]:
        query = select(Video).filter(Video.is_published == True)
        if course_id:
            query = query.filter(Video.course_id == course_id)
        query = query.offset(skip).limit(limit).order_by(desc(Video.created_at))
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update(db: AsyncSession, video: Video, update_data: dict) -> Video:
        for key, value in update_data.items():
            setattr(video, key, value)
        await db.commit()
        await db.refresh(video)
        return video

    @staticmethod
    async def delete(db: AsyncSession, video: Video) -> bool:
        await db.delete(video)
        await db.commit()
        return True

    @staticmethod
    async def search_videos(db: AsyncSession, query: str, course_id: Optional[int] = None) -> List[Video]:
        stmt = select(Video).filter(Video.title.ilike(f"%{query}%"), Video.is_published == True)
        if course_id:
            stmt = stmt.filter(Video.course_id == course_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_recent_videos(db: AsyncSession, limit: int = 10) -> List[Video]:
        result = await db.execute(select(Video).filter(Video.is_published == True).order_by(desc(Video.created_at)).limit(limit))
        return list(result.scalars().all())

# Alias for singular name used in some places
VideoRepository = VideosRepository
