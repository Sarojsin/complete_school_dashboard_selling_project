# Add imports
from .department_models import Department
from .exam_models import ExamResult
from .library_models import BookLoan
from .account_models import TeacherPayment

__all__ = [
    # ... existing imports
    "Department",
    "ExamResult", 
    "BookLoan",
    "TeacherPayment",
]