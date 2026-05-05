import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)  # Ignore Pydantic

try:
    # Import all school models in proper order
    from modules.school.school_teacher import models as teacher_mod
    from modules.school.school_student import models as student_mod
    from modules.school.school_parent import models as parent_mod
    from modules.school.school_classes import models as class_mod
    from modules.school.school_subjects import models as subject_mod
    from modules.school.school_courses import models as course_mod
    from modules.school.school_assignments import models as assign_mod
    from modules.school.school_notes import models as notes_mod
    from modules.school.school_videos import models as videos_mod
    from modules.school.school_attendance import models as attend_mod
    # Also import other modules that define relationships to these
    from modules.school.school_grades import models as grades_mod
    from modules.school.school_tests import models as tests_mod
    print("All core school models imported")
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured successfully - no overlapping warnings")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Exception:", type(e).__name__, e)
