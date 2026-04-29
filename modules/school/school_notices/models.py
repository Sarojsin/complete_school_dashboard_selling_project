from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base


class Notice(Base):
    __tablename__ = "notices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    authority_id = Column(Integer, ForeignKey("school_authorities.id", ondelete="CASCADE"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=True)
    target_role = Column(String(20))  # all, student, teacher
    target_grade = Column(String(50))
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    # Relationships - using string references for now
    # authority = relationship("Authority", back_populates="notices")
    # teacher = relationship("Teacher", back_populates="notices")