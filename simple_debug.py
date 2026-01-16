
from database.database import SessionLocal
from models.models import Student, User, Course, CourseEnrollment
from models.test_models import Test

def debug():
    db = SessionLocal()
    try:
        print("--- STUDENTS ---")
        students = db.query(Student).all()
        for s in students:
            print(f"S_ID:{s.id}|G:'{s.grade_level}'|S:'{s.section}'")
    finally:
        db.close()

if __name__ == "__main__":
    debug()
