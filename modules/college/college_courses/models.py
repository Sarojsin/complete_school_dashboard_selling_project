"""
College Course Model

Course model for college system (with credits).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class CollegeCourse(Base):
    """
    Course model for college (with credits)
    """
    __tablename__ = "college_courses"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20))  # e.g., "CS101"
    name = Column(String(255))
    description = Column(Text)
    credits = Column(Integer, default=3)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    instructor_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    is_elective = Column(Boolean, default=False)
    max_students = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="courses")
    semester = relationship("Semester", back_populates="courses")
    instructor = relationship("Faculty", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


class Department(Base):
    """
    Department model for college system
    """
    __tablename__ = "college_departments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    code = Column(String(20), unique=True)
    hod_teacher_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL", use_alter=True, name="fk_dept_hod"), nullable=True)
    description = Column(Text)
    
    # Relationships
    hod = relationship("Faculty", back_populates="department_hod", foreign_keys=[hod_teacher_id])
    faculty = relationship("Faculty", back_populates="department", foreign_keys="[Faculty.department_id]")
    programs = relationship("Program", back_populates="department")
    courses = relationship("CollegeCourse", back_populates="department")


class Program(Base):
    """
    Program/Degree model for college (e.g., BSc CS, BSc IT, MBA)
    """
    __tablename__ = "college_programs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # "Bachelor of Computer Science"
    code = Column(String(20))  # "BCS"
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    level = Column(String(50))  # "Bachelor", "Master", "PhD"
    duration_years = Column(Integer)
    total_credits = Column(Integer)
    
    # Relationships
    department = relationship("Department", back_populates="programs")
    semesters = relationship("Semester", back_populates="program")
    students = relationship("CollegeStudent", back_populates="program")


class Semester(Base):
    """
    Semester model for college
    """
    __tablename__ = "college_semesters"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))  # "Fall 2024", "Spring 2025"
    program_id = Column(Integer, ForeignKey("college_programs.id", ondelete="SET NULL"), nullable=True)
    number = Column(Integer)  # 1, 2, 3, 4...
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)
    
    # Relationships
    program = relationship("Program", back_populates="semesters")
    courses = relationship("CollegeCourse", back_populates="semester")
    students = relationship("CollegeStudent", back_populates="semester")
    enrollments = relationship("Enrollment", back_populates="semester")


class Enrollment(Base):
    """
    Course Enrollment model for college
    """
    __tablename__ = "college_enrollments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="enrolled")  # enrolled, completed, dropped
    grade = Column(String(5), nullable=True)
    grade_points = Column(Float, nullable=True)
    
    # Relationships
    student = relationship("CollegeStudent", back_populates="enrollments")
    course = relationship("CollegeCourse", back_populates="enrollments")
    semester = relationship("Semester", back_populates="enrollments")