"""
College Course Model

Course model for college system (with credits).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase


class CollegeCourse(CollegeBase):
    """
    Course model for college (with credits)
    """
    __tablename__ = "college_courses"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20))  # e.g., "CS101"
    name = Column(String(255))
    description = Column(Text)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("college_departments.id"))
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    instructor_id = Column(Integer, ForeignKey("college_faculty.id"))
    is_elective = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department = relationship("Department")
    semester = relationship("Semester", back_populates="courses")
    instructor = relationship("Faculty")
    enrollments = relationship("Enrollment", back_populates="course")
