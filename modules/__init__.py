"""
Top-Level Modules Package

This is the new modular architecture for the school/college management system.
Each submodule represents a domain-specific module with its own models, schemas,
repository, service, API, and web routes.

Modules:
- shared: Core infrastructure (config, database, auth, base models)
- school_authority: School administration
- school_teacher: Teacher management
- school_student: Student management
- school_parent: Parent Portal
- school_exam_section: Exam management
- school_account_section: Finance & Fees
- school_library: Library management
- school_attendance: School attendance
- college_faculty: College faculty
- college_student: College students
- college_library: College library
- college_hod: Department heads
- college_registrar: Registrations & programs
- college_exam_section: College exams
- college_account_section: College finance
- college_library: College library
- college_placement: Placement cell
- college_research: Research projects
- college_hostel: Hostel management
- college_lab: Laboratory management
- college_dean: Dean oversight
"""

__version__ = "2.0.0"

# Import all module routers for easy access
# School modules
# School modules
from modules.school.school_teacher import router as school_teacher_router
# from modules.school_authority import router as school_authority_router
from modules.school.school_student import router as school_student_router
# ... other school modules commented out for POC
# College modules
# ... all college modules commented out for POC

__all__ = [
    # Version
    "__version__",
    # School routers
    # "school_authority_router",
    "school_teacher_router",
    "school_student_router",
    # "school_parent_router",
    # "school_exam_section_router",
    # "school_account_section_router",
    # "school_library_router",
    # "school_attendance_router",
    # College routers
    # "college_dean_router",
    # "college_hod_router",
    # "college_registrar_router",
    # "college_exam_section_router",
    # "college_account_section_router",
    # "college_placement_router",
    # "college_research_router",
    # "college_hostel_router",
    # "college_lab_router",
    # "college_faculty_router",
    # "college_student_router",
    # "college_library_router",
]
