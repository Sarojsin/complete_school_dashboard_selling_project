from sqlalchemy.exc import SAWarning
import warnings
warnings.simplefilter('error', SAWarning)

try:
    from backup.models.college.faculty import Faculty
    print("Faculty imported successfully")
except SAWarning as e:
    print("SAWarning:", e)
except Exception as e:
    print("Exception:", e)
