
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from models.models import Course, Assignment, User, Teacher

def list_courses():
    db = SessionLocal()
    try:
        courses = db.query(Course).all()
        print(f"\nTotal Courses: {len(courses)}")
        if not courses:
            print("No courses found in database.")
            
        for c in courses:
            print(f"ID: {c.id}, Name: '{c.course_name}', Code: '{c.course_code}', Grade: '{c.grade_level}'")
            # Count assignments
            assignment_count = db.query(Assignment).filter(Assignment.course_id == c.id).count()
            print(f"   -> Assignments: {assignment_count}")
            
    finally:
        db.close()

if __name__ == "__main__":
    list_courses()
