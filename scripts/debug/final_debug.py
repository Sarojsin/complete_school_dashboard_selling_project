
from app.core.database import SessionLocal
from app.models.models import Student, User, Course, CourseEnrollment
from app.models.test_models import Test
import sys

def debug():
    db = SessionLocal()
    try:
        print("--- STUDENTS ---")
        students = db.query(Student).all()
        for s in students:
            print(f"Student ID: {s.id} | Name: {s.full_name} | Grade: '{s.grade_level}' | Section: '{s.section}'")
            courses = db.query(Course).join(CourseEnrollment).filter(CourseEnrollment.student_id == s.id).all()
            c_ids = [c.id for c in courses]
            print(f"  Enrolled Course IDs: {c_ids}")
            
        print("\n--- TESTS ---")
        tests = db.query(Test).all()
        for t in tests:
            print(f"Test ID: {t.id} | Title: '{t.title}' | CourseID: {t.course_id} | Grade Filter: '{t.grade_level}' | Section Filter: '{t.target_section}'")
    finally:
        db.close()

if __name__ == "__main__":
    debug()
