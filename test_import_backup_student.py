import sys
# In a fresh python process, import backup.models.college.student alone
print("Before import:", [k for k in sys.modules if 'backup' in k])
from backup.models.college.student import CollegeStudent
print("After import:", [k for k in sys.modules if 'backup' in k and 'student' in k.lower()])
