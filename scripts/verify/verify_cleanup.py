
from backup.core.database import SessionLocal
from backup.models.models import Student
from backup.models.test_models import Test
from backup.repositories.test_repository import TestRepository

def verify_cleanup():
    db = SessionLocal()
    try:
        print("Checking Test model...")
        test = db.query(Test).first()
        if test:
            print(f"Found Test: {test.title}")
            try:
                print(f"Course ID: {test.course_id}")
            except AttributeError:
                print("Confirmed: 'course_id' attribute is GONE from Test model.")
        
        print("\nChecking available tests for student...")
        # Get a real student
        student = db.query(Student).first()
        if student:
            tests = TestRepository.get_available_tests_for_student(
                db, 
                student.id, 
                section=student.section, 
                grade_level=student.grade_level
            )
            print(f"Found {len(tests)} tests for student {student.id} ({student.grade_level} {student.section})")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_cleanup()
