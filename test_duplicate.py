import warnings
warnings.simplefilter('ignore')
try:
    from modules.college.college_courses import models as college_course_models
    print("Imported college_course_models")
    from backup.models.college import Department, Program, Faculty, CollegeStudent
    print("Imported backup Department successfully")
except Exception as e:
    print("Exception:", type(e).__name__, e)
