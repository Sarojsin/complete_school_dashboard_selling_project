"""
Import all college models and create tables in college database.
"""

import sys
import importlib

# List all college model modules to import
college_modules = [
    'backup.models.college.student',
    'backup.models.college.faculty',
    'backup.models.college.course',
    'backup.models.college.department',
    'backup.models.college.enrollment',
    'backup.models.college.fee',
    'backup.models.college.hostel',
    'backup.models.college.lab',
    'backup.models.college.placement',
    'backup.models.college.program',
    'backup.models.college.research',
    'backup.models.college.semester',
]

print("Importing college models...")
for mod in college_modules:
    try:
        importlib.import_module(mod)
        print(f"  [OK] {mod}")
    except Exception as e:
        print(f"  [ERROR] {mod}: {e}")

# Now create tables
from modules.college.database import create_college_tables

print("\nCreating tables in college_sell_db...")
create_college_tables()
