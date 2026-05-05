import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

try:
    # College models
    from modules.college.college_courses import models as college_course_mod
    from modules.college.college_student import models as college_student_mod
    from modules.college.college_faculty import models as college_faculty_mod
    from modules.college.college_library import models as college_lib_mod
    from modules.college.college_hostel import models as college_hostel_mod
    from modules.college.college_lab import models as college_lab_mod
    from modules.college.college_placement import models as college_placement_mod
    from modules.college.college_research import models as college_research_mod
    print("All college model modules imported")
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("College mappers configured successfully - no SAWarnings")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Exception:", type(e).__name__, e)
