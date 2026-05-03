"""
College Research Models

Models for research management - ResearchProject, ResearchPublication, ResearchPatent.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class ResearchProject(Base):
    """Research project"""
    __tablename__ = "research_projects"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    principal_investigator_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    co_investigators = Column(Text)  # JSON array of faculty IDs
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    funding_amount = Column(String(100))
    funding_agency = Column(String(200))
    status = Column(String(50), default="ongoing")  # ongoing, completed, suspended
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    principal_investigator = relationship("Faculty")


class ResearchPublication(Base):
    """Research publication"""
    __tablename__ = "research_publications"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    authors = Column(Text)  # JSON array of author names
    journal_name = Column(String(200))
    publication_date = Column(DateTime)
    volume = Column(String(50))
    issue = Column(String(50))
    pages = Column(String(50))
    doi = Column(String(100))
    abstract = Column(Text)
    faculty_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    faculty = relationship("Faculty")


class ResearchPatent(Base):
    """Research patent"""
    __tablename__ = "research_patents"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    inventors = Column(Text)  # JSON array of inventor names
    patent_number = Column(String(100))
    filing_date = Column(DateTime)
    grant_date = Column(DateTime)
    status = Column(String(50), default="filed")  # filed, granted, expired
    description = Column(Text)
    faculty_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    faculty = relationship("Faculty")