
from database.database import SessionLocal
from app.models.models import Student, User, Course, CourseEnrollment
from app.models.test_models import Test
import sys

def debug_enrollments():
    db = SessionLocal()
    try:
        print("--- ALL STUDENTS ---")
        students = db.query(Student).all()
        for s in students:
            print(f"ID: {s.id}, Name: {s.full_name}, Grade: '{s.grade_level}', Section: '{s.section}'")
            
        print("\n--- ENROLLMENTS FOR COURSE 1 ---")
        enrolls = db.query(CourseEnrollment).filter(CourseEnrollment.course_id == 1).all()
        for e in enrolls:
            s = db.query(Student).get(e.student_id)
            print(f"Student {s.id} ({s.full_name}) is enrolled in Course 1")

        print("\n--- COURSE 1 INFO ---")
        c = db.query(Course).get(1)
        if c:
            print(f"Course 1: '{c.course_name}', Grade: '{c.grade_level}'")
        else:
            print("Course 1 NOT FOUND")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_enrollments()
