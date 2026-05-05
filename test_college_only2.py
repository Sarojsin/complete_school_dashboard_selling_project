import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)

# Import in order
print("Importing college courses models...")
from modules.college.college_courses import models as college_course_mod
print("Importing college faculty models...")
from modules.college.college_faculty import models as college_faculty_mod
print("Importing college student models...")
from modules.college.college_student import models as college_student_mod
print("Importing college library models...")
from modules.college.college_library import models as college_lib_mod
print("Importing college hostel models...")
from modules.college.college_hostel import models as college_hostel_mod
print("Importing college lab models...")
from modules.college.college_lab import models as college_lab_mod
print("Importing college placement models...")
from modules.college.college_placement import models as college_placement_mod
print("Importing college research models...")
from modules.college.college_research import models as college_research_mod
print("All college model modules imported")
# check if old Student is loaded
import sys
mods = [m for m in sys.modules.keys() if 'backup' in m.lower() and 'student' in m.lower()]
print("Backup student modules loaded:", mods)
# configure mappers
from sqlalchemy.orm import configure_mappers
configure_mappers()
print("College mappers configured successfully - no SAWarnings")
