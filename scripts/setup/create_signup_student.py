from database.database import SessionLocal
from models.models import User, Student, UserRole
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository

db = SessionLocal()

try:
    # Create student user
    username = "student_signup_verify"
    existing = UserRepository.get_by_username(db, username)
    if not existing:
        student_user = UserRepository.create(
            db=db,
            email="signup_verify@school.com",
            username=username,
            password="Student123",
            full_name="Signup Verify Student",
            role=UserRole.STUDENT
        )
        
        # Create student profile
        student_profile_data = {
            "user_id": student_user.id,
            "student_id": "TEST_SIGNUP_1",
            "grade_level": "10",
            "section": "B"
        }
        student = StudentRepository.create(db, student_profile_data)
        print(f"Created student with Student ID: TEST_SIGNUP_1")
    else:
        print(f"Student already exists")

except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
