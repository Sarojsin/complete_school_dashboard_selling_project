import warnings
from sqlalchemy.exc import SAWarning

# Show all warnings
warnings.filterwarnings('always', category=SAWarning)

try:
    # Shared models
    from modules.shared import models as shared_models
    # School models
    from modules.school.school_teacher import models as teacher_models
    from modules.school.school_student import models as student_models
    from modules.school.school_parent import models as parent_models
    from modules.school.school_authority import models as authority_models
    from modules.school.school_classes import models as class_models
    from modules.school.school_subjects import models as subject_models
    from modules.school.school_courses import models as course_models
    from modules.school.school_assignments import models as assignment_models
    from modules.school.school_notes import models as note_models
    from modules.school.school_attendance import models as attendance_models
    # College models
    from modules.college.college_courses import models as college_course_models
    from modules.college.college_student import models as college_student_models
    from modules.college.college_faculty import models as college_faculty_models
    from modules.college.college_library import models as college_library_models
    from modules.college.college_hostel import models as college_hostel_models
    from modules.school.school_exam_section import models as exam_models
    from modules.school.school_timetable import models as timetable_models
    from modules.school.school_videos import models as video_models
    from modules.school.school_account_section import models as account_models
    from modules.school.school_library import models as library_models
    from modules.school.school_groups import models as group_models
    from modules.school.school_chat import models as chat_models
    from modules.school.school_notices import models as notice_models
    from modules.school.school_grades import models as grade_models
    from modules.school.school_tests import models as test_models
    from modules.school.school_dashboard import models as dashboard_models

    # Force configure mappers
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured without errors")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Exception:", type(e).__name__, e)
