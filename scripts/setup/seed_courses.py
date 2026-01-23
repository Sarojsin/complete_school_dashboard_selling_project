
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
# Import ALL models to ensure mapper registry is populated and relationships work
from models.models import *

def seed_courses():
    db = SessionLocal()
    try:
        # Get a teacher to assign (using the first available teacher)
        teacher = db.query(Teacher).first()
        if not teacher:
            print("Error: No teachers found in database. Cannot create courses.")
            return

        print(f"Assigning new courses to teacher: {teacher.user.full_name if teacher.user else 'Unknown'} (ID: {teacher.id})")

        new_courses = [
            {"name": "English", "code": "ENG101", "grade": "9", "desc": "English Literature and Language"},
            {"name": "Physics", "code": "PHY101", "grade": "10", "desc": "Fundamentals of Physics"},
            {"name": "Computer Science", "code": "CS101", "grade": "9", "desc": "Introduction to Computer Science"},
            {"name": "Mathematics", "code": "MATH101", "grade": "9", "desc": "General Mathematics"},
            {"name": "History", "code": "HIST101", "grade": "10", "desc": "World History"}
        ]

        for course_data in new_courses:
            # Check if course exists to avoid duplicates (checking by code)
            exists = db.query(Course).filter(Course.course_code == course_data["code"]).first()
            if exists:
                print(f"Skipping {course_data['name']} (Code: {course_data['code']}) - Already exists")
                continue

            course = Course(
                course_name=course_data["name"],
                course_code=course_data["code"],
                grade_level=course_data["grade"],
                description=course_data["desc"],
                teacher_id=teacher.id
            )
            db.add(course)
            print(f"Adding course: {course_data['name']}")

        db.commit()
        print("Courses seeded successfully!")

    except Exception as e:
        print(f"Error seeding courses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()
