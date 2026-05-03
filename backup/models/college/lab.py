"""
College Lab Models
=================
Laboratory related models for college.
"""
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase

class Lab(CollegeBase):
    """Laboratory model"""
    __tablename__ = "college_labs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("college_departments.id"), nullable=False)
    capacity = Column(Integer, default=30)
    location = Column(String(100))
    equipment_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    department = relationship("Department", back_populates="labs")
    equipment = relationship("LabEquipment", back_populates="lab")
    schedules = relationship("LabSchedule", back_populates="lab")


class LabEquipment(CollegeBase):
    """Lab equipment inventory"""
    __tablename__ = "lab_equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("college_labs.id"), nullable=False)
    name = Column(String(200), nullable=False)
    serial_number = Column(String(100))
    quantity = Column(Integer, default=1)
    purchase_date = Column(Date)
    condition = Column(String(50), default="good")  # good, needs_repair, broken
    notes = Column(Text)
    
    # Relationships
    lab = relationship("Lab", back_populates="equipment")


class LabSchedule(CollegeBase):
    """Lab timetable/booking schedule"""
    __tablename__ = "lab_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("college_labs.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id"))
    faculty_id = Column(Integer, ForeignKey("college_faculty.id"))
    day_of_week = Column(String(20))  # monday, tuesday, etc.
    start_time = Column(String(10))   # HH:MM format
    end_time = Column(String(10))
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    lab = relationship("Lab", back_populates="schedules")
