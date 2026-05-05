import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)

try:
    from modules.college.base import CollegeBase
    # Force configure mappers
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured successfully")
except SAWarning as e:
    print("SAWarning during configure:", e)
except Exception as e:
    print("Exception during configure:", type(e).__name__, e)
    import traceback
    traceback.print_exc()

# Also try to import all models to ensure they register
try:
    import modules.college.college_courses.models as cmod
    import modules.college.college_student.models as csmod
    import modules.college.college_faculty.models as cfmod
    print("All college model modules imported")
except SAWarning as e:
    print("SAWarning on import:", e)
except Exception as e:
    print("Exception on import:", type(e).__name__, e)
