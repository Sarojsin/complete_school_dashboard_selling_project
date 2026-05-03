from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base
from modules.school.school_classes.models import SchoolClass
from modules.school.school_subjects.models import SchoolSubject
from modules.school.school_teacher.models import Teacher
from modules.school.school_student.models import SchoolStudent


class SchoolCourse(Base):
    __tablename__ = "school_courses"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(50), unique=True, nullable=False, index=True)
    course_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    subject_id = Column(Integer, ForeignKey("school_subjects.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    semester = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teacher = relationship(Teacher)
    class_obj = relationship(SchoolClass)
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", cascade="all, delete-orphan")
    notes = relationship("Note", cascade="all, delete-orphan")
    videos = relationship("Video", cascade="all, delete-orphan")


class CourseEnrollment(Base):
    __tablename__ = "school_course_enrollments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(Date, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    student = relationship("SchoolStudent")
    course = relationship("SchoolCourse", back_populates="enrollments")