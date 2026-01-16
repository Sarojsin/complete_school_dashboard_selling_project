
from database.database import SessionLocal
from models.models import Student, User, Course, CourseEnrollment
from models.test_models import Test
import sys

def debug_student_tests():
    db = SessionLocal()
    try:
        print("--- STUDENTS ---")
        students = db.query(Student).all()
        for s in students:
            print(f"Student ID: {s.id}")
            print(f"  Name: {s.full_name}")
            print(f"  Grade: '{s.grade_level}'")
            print(f"  Section: '{s.section}'")
            enrollments = db.query(CourseEnrollment).filter(CourseEnrollment.student_id == s.id).all()
            if enrollments:
                for e in enrollments:
                    c = db.query(Course).get(e.course_id)
                    if c:
                        print(f"  - Enrolled in Course ID {c.id}: '{c.course_name}' (Grade: '{c.grade_level}')")
                    else:
                        print(f"  - Enrolled in Course ID {e.course_id} (NOT FOUND)")
            else:
                print("  - NO ENROLLMENTS FOUND")
        
        print("\n--- TESTS ---")
        tests = db.query(Test).all()
        for t in tests:
            print(f"Test ID: {t.id}")
            print(f"  Title: '{t.title}'")
            print(f"  Course ID: {t.course_id}")
            print(f"  Grade Level Filter: '{t.grade_level}'")
            print(f"  Target Section: '{t.target_section}'")
            print(f"  Active: {t.is_active}")
            print(f"  Window: {t.start_time} TO {t.end_time}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_student_tests()
