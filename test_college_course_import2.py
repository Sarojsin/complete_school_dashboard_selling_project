import warnings
from sqlalchemy.exc import SAWarning

# Only treat SAWarning as error, allow others
warnings.filterwarnings('error', category=SAWarning)

try:
    from modules.college.college_courses.models import CollegeCourse, Department, Semester, Program, Enrollment
    print("College models imported successfully")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Other exception:", type(e).__name__, e)
