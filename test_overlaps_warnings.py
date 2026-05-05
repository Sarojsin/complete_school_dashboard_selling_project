import warnings
warnings.filterwarnings('error', category=DeprecationWarning)  # ignore Pydantic
warnings.filterwarnings('always', category=DeprecationWarning)  # but allow others
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)

try:
    # Import all modules
    from modules.school.school_courses import models as school_course_mod
    from modules.school.school_assignments import models as assign_mod
    from modules.school.school_notes import models as notes_mod
    from modules.school.school_videos import models as videos_mod
    print("School models with overlaps imported successfully")
    # Force configure
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("Mappers configured successfully")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Other exception:", type(e).__name__, e)
