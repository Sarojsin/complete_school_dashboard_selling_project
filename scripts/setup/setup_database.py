"""
Database setup script
Creates tables and adds initial data
"""
from database.database import engine, Base
from models.models import User, Student, Teacher, Authority, UserRole
from models.chat_models import ChatMessage
from models.test_models import Test, TestQuestion, TestSubmission
from repositories.user_repository import UserRepository
from database.database import SessionLocal
from datetime import datetime

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

def create_default_users():
    """Create default admin, teacher, and student accounts"""
    db = SessionLocal()
    
    try:
        # Check if admin exists
        existing_admin = db.query(User).filter(User.role == UserRole.AUTHORITY).first()
        if existing_admin:
            print("✓ Admin user already exists")
            return
        
        print("Creating default users...")
        
        # Create Authority user
        admin_user = UserRepository.create(
            db=db,
            email="admin@school.com",
            username="admin",
            password="admin123",
            full_name="School Administrator",
            role=UserRole.AUTHORITY
        )
        
        authority = Authority(
            user_id=admin_user.id,
            position="Principal",
            department="Administration",
            phone="1234567890"
        )
        db.add(authority)
        
        # Create Teacher user
        teacher_user = UserRepository.create(
            db=db,
            email="teacher@school.com",
            username="teacher",
            password="teacher123",
            full_name="John Teacher",
            role=UserRole.TEACHER
        )
        
        teacher = Teacher(
            user_id=teacher_user.id,
            employee_id="T001",
            phone="1234567891",
            department="Mathematics",
            qualification="M.Sc Mathematics",
            specialization="Algebra"
        )
        db.add(teacher)
        
        # Create Student user
        student_user = UserRepository.create(
            db=db,
            email="student@school.com",
            username="student",
            password="student123",
            full_name="Jane Student",
            role=UserRole.STUDENT
        )
        
        student = Student(
            user_id=student_user.id,
            student_id="S001",
            grade_level="10",
            section="A",
            phone="1234567892",
            parent_name="Parent Name",
            parent_phone="1234567893"
        )
        db.add(student)
        
        db.commit()
        
        print("✓ Default users created successfully")
        print("\n" + "="*50)
        print("DEFAULT LOGIN CREDENTIALS")
        print("="*50)
        print("\nAdmin/Authority:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nTeacher:")
        print("  Username: teacher")
        print("  Password: teacher123")
        print("\nStudent:")
        print("  Username: student")
        print("  Password: student123")
        print("\n" + "="*50)
        print("\n⚠️  IMPORTANT: Change these passwords in production!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"✗ Error creating default users: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("\n" + "="*50)
    print("School Management System - Database Setup")
    print("="*50 + "\n")
    
    init_db()
    create_default_users()
    
    print("\n✓ Database setup complete!")
    print("You can now run the application with:")
    print("  uvicorn app.main:app --reload\n")

if __name__ == "__main__":
    main()