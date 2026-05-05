"""
Comprehensive test for college signup flow (Student & Teacher)
Tests:
1. POST /api/v1/auth/signup/college/student
2. POST /api/v1/auth/signup/college/teacher
3. Database verification in both school_sell_db.users and college_sell_db
4. Login and JWT token verification
"""

import asyncio
import random
import string
import httpx

# RANDOM SUFFIX for unique test credentials
SUFFIX = ''.join(random.choices(string.digits, k=4))
STUDENT_USERNAME = f"college_student_{SUFFIX}"
STUDENT_EMAIL = f"college.student{SUFFIX}@test.com"
STUDENT_ID = f"CS2024{SUFFIX}"
TEACHER_USERNAME = f"college_teacher_{SUFFIX}"
TEACHER_EMAIL = f"college.teacher{SUFFIX}@test.com"
TEACHER_EMPLOYEE_ID = f"CT2024{SUFFIX}"

BASE_URL = "http://127.0.0.1:8000"

# Import everything at the top to ensure mappers are configured before any DB session starts
# This must be after all model modules are loaded to avoid circular dependency errors
from modules.shared import models as shared_models
from modules.school.school_teacher import models as teacher_models
from modules.school.school_parent import models as parent_models  # IMPORTANT: before student
from modules.school.school_student import models as student_models
from modules.school.school_authority import models as authority_models
from modules.school.school_classes import models as class_models
from modules.school.school_subjects import models as subject_models
from modules.school.school_courses import models as course_models
from modules.school.school_assignments import models as assignment_models
from modules.school.school_notes import models as note_models
from modules.school.school_attendance import models as attendance_models
# More school models...
from modules.school.school_grades import models as grades_models
from modules.school.school_tests import models as tests_models
from modules.school.school_videos import models as videos_models
from modules.school.school_exam_section import models as exam_models
from modules.school.school_timetable import models as timetable_models
from modules.school.school_account_section import models as account_models
from modules.school.school_library import models as school_library_models
from modules.school.school_groups import models as groups_models
from modules.school.school_chat import models as chat_models
from modules.school.school_notices import models as notices_models
from modules.school.school_dashboard import models as dashboard_models
# College models
from modules.college.college_courses import models as college_course_models
from modules.college.college_student import models as college_student_models
from modules.college.college_faculty import models as college_faculty_models
from modules.college.college_library import models as college_library_models
from modules.college.college_hostel import models as college_hostel_models
from modules.college.college_lab import models as college_lab_models
from modules.college.college_placement import models as college_placement_models
from modules.college.college_research import models as college_research_models

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from modules.shared.models import User
from backup.models.college.student import CollegeStudent as BackupCollegeStudent
from backup.models.college.faculty import Faculty as BackupFaculty
from modules.shared.config import settings

def get_async_url(url):
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///")
    return url

school_engine = create_async_engine(get_async_url(settings.DATABASE_URL_FIXED))
college_engine = create_async_engine(get_async_url(settings.COLLEGE_DATABASE_URL))
SchoolSessionLocal = sessionmaker(school_engine, class_=AsyncSession, expire_on_commit=False)
CollegeSessionLocal = sessionmaker(college_engine, class_=AsyncSession, expire_on_commit=False)

async def test_college_student_signup():
    print("\n=== Testing College Student Signup ===")
    student_data = {
        "username": STUDENT_USERNAME,
        "email": STUDENT_EMAIL,
        "password": "SecurePass123!",
        "full_name": "College Student Test",
        "student_id": STUDENT_ID,
        "portal_type": "college"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/auth/signup/college/student", json=student_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        try:
            print(f"Response JSON: {response.json()}")
        except:
            print(f"Response Text: {response.text}")
        if response.status_code == 201:
            print("College student signup successful")
            return response.json()
        else:
            print(f"College student signup failed")
            return None

async def verify_student_in_db(username=STUDENT_USERNAME):
    print(f"\n=== Verifying student '{username}' in databases ===")
    async with SchoolSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if user:
            print(f"User found in school_sell_db.users (id={user.id}, portal_type={user.portal_type}, role={user.role})")
        else:
            print("User NOT found in school_sell_db.users")
            return False
    async with CollegeSessionLocal() as college_db:
        result = await college_db.execute(select(BackupCollegeStudent).where(BackupCollegeStudent.user_id == user.id))
        college_student = result.scalars().first()
        if college_student:
            print(f"CollegeStudent found in college_sell_db (id={college_student.id}, roll_number={college_student.roll_number})")
            return True
        else:
            print("CollegeStudent NOT found in college_sell_db")
            return False

async def test_college_student_login():
    print("\n=== Testing College Student Login ===")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": STUDENT_USERNAME, "password": "SecurePass123!", "portal_type": "college"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Login successful - portal_type: {data.get('portal_type')}, role: {data.get('role')}")
            return token
        else:
            print(f"Login failed: {response.text}")
            return None

async def test_college_teacher_signup():
    print("\n=== Testing College Teacher Signup ===")
    teacher_data = {
        "username": TEACHER_USERNAME,
        "email": TEACHER_EMAIL,
        "password": "SecurePass123!",
        "full_name": "College Teacher Test",
        "employee_id": TEACHER_EMPLOYEE_ID,
        "portal_type": "college"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/auth/signup/college/teacher", json=teacher_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("College teacher signup successful")
            return response.json()
        else:
            print(f"College teacher signup failed: {response.text}")
            return None

async def verify_teacher_in_db(username=TEACHER_USERNAME):
    print(f"\n=== Verifying teacher '{username}' in databases ===")
    async with SchoolSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if user:
            print(f"User found in school_sell_db.users (id={user.id}, portal_type={user.portal_type}, role={user.role})")
        else:
            print("User NOT found in school_sell_db.users")
            return False
    async with CollegeSessionLocal() as college_db:
        result = await college_db.execute(select(BackupFaculty).where(BackupFaculty.user_id == user.id))
        faculty = result.scalars().first()
        if faculty:
            print(f"Faculty found in college_sell_db (id={faculty.id}, employee_id={faculty.employee_id})")
            return True
        else:
            print("Faculty NOT found in college_sell_db")
            return False

async def test_college_teacher_login():
    print("\n=== Testing College Teacher Login ===")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": TEACHER_USERNAME, "password": "SecurePass123!", "portal_type": "college"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Login successful - portal_type: {data.get('portal_type')}, role: {data.get('role')}")
            return token
        else:
            print(f"Login failed: {response.text}")
            return None

async def main():
    print("=" * 60)
    print("College Signup Flow Test")
    print("=" * 60)
    
    student_result = await test_college_student_signup()
    student_verified = await verify_student_in_db() if student_result else False
    student_token = await test_college_student_login() if student_result else None
    
    teacher_result = await test_college_teacher_signup()
    teacher_verified = await verify_teacher_in_db() if teacher_result else False
    teacher_token = await test_college_teacher_login() if teacher_result else None
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"College Student Signup: {'PASS' if student_result else 'FAIL'}")
    print(f"Student DB Verification: {'PASS' if student_verified else 'FAIL'}")
    print(f"College Student Login: {'PASS' if student_token else 'FAIL'}")
    print(f"College Teacher Signup: {'PASS' if teacher_result else 'FAIL'}")
    print(f"Teacher DB Verification: {'PASS' if teacher_verified else 'FAIL'}")
    print(f"College Teacher Login: {'PASS' if teacher_token else 'FAIL'}")
    
    all_passed = all([student_result, student_verified, student_token, teacher_result, teacher_verified, teacher_token])
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())
