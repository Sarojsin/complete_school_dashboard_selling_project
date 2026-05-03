"""
School Attendance Models

SQLAlchemy models for school attendance management.
Imports from existing app models to avoid duplication.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base
from modules.school.school_classes.models import SchoolClass
from modules.school.school_subjects.models import SchoolSubject


class AttendanceSession(Base):
    """
    Attendance session model - tracks daily attendance sessions
    """
    __tablename__ = "attendance_sessions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"))
    date = Column(Date, nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("school_subjects.id"))
    taken_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    school_class = relationship(SchoolClass)
    subject = relationship(SchoolSubject)
    attendance_records = relationship("AttendanceRecord", back_populates="session")


class AttendanceRecord(Base):
    """
    Individual attendance record for a student
    """
    __tablename__ = "attendance_records"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"))
    student_id = Column(Integer, ForeignKey("school_students.id"), nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late, excused
    remarks = Column(Text)
    marked_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    session = relationship("AttendanceSession", back_populates="attendance_records")
    student = relationship("SchoolStudent")


__all__ = ["AttendanceSession", "AttendanceRecord"]
