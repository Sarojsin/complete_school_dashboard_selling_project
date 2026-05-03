"""
Batch update all college models to use CollegeBase instead of backup.base.Base
"""

import os
import re

college_models_dir = r"C:\Users\U S E R\Desktop\claud_sc\backup\models\college"

files_to_update = [
    "student.py",
    "faculty.py",
    "course.py",
    "department.py",
    "enrollment.py",
    "fee.py",
    "hostel.py",
    "lab.py",
    "placement.py",
    "program.py",
    "research.py",
    "semester.py",
]

for filename in files_to_update:
    filepath = os.path.join(college_models_dir, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} - file not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace base import
    content = content.replace(
        "from backup.models.base import Base",
        "from modules.college.base import CollegeBase"
    )
    
    # Replace class inheritance: class X(Base): → class X(CollegeBase):
    # Use regex to match class definitions inheriting from Base
    content = re.sub(
        r'class (\w+)\(Base\):',
        r'class \1(CollegeBase):',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  [UPDATED] {filename}")

print("\nAll college models updated to use CollegeBase!")
