"""
Models Package

Contains all database models for the application.
Uses the existing Base from core.database for backward compatibility.
"""

# Import Base from existing location
from backup.core.database import Base

# Import User and UserRole from existing models
from backup.models.models import User, UserRole

# School models
from backup.models.school import (
    SchoolStudent,
    SchoolTeacher,
    SchoolParent,
    SchoolAuthority,
    SchoolClass,
    SchoolFee,
)

# College models
from backup.models.college import (
    Department,
    Program,
    Semester,
    CollegeCourse,
    Faculty,
    CollegeStudent,
    Enrollment,
    CollegeFee,
    # Placements
    Company,
    Job,
    Application,
    PlacementDrive,
    # Research
    ResearchProject,
    Publication,
    Patent,
    # Hostels
    Hostel,
    Room,
    HostelAllocation,
    HostelComplaint,
    # Labs
    Lab,
    LabEquipment,
    LabSchedule,
)

# Re-export for backward compatibility
# These aliases allow existing code to continue working
Student = SchoolStudent
Teacher = SchoolTeacher
Parent = SchoolParent
Authority = SchoolAuthority
SchoolClass = SchoolClass
FeeStructure = SchoolFee

# College exports
Course = CollegeCourse
FeeRecord = CollegeFee

__all__ = [
    # Base
    "Base",
    # User
    "User",
    "UserRole",
    # School models
    "SchoolStudent",
    "SchoolTeacher", 
    "SchoolParent",
    "SchoolAuthority",
    "SchoolClass",
    "SchoolFee",
    # College models
    "Department",
    "Program", 
    "Semester",
    "CollegeCourse",
    "Faculty",
    "CollegeStudent",
    "Enrollment",
    "CollegeFee",
    # Placements
    "Company",
    "Job",
    "Application",
    "PlacementDrive",
    # Research
    "ResearchProject",
    "Publication",
    "Patent",
    # Hostels
    "Hostel",
    "Room",
    "HostelAllocation",
    "HostelComplaint",
    # Labs
    "Lab",
    "LabEquipment",
    "LabSchedule",
    # Backward compatibility aliases
    "Student",
    "Teacher",
    "Parent", 
    "Authority",
    "Course",
    "FeeStructure",
    "FeeRecord",
]
