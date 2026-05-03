"""
College Hostel Models

Models for hostel management - Hostel, Room, Allocation, Complaints.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class Hostel(Base):
    """Hostel building"""
    __tablename__ = "hostels"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    capacity = Column(Integer, default=0)
    warden_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    address = Column(Text)
    contact_number = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rooms = relationship("Room", back_populates="hostel")
    warden = relationship("Faculty", foreign_keys=[warden_id])
    complaints = relationship("HostelComplaint", back_populates="hostel")


class Room(Base):
    """Hostel room"""
    __tablename__ = "rooms"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(20), nullable=False)
    floor = Column(Integer, default=1)
    capacity = Column(Integer, default=2)
    occupied = Column(Integer, default=0)
    room_type = Column(String(50))  # single, double, triple
    amenities = Column(String(500))  # JSON string of amenities
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("HostelAllocation", back_populates="room")
    complaints = relationship("HostelComplaint", back_populates="room")


class HostelAllocation(Base):
    """Hostel room allocation to students"""
    __tablename__ = "hostel_allocations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    allocation_date = Column(DateTime, default=datetime.utcnow)
    vacate_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")  # active, vacated, transferred
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("CollegeStudent", back_populates="hostel_allocations")
    room = relationship("Room", back_populates="allocations")


class HostelComplaint(Base):
    """Student hostel complaint"""
    __tablename__ = "hostel_complaints"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="SET NULL"), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))  # maintenance, cleanliness, noise, etc.
    status = Column(String(20), default="pending")  # pending, in_progress, resolved, rejected
    resolved_by = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    hostel = relationship("Hostel", back_populates="complaints")
    room = relationship("Room", back_populates="complaints")