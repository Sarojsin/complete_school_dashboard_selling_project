"""
Semester Model

Semester model for college system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase


class Semester(CollegeBase):
    """
    Semester model for college
    """
    __tablename__ = "college_semesters"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))  # "Fall 2024", "Spring 2025"
    program_id = Column(Integer, ForeignKey("college_programs.id"))
    number = Column(Integer)  # 1, 2, 3, 4...
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    
    # Relationships
    program = relationship("Program", back_populates="semesters")
    courses = relationship("CollegeCourse", back_populates="semester")
