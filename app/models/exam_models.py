from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .models import Base

class ExamResult(Base):
    __tablename__ = "exam_results"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    marks = Column(Float)
    grade = Column(String(2))
    published_by = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime, default=datetime.utcnow)
    semester = Column(String(10))
    
    # Relationships
    student = relationship("Student", back_populates="exam_results")
    course = relationship("Course")
    publisher = relationship("User")
