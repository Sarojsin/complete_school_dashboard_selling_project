import asyncio
import sys
import os

# Add the current directory to sys.path to allow imports from app and modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import AsyncSessionLocal, async_engine
from modules.shared.models import User, UserRole
from modules.shared.auth_utils import get_password_hash
from modules.school_teacher.models import Teacher
from modules.shared.base import Base

async def seed():
    # Create tables if they don't exist
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        # Create a test teacher user
        username = "testteacher"
        email = "teacher@example.com"
        password = "password123"
        
        # Check if user already exists
        from sqlalchemy import select
        result = await db.execute(select(User).filter(User.username == username))
        existing_user = result.scalars().first()
        
        if not existing_user:
            print(f"Creating user {username}...")
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
                full_name="Test Teacher",
                role=UserRole.TEACHER,
                is_active=True
            )
            db.add(user)
            await db.flush() # To get the user ID
            
            print(f"Creating teacher profile for {username}...")
            teacher = Teacher(
                user_id=user.id,
                employee_id="T1001",
                full_name="Test Teacher",
                department="Computer Science",
                qualification="M.Tech",
                status="active"
            )
            db.add(teacher)
            await db.commit()
            print("Seeding completed successfully!")
            print(f"Login with: {username} / {password}")
        else:
            print(f"User {username} already exists.")
            
        # Create a test student user
        student_username = "teststudent"
        student_email = "student@example.com"
        student_password = "password123"
        
        result = await db.execute(select(User).filter(User.username == student_username))
        existing_student_user = result.scalars().first()
        
        if not existing_student_user:
            print(f"Creating student user {student_username}...")
            student_user = User(
                username=student_username,
                email=student_email,
                hashed_password=get_password_hash(student_password),
                full_name="Test Student",
                role=UserRole.STUDENT,
                is_active=True
            )
            db.add(student_user)
            await db.flush()
            
            from modules.school_student.models import Student
            print(f"Creating student profile for {student_username}...")
            student = Student(
                user_id=student_user.id,
                student_id="S2001",
                full_name="Test Student",
                grade_level="Class 10",
                section="A",
                roll_number="101"
            )
            db.add(student)
            await db.commit()
            print("Student seeding completed successfully!")
            print(f"Login with: {student_username} / {student_password}")
        else:
            print(f"User {student_username} already exists.")

if __name__ == "__main__":
    asyncio.run(seed())
