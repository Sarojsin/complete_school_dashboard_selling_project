"""
College Placement Models

Models for placement management - Company, Job, Application.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class PlacementCompany(Base):
    """Company visiting for placements"""
    __tablename__ = "placement_companies"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    contact_person = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    jobs = relationship("PlacementJob", back_populates="company", cascade="all, delete-orphan")


class PlacementJob(Base):
    """Job opening at a company"""
    __tablename__ = "placement_jobs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("placement_companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    job_type = Column(String(50))  # full_time, part_time, internship
    location = Column(String(100))
    salary_min = Column(Float)
    salary_max = Column(Float)
    eligibility_criteria = Column(Text)
    deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("PlacementCompany", back_populates="jobs")
    applications = relationship("PlacementApplication", back_populates="job", cascade="all, delete-orphan")


class PlacementApplication(Base):
    """Student's application for a job"""
    __tablename__ = "placement_applications"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("placement_jobs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="applied")  # applied, shortlist, interview, selected, rejected
    applied_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    # Relationships
    student = relationship("CollegeStudent")
    job = relationship("PlacementJob", back_populates="applications")