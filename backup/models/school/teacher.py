"""
School Teacher Model

Teacher model for school system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backup.models.base import Base


class SchoolTeacher(Base):
    """
    School Teacher model for school system
    """
    __tablename__ = "school_teachers"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    phone = Column(String(20))
    department = Column(String(100))
    qualification = Column(String(255))
    specialization = Column(String(255))
    joining_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20), default="active")  # active, inactive, on_leave, retired
    
    # Relationships
    user = relationship("User", back_populates="school_teacher_profile")
    school_courses = relationship("SchoolCourse", back_populates="teacher")


# For backward compatibility - reference to existing teachers table
Teacher = SchoolTeacher
