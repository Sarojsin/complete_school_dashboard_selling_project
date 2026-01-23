import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from repositories.user_repository import UserRepository
from models.models import UserRole

def create_test_users():
    db = SessionLocal()
    try:
        # Check if users already exist
        existing_teacher = UserRepository.get_by_username(db, "teacher1")
        existing_student = UserRepository.get_by_username(db, "student1")
        
        if existing_teacher:
            print(f"✅ Teacher user '{existing_teacher.username}' already exists (ID: {existing_teacher.id})")
        else:
            # Create teacher user
            teacher = UserRepository.create(
                db=db,
                email="teacher1@test.com",
                username="teacher1",
                password="password",
                full_name="Test Teacher One",
                role=UserRole.TEACHER
            )
            print(f"✅ Created teacher user: {teacher.username} (ID: {teacher.id})")
        
        if existing_student:
            print(f"✅ Student user '{existing_student.username}' already exists (ID: {existing_student.id})")
        else:
            # Create student user  
            student = UserRepository.create(
                db=db,
                email="student1@test.com",
                username="student1",
                password="password",
                full_name="Test Student One",
                role=UserRole.STUDENT
            )
            print(f"✅ Created student user: {student.username} (ID: {student.id})")
        
        # Create an authority user for testing group creation
        existing_authority = UserRepository.get_by_username(db, "authority1")
        if existing_authority:
            print(f"✅ Authority user '{existing_authority.username}' already exists (ID: {existing_authority.id})")
        else:
            authority = UserRepository.create(
                db=db,
                email="authority1@test.com",
                username="authority1",
                password="password",
                full_name="Test Authority",
                role=UserRole.AUTHORITY
            )
            print(f"✅ Created authority user: {authority.username} (ID: {authority.id})")
        
        print("\n🎉 All test users ready!")
        print("\nLogin Credentials:")
        print("  Teacher:   username='teacher1'   password='password'")
        print("  Student:   username='student1'   password='password'") 
        print("  Authority: username='authority1' password='password'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
