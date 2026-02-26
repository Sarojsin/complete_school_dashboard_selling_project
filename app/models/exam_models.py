from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, Text, Boolean
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
    max_marks = Column(Float, default=100.0)          # NEW
    grade = Column(String(2))
    exam_type = Column(String(20), default="final")    # NEW: midterm, final, quiz
    is_published = Column(Boolean, default=True)       # NEW
    published_by = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime, default=datetime.utcnow)
    semester = Column(String(10))
    
    # Relationships
    student = relationship("Student", back_populates="exam_results")
    course = relationship("Course")
    publisher = relationship("User")

class ExamNotice(Base):                                # NEW MODEL
    __tablename__ = "exam_notices"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    notice_type = Column(String(20))  # schedule, hall_ticket, result
    exam_date = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    creator = relationship("User")
