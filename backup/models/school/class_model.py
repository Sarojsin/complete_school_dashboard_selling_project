"""
School Class Model

Class/Grade model for school system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backup.models.base import Base


class SchoolClass(Base):
    """
    School Class model (Class 1-12 with sections)
    """
    __tablename__ = "school_classes"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))  # "Class 1", "Class 10"
    section = Column(String(10))  # "A", "B"
    class_teacher_id = Column(Integer, ForeignKey("school_teachers.id"), nullable=True)
    academic_year = Column(String(20))
    
    # Relationships
    class_teacher = relationship("SchoolTeacher", back_populates="school_classes")
    students = relationship("SchoolStudent", back_populates="school_class")


# For backward compatibility - reference
SchoolClass = SchoolClass
