"""
Script to create a test student and parent for verification
"""
from database.database import SessionLocal
from models.models import User, Student, Parent, UserRole
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository
from repositories.parent_repository import ParentRepository

db = SessionLocal()

try:
    # Step 1: Create a test student
    print("Step 1: Creating test student...")
    
    # Check if student already exists
    existing_student_user = UserRepository.get_by_username(db, "teststudent_forparent")
    if existing_student_user:
        print(f"✓ Student user already exists (ID: {existing_student_user.id})")
        student_user = existing_student_user
        student = StudentRepository.get_by_user_id(db, student_user.id)
    else:
        # Create student user
        student_user = UserRepository.create(
            db=db,
            email="teststudent@school.com",
            username="teststudent_forparent",
            password="Student123",
            full_name="Test Student For Parent",
            role=UserRole.STUDENT
        )
        
        # Create student profile
        student_profile_data = {
            "user_id": student_user.id,
            "student_id": "TEST999",
            "grade_level": "10",
            "section": "A"
        }
        student = StudentRepository.create(db, student_profile_data)
        print(f"✓ Created test student (ID: {student.id}, Student ID: TEST999)")
    
    # Step 2: Create parent account
    print("\nStep 2: Creating parent account...")
    
    # Check if parent exists
    existing_parent_user = UserRepository.get_by_username(db, "testparent_verified")
    if existing_parent_user:
        print(f"✗ Parent user already exists. Using existing account.")
        parent_user = existing_parent_user
    else:
        # Create parent user
        parent_user = UserRepository.create(
            db=db,
            email="testparent_verified@school.com",
            username="testparent_verified",
            password="Parent123",
            full_name="Test Parent Verified",
            role=UserRole.PARENT
        )
        
        # Create parent profile
        parent_profile_data = {
            "user_id": parent_user.id,
            "phone": "9876543210",
            "address": "456 Parent Avenue",
            "occupation": "Software Engineer"
        }
        parent = ParentRepository.create(db, parent_profile_data)
        
        # Link student to parent
        ParentRepository.link_child(db, parent.id, student.id)
        
        print(f"✓ Created parent account:")
        print(f"  Username: testparent_verified")
        print(f"  Password: Parent123")
        print(f"  Linked to student ID: TEST999")
    
    print("\n" + "="*60)
    print("TEST CREDENTIALS:")
    print("="*60)
    print(f"Username: testparent_verified")
    print(f"Password: Parent123")
    print(f"Child's Student ID: TEST999")
    print("="*60)
    print("\nYou can now login at: http://localhost:8000/login")
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
