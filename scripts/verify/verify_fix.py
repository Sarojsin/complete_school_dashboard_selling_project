from database.database import SessionLocal
from repositories.student_repository import StudentRepository

def verify_fix():
    db = SessionLocal()
    try:
        print("Testing StudentRepository.get_all with filters:")
        # Test 1: Grade 10, Section A (User's case)
        students = StudentRepository.get_all(db, grade_level="10", section="A")
        print(f"Grade 10, Section A: {len(students)} students found")
        for s in students:
            print(f" - {s.user.full_name} ({s.grade_level}-{s.section})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_fix()
