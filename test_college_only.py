import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)

try:
    # Only college models - no school models
    from modules.college.college_courses import models as college_course_mod
    print("Imported college_course")
    from modules.college.college_faculty import models as college_faculty_mod
    print("Imported college_faculty")
    from modules.college.college_student import models as college_student_mod
    print("Imported college_student")
    from modules.college.college_library import models as college_lib_mod
    print("Imported college_library")
    from modules.college.college_hostel import models as college_hostel_mod
    print("Imported college_hostel")
    from modules.college.college_lab import models as college_lab_mod
    print("Imported college_lab")
    from modules.college.college_placement import models as college_placement_mod
    print("Imported college_placement")
    from modules.college.college_research import models as college_research_mod
    print("Imported college_research")
    print("All college models imported")
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Exception:", type(e).__name__, e)
    import traceback
    traceback.print_exc()
