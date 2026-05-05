import warnings
warnings.simplefilter('ignore')
from modules.college.college_courses.models import Department as NewDepartment
print("New Department loaded:", NewDepartment, NewDepartment.__tablename__)
from backup.models.college import Department as BackupDepartment
print("Backup Department loaded:", BackupDepartment, BackupDepartment.__tablename__)
# Check if they are same class
print("Are they same class?", NewDepartment is BackupDepartment)
# Check mapper
from sqlalchemy.orm import mapper
print("New mappers:", NewDepartment.__mapper__)
print("Backup mappers:", BackupDepartment.__mapper__)
