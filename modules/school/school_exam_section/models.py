# School Exam Section Models
# ===========================

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func as sql_func
from datetime import datetime
from modules.shared.base import Base


class SchoolExamSchedule(Base):
    __tablename__ = "school_exam_schedules"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=False)
    subject = Column(String(200), nullable=False)
    exam_date = Column(Date, nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    total_marks = Column(Integer, default=100)
    passing_marks = Column(Integer, default=35)


class ExamGrade(Base):
    __tablename__ = "school_exam_grades"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("school_exam_schedules.id"), nullable=False)
    marks = Column(Integer, nullable=False)
    grade = Column(String(5), nullable=False)
    remarks = Column(String(500))


class ExamResult(Base):
    __tablename__ = "exam_results"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id"))
    course_id = Column(Integer, ForeignKey("school_courses.id"))
    marks = Column(Float)
    max_marks = Column(Float, default=100.0)
    grade = Column(String(2))
    exam_type = Column(String(20), default="final")
    is_published = Column(Boolean, default=True)
    published_by = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime, default=datetime.utcnow)
    semester = Column(String(10))


class ExamNotice(Base):
    __tablename__ = "exam_notices"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    notice_type = Column(String(20))  # schedule, hall_ticket, result
    exam_date = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

# For backward compatibility
ExamSchedules = SchoolExamSchedule
SchoolGrade = ExamGrade

__all__ = ["SchoolExamSchedule", "SchoolGrade", "ExamResult", "ExamNotice"]