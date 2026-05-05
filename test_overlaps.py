import warnings
warnings.simplefilter('ignore')
# Test imports
from modules.school.school_courses.models import SchoolCourse
from modules.school.school_assignments.models import Assignment
from modules.school.school_notes.models import Note
from modules.school.school_videos.models import Video
print("All imported OK")
# Check relationships
print("SchoolCourse.assignments overlaps:", getattr(SchoolCourse.assignments, 'overlaps', None))
print("Assignment.course overlaps:", getattr(Assignment.course, 'overlaps', None))
