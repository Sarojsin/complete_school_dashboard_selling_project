"""
Enrollment Model

Course enrollment model for college system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase


class Enrollment(CollegeBase):
    """
    Course Enrollment model for college
    """
    __tablename__ = "college_enrollments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    enrollment_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20))  # enrolled, completed, dropped
    grade = Column(String(5))
    grade_points = Column(Float)
    
    # Relationships
    student = relationship("CollegeStudent", back_populates="enrollments")
    course = relationship("CollegeCourse", back_populates="enrollments")
    semester = relationship("Semester")
