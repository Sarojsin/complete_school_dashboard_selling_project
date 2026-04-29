from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base

class Video(Base):
    __tablename__ = "school_videos"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("SchoolCourse")
    teacher = relationship("Teacher")


class VideoProgress(Base):
    __tablename__ = "school_video_progress"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("school_videos.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    watched_seconds = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    last_viewed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    video = relationship("Video")
    student = relationship("SchoolStudent")
