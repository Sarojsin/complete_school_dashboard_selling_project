
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
# Import all models to ensure mapper registry is populated
from app.models.models import User, Student, Teacher, Course, Assignment, AssignmentSubmission, CourseEnrollment

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
