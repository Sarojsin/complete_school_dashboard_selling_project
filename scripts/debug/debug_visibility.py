
from app.core.database import SessionLocal
from app.models.models import Student, User, Course, CourseEnrollment
from app.models.test_models import Test
from datetime import datetime

def debug_deep():
    db = SessionLocal()
    try:
        now_val = datetime.now()
        print(f"Current Comparison Time (Local Now): {now_val}")
        
        print("\n--- STUDENTS ---")
        students = db.query(Student).all()
        for s in students:
            print(f"ID:{s.id} | G:'{s.grade_level}' | S:'{s.section}'")
            
        print("\n--- TESTS ---")
        tests = db.query(Test).all()
        for t in tests:
            start_ok = t.start_time <= now_val if t.start_time else "N/A"
            end_ok = t.end_time >= now_val if t.end_time else "N/A"
            print(f"Test ID: {t.id} | Title: '{t.title}'")
            print(f"  Target: Grade='{t.grade_level}', Section='{t.target_section}'")
            print(f"  Times: {t.start_time} TO {t.end_time}")
            print(f"  Active: {t.is_active} | StartOK: {start_ok} | EndOK: {end_ok}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_deep()
