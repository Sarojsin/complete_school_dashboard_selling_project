from database.database import SessionLocal
from repositories.teacher_repository import TeacherRepository
from models.models import Teacher, User, Course, Student, CourseEnrollment

def debug_teacher_filter():
    db = SessionLocal()
    try:
        # Create a mock scenario if needed, or search for existing
        # Find a teacher
        teacher = db.query(Teacher).first()
        if not teacher:
            print("No teacher found.")
            return

        print(f"Teacher: {teacher.full_name} (ID: {teacher.id})")
        
        # Check actual students attached to this teacher via courses
        all_students = TeacherRepository.get_my_students(db, teacher.id)
        print(f"Total enrolled students: {len(all_students)}")
        
        if not all_students:
            print("Teacher has no students. Cannot verify filtering.")
            # Let's try to find *any* student and see their grade
            s = db.query(Student).first()
            if s:
                print(f"Sample Student in DB: {s.full_name}, Grade: '{s.grade_level}', Section: '{s.section}'")
            return

        for s in all_students:
            print(f" - Student: {s.user.full_name}, Grade: '{s.grade_level}', Section: '{s.section}'")

        # Now simulate the failed filter
        # User said: grade=10, section=A
        print("\n--- Testing Filter: grade='10', section='A' ---")
        filtered = TeacherRepository.get_my_students(db, teacher.id, grade="10", section="A")
        print(f"Filtered count: {len(filtered)}")
        for s in filtered:
            print(f" - P: {s.user.full_name} ({s.grade_level}-{s.section})")
            
        # Debug: Check if there ARE any 10-A students associated?
        # Maybe the data in DB is "Grade 10" not "10"?
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_teacher_filter()
