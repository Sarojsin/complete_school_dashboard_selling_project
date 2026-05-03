"""
College Models Package

Contains college-specific models (Department, Program, Semester, Course, Faculty, Student, Enrollment, Fee, Placement, Research, Hostel).
"""

from .department import Department
from .program import Program
from .semester import Semester
from .course import CollegeCourse
from .faculty import Faculty
from .student import CollegeStudent
from .enrollment import Enrollment
from .fee import CollegeFee

# Placement models
from .placement import Company, Job, Application, PlacementDrive

# Research models
from .research import ResearchProject, Publication, Patent

# Hostel models
from .hostel import Hostel, Room, HostelAllocation, HostelComplaint

# Lab models
from .lab import Lab, LabEquipment, LabSchedule

__all__ = [
    "Department",
    "Program",
    "Semester", 
    "CollegeCourse",
    "Faculty",
    "CollegeStudent",
    "Enrollment",
    "CollegeFee",
    # Placement
    "Company",
    "Job", 
    "Application",
    "PlacementDrive",
    # Research
    "ResearchProject",
    "Publication",
    "Patent",
    # Hostel
    "Hostel",
    "Room",
    "HostelAllocation",
    "HostelComplaint",
    # Lab
    "Lab",
    "LabEquipment",
    "LabSchedule",
]
