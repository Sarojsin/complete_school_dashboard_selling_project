
import sys
import os
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup.core.database import SessionLocal
from backup.models.models import User, Student, Course, Assignment, CourseEnrollment
from backup.repositories.student_repository import StudentRepository
from backup.repositories.assignment_repository import AssignmentRepository

def debug_student_access(email: str):
    db = SessionLocal()
    try:
        print(f"\n--- Debugging Access for {email} ---")
        
        # 1. Get User
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ User not found: {email}")
            return
        print(f"✅ Found User: ID {user.id}, Role {user.role}")

        # 2. Get Student Profile
        student = StudentRepository.get_by_user_id(db, user.id)
        if not student:
            print("❌ Student profile not found")
            return
        print(f"✅ Found Student Profile: ID {student.id}, Grade {student.grade_level}, Section {student.section}")

        # 3. Check Enrollments
        courses = StudentRepository.get_enrolled_courses(db, student.id)
        enrolled_ids = [c.id for c in courses]
        print(f"ℹ️  Direct Enrollments: {len(courses)} courses found. IDs: {enrolled_ids}")
        for c in courses:
            print(f"   - {c.course_name} (Grade {c.grade_level})")

        # 4. Check Grade-based Fallback (if logic uses it)
        fallback_courses = db.query(Course).filter(Course.grade_level == student.grade_level).all()
        fallback_ids = [c.id for c in fallback_courses]
        print(f"ℹ️  Grade-level Fallback: {len(fallback_courses)} courses found for Grade {student.grade_level}. IDs: {fallback_ids}")
        for c in fallback_courses:
            print(f"   - {c.course_name} (ID: {c.id})")

        # 5. Simulate Route Logic
        course_ids = enrolled_ids
        if not course_ids:
            print("⚠️  No direct enrollments, using fallback...")
            course_ids = fallback_ids
        
        print(f"👉 Final Course IDs used for query: {course_ids}")

        if not course_ids:
            print("❌ No courses identified for this student. No assignments will be fetched.")
            return

        # 6. Fetch Assignments
        assignments = AssignmentRepository.get_student_assignments(db, student.id, course_ids)
        print(f"ℹ️  Assignments Found: {len(assignments)}")
        for a in assignments:
            print(f"   - ID: {a['id']}, Title: '{a['title']}', Status: {a['status']}, CourseID: {a['course'].id}")

        # 7. Check All Assignments (Raw DB)
        all_assignments_count = db.query(Assignment).count()
        print(f"\n--- Global Stats ---")
        print(f"Total Assignments in DB: {all_assignments_count}")
        all_assignments = db.query(Assignment).all()
        for a in all_assignments:
             print(f"   - Global Assignment: ID {a.id}, CourseID {a.course_id}, Grade {a.course.grade_level if a.course else 'N/A'}")

    finally:
        db.close()

if __name__ == "__main__":
    # You can change the email to the one you are testing with
    debug_student_access("sarojsinghdhami@gmail.com")
