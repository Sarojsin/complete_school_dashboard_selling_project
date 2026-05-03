"""
College Hostel Models
====================
Models for hostel management.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase
from datetime import datetime


class Hostel(CollegeBase):
    """Hostel building"""
    __tablename__ = "hostels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    capacity = Column(Integer, default=0)
    warden_id = Column(Integer, ForeignKey("faculty.id"))
    address = Column(Text)
    contact_number = Column(String(20))
    email = Column(String(100))
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    rooms = relationship("Room", back_populates="hostel")
    warden = relationship("Faculty", foreign_keys=[warden_id])


class Room(CollegeBase):
    """Hostel room"""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False)
    room_number = Column(String(20), nullable=False)
    floor = Column(Integer, default=1)
    capacity = Column(Integer, default=2)
    occupied = Column(Integer, default=0)
    room_type = Column(String(50))  # single, double, triple
    amenities = Column(String(500))  # JSON string of amenities
    is_available = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("HostelAllocation", back_populates="room")


class HostelAllocation(CollegeBase):
    """Hostel room allocation to students"""
    __tablename__ = "hostel_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    allocation_date = Column(Date, default=datetime.utcnow)
    vacate_date = Column(Date)
    status = Column(String(20), default="active")  # active, vacated, transferred
    created_at = Column(Date, default=datetime.utcnow)
    
    # Relationships
    student = relationship("CollegeStudent", back_populates="hostel_allocations")
    room = relationship("Room", back_populates="allocations")


class HostelComplaint(CollegeBase):
    """Student hostel complaint"""
    __tablename__ = "hostel_complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id"), nullable=False)
    hostel_id = Column(Integer, ForeignKey("hostels.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))  # maintenance, cleanliness, noise, etc.
    status = Column(String(20), default="pending")  # pending, in_progress, resolved, rejected
    resolved_by = Column(Integer, ForeignKey("faculty.id"))
    resolved_at = Column(Date)
    created_at = Column(Date, default=datetime.utcnow)
