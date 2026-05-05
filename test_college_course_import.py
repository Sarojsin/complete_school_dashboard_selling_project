import warnings
warnings.simplefilter('error')
from sqlalchemy.exc import SAWarning

try:
    from modules.college.college_courses.models import CollegeCourse, Department, Semester, Program, Enrollment
    print("College models imported successfully")
except SAWarning as e:
    print("SAWarning:", e)
except Exception as e:
    print("Exception:", type(e).__name__, e)
    import traceback
    traceback.print_exc()
