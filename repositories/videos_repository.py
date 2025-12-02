from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.models import Video

class VideosRepository:
    @staticmethod
    def get_by_id(db: Session, video_id: int) -> Optional[Video]:
        return db.query(Video).options(
            joinedload(Video.course),
            joinedload(Video.teacher)
        ).filter(Video.id == video_id).first()
    
    @staticmethod
    def create(db: Session, video_data: dict) -> Video:
        video = Video(**video_data)
        db.add(video)
        db.commit()
        db.refresh(video)
        return video
    
    @staticmethod
    def update(db: Session, video: Video, **kwargs) -> Video:
        for key, value in kwargs.items():
            if value is not None and hasattr(video, key):
                setattr(video, key, value)
        db.commit()
        db.refresh(video)
        return video
    
    @staticmethod
    def delete(db: Session, video: Video):
        db.delete(video)
        db.commit()
    
    @staticmethod
    def get_by_course(db: Session, course_id: int) -> List[Video]:
        return db.query(Video).options(
            joinedload(Video.teacher)
        ).filter(
            Video.course_id == course_id
        ).order_by(Video.uploaded_at.desc()).all()
    
    @staticmethod
    def get_by_teacher(db: Session, teacher_id: int) -> List[Video]:
        return db.query(Video).options(
            joinedload(Video.course)
        ).filter(
            Video.teacher_id == teacher_id
        ).order_by(Video.uploaded_at.desc()).all()
    
    @staticmethod
    def search_videos(db: Session, query: str, course_id: int = None) -> List[Video]:
        """Search videos by title or description"""
        search_pattern = f"%{query}%"
        
        search_query = db.query(Video).filter(
            (Video.title.ilike(search_pattern)) |
            (Video.description.ilike(search_pattern))
        )
        
        if course_id:
            search_query = search_query.filter(Video.course_id == course_id)
        
        return search_query.order_by(Video.uploaded_at.desc()).limit(50).all()
    
    @staticmethod
    def get_recent_videos(db: Session, course_id: int = None, limit: int = 10) -> List[Video]:
        """Get recently uploaded videos"""
        query = db.query(Video).options(
            joinedload(Video.course),
            joinedload(Video.teacher)
        )
        
        if course_id:
            query = query.filter(Video.course_id == course_id)
        
        return query.order_by(Video.uploaded_at.desc()).limit(limit).all()