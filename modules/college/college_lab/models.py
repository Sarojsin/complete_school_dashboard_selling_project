"""
College Lab Models

Models for lab management - Lab, Equipment, Schedule.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class Lab(Base):
    """Laboratory"""
    __tablename__ = "labs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    location = Column(String(100))
    capacity = Column(Integer, default=30)
    description = Column(Text)
    in_charge_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="labs")
    in_charge = relationship("Faculty", foreign_keys=[in_charge_id])
    equipment = relationship("LabEquipment", back_populates="lab", cascade="all, delete-orphan")
    schedules = relationship("LabSchedule", back_populates="lab", cascade="all, delete-orphan")


class LabEquipment(Base):
    """Lab equipment"""
    __tablename__ = "lab_equipment"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    serial_number = Column(String(100))
    quantity = Column(Integer, default=1)
    status = Column(String(50), default="working")  # working, maintenance, broken
    purchase_date = Column(DateTime)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lab = relationship("Lab", back_populates="equipment")


class LabSchedule(Base):
    """Lab schedule for practical sessions"""
    __tablename__ = "lab_schedules"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id", ondelete="SET NULL"), nullable=True)
    day_of_week = Column(String(10))  # Monday, Tuesday, etc.
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lab = relationship("Lab", back_populates="schedules")