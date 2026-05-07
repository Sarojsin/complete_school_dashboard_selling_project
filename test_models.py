#!/usr/bin/env python3

"""
Simple test to verify college models work
"""

from modules.college.models import CollegeFaculty, CollegeStudent

print("College models imported successfully!")
print(f"CollegeFaculty table: {CollegeFaculty.__tablename__}")
print(f"CollegeStudent table: {CollegeStudent.__tablename__}")