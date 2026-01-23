
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from models.models import User, Student, Teacher, Course, CourseEnrollment, Assignment, UserRole
from repositories.user_repository import UserRepository

def create_test_data():
    db = SessionLocal()
    try:
        print("Creating test data...")

        # 1. Create Teacher
        teacher_email = "teacher@test.com"
        teacher_user = db.query(User).filter(User.email == teacher_email).first()
        if not teacher_user:
            teacher_user = User(
                email=teacher_email,
                username="teacher_test",
                hashed_password=UserRepository.get_password_hash("password123"),
                full_name="Test Teacher",
                role=UserRole.TEACHER
            )
            db.add(teacher_user)
            db.commit()
            db.refresh(teacher_user)
            
            teacher_profile = Teacher(
                user_id=teacher_user.id,
                employee_id="T001",
                full_name=teacher_user.full_name,
                department="Science"
            )
            db.add(teacher_profile)
            db.commit()
            print(f"Created teacher: {teacher_email}")
        else:
            teacher_profile = teacher_user.teacher_profile
            print(f"Teacher exists: {teacher_email}")

        # 2. Create Student
        student_email = "student@test.com"
        student_user = db.query(User).filter(User.email == student_email).first()
        if not student_user:
            student_user = User(
                email=student_email,
                username="student_test",
                hashed_password=UserRepository.get_password_hash("password123"),
                full_name="Test Student",
                role=UserRole.STUDENT
            )
            db.add(student_user)
            db.commit()
            db.refresh(student_user)
            
            student_profile = Student(
                user_id=student_user.id,
                student_id="S001",
                full_name=student_user.full_name,
                grade_level="10",
                section="A"
            )
            db.add(student_profile)
            db.commit()
            print(f"Created student: {student_email}")
        else:
            student_profile = student_user.student_profile
            print(f"Student exists: {student_email}")

        # 3. Create Course
        course_code = "SCI101"
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            course = Course(
                course_code=course_code,
                course_name="Introduction to Science",
                description="Basic science principles",
                teacher_id=teacher_profile.id,
                grade_level="10"
            )
            db.add(course)
            db.commit()
            db.refresh(course)
            print(f"Created course: {course_code}")
        else:
            print(f"Course exists: {course_code}")

        # 4. Enroll Student
        enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.student_id == student_profile.id,
            CourseEnrollment.course_id == course.id
        ).first()
        if not enrollment:
            enrollment = CourseEnrollment(
                student_id=student_profile.id,
                course_id=course.id
            )
            db.add(enrollment)
            db.commit()
            print("Enrolled student in course")
        else:
            print("Student already enrolled")

        # 5. Create Assignment
        assignment_title = "Science Lab Report 1"
        assignment = db.query(Assignment).filter(
            Assignment.course_id == course.id, 
            Assignment.title == assignment_title
        ).first()
        
        if not assignment:
            assignment = Assignment(
                title=assignment_title,
                description="Write a report on the chemical reaction experiment.",
                course_id=course.id,
                teacher_id=teacher_profile.id,
                due_date=datetime.utcnow() + timedelta(days=7),
                max_score=100
            )
            db.add(assignment)
            db.commit()
            print(f"Created assignment: {assignment_title}")
        else:
            print(f"Assignment exists: {assignment_title}")

        print("\nTest data setup complete!")
        print(f"Login as Student: {student_email} / password123")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
