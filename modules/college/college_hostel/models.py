"""
College Hostel Models

Models for hostel management - Hostel, Room, Allocation, Complaint.
All models are imported from backup.models.college.hostel for single source of truth.
"""

from backup.models.college.hostel import Hostel, Room, HostelAllocation, HostelComplaint

__all__ = ["Hostel", "Room", "HostelAllocation", "HostelComplaint"]
