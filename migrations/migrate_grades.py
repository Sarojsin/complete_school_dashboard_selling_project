import os
import sys

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from database.database import SessionLocal
from app.models.models import Student, Course
from app.models.test_models import Test
from sqlalchemy import text


def migrate_grades():
    db = SessionLocal()
    try:
        # Prepend "Grade " to numeric grade levels
        # Students
        students = db.query(Student).all()
        for s in students:
            if s.grade_level and s.grade_level.isdigit():
                print(f"Updating Student {s.id}: '{s.grade_level}' -> 'Grade {s.grade_level}'")
                s.grade_level = f"Grade {s.grade_level}"

        # Courses
        courses = db.query(Course).all()
        for c in courses:
            if c.grade_level and c.grade_level.isdigit():
                print(f"Updating Course {c.id}: '{c.grade_level}' -> 'Grade {c.grade_level}'")
                c.grade_level = f"Grade {c.grade_level}"

        # Tests
        tests = db.query(Test).all()
        for t in tests:
            if t.grade_level and t.grade_level.isdigit():
                print(f"Updating Test {t.id}: '{t.grade_level}' -> 'Grade {t.grade_level}'")
                t.grade_level = f"Grade {t.grade_level}"
            elif t.grade_level == "None" or t.grade_level is None:
                # Try to infer from course if grade_level is missing in tests
                if t.course_id:
                    course = db.query(Course).get(t.course_id)
                    if course and course.grade_level:
                        target = course.grade_level
                        if target.isdigit():
                            target = f"Grade {target}"
                        print(f"Infilling Test {t.id} Grade from Course: -> '{target}'")
                        t.grade_level = target

        db.commit()
        print("Migration completed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Migration failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_grades()