"""
College Placement Models
=======================
Models for campus placement system.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase
from datetime import datetime


class Company(CollegeBase):
    """Company visiting for campus placements"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    logo = Column(String(200))
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    jobs = relationship("Job", back_populates="company")


class Job(CollegeBase):
    """Job posting from a company"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    location = Column(String(100))
    job_type = Column(String(50))  # full-time, internship
    deadline = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Application(CollegeBase):
    """Student job application"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("college_students.id"), nullable=False)
    applied_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20), default="applied")  # applied, shortlisted, rejected, selected
    resume = Column(String(200))
    cover_letter = Column(Text)
    notes = Column(Text)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    student = relationship("CollegeStudent", back_populates="applications")


class PlacementDrive(CollegeBase):
    """Placement drive/event"""
    __tablename__ = "placement_drives"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.utcnow)
