"""
College Research Models
======================
Models for research projects and publications.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase
from datetime import datetime


class ResearchProject(CollegeBase):
    """Research project"""
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    principal_investigator_id = Column(Integer, ForeignKey("faculty.id"))
    co_investigators = Column(JSON)  # List of faculty IDs
    funding_amount = Column(Integer)
    funding_agency = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50), default="ongoing")  # ongoing, completed, suspended
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    pi = relationship("Faculty", foreign_keys=[principal_investigator_id])


class Publication(CollegeBase):
    """Academic publication"""
    __tablename__ = "publications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    authors = Column(JSON)  # List of author names
    journal = Column(String(200))
    conference = Column(String(200))
    publication_date = Column(Date)
    doi = Column(String(100))
    abstract = Column(Text)
    citation_count = Column(Integer, default=0)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    research_project_id = Column(Integer, ForeignKey("research_projects.id"))
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    faculty = relationship("Faculty")


class Patent(CollegeBase):
    """Patent record"""
    __tablename__ = "patents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    inventors = Column(JSON)  # List of inventor names
    patent_number = Column(String(50))
    filing_date = Column(Date)
    grant_date = Column(Date)
    status = Column(String(50))  # filed, granted, expired
    description = Column(Text)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    created_at = Column(Date, default=datetime.utcnow)
