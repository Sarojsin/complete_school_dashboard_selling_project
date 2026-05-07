"""
College Department Models

SQLAlchemy models for college department management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase

class CollegeDepartment(CollegeBase):
    __tablename__ = "college_departments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    hod_teacher_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    hod = relationship("CollegeFaculty", foreign_keys=[hod_teacher_id])
    programs = relationship("CollegeProgram", back_populates="department")

    def __repr__(self):
        return f"<CollegeDepartment(id={self.id}, code='{self.code}', name='{self.name}')>"


__all__ = ["CollegeDepartment"]