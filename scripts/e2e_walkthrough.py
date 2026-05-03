"""
End-to-End Walkthrough Automation

This script performs a full cycle for both school and college portals:
1. Sign up a test user
2. Login and obtain JWT token
3. Access the user's dashboard endpoint
4. Verify database records exist in correct database

Usage: python scripts/e2e_walkthrough.py
"""

import requests
import random
import string
import sys
import os

# Ensure backend is running at this URL
BASE_URL = "http://127.0.0.1:8000/api/v1"

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def test_school_flow():
    print("\n" + "="*60)
    print("📚 SCHOOL PORTAL E2E TEST")
    print("="*60)
    
    # 1. Signup a school student
    username = f"school_student_{rand_str()}"
    password = "TestPass123!"
    student_id = f"STU_{rand_str(5)}"
    
    print(f"\n1️⃣  Signing up school student: {username}")
    signup_data = {
        "email": f"{username}@test.com",
        "username": username,
        "password": password,
        "full_name": "Test School Student",
        "student_id": student_id,
        "date_of_birth": "2005-01-01",
        "phone": "1234567890",
        "address": "123 School St",
        "parent_name": "Test Parent",
        "parent_phone": "0987654321",
        "grade_level": "10",
        "section": "A"
    }
    
    resp = requests.post(f"{BASE_URL}/auth/signup/student", json=signup_data)
    if resp.status_code != 201:
        print(f"   ❌ Signup failed: {resp.status_code} - {resp.text}")
        return False
    print("   ✅ Signup successful")
    
    # 2. Login
    print(f"\n2️⃣  Logging in as {username}")
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": username,
        "password": password
    })
    if login_resp.status_code != 200:
        print(f"   ❌ Login failed: {login_resp.status_code} - {login_resp.text}")
        return False
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ Login successful, token obtained")
    
    # 3. Access school student dashboard
    print(f"\n3️⃣  Accessing /api/v1/school/students/dashboard")
    dash_resp = requests.get(f"{BASE_URL}/school/students/dashboard", headers=headers)
    if dash_resp.status_code != 200:
        print(f"   ❌ Dashboard access failed: {dash_resp.status_code} - {dash_resp.text}")
        return False
    print("   ✅ School dashboard accessible")
    print(f"   Data: {dash_resp.json()}")
    
    # 4. Verify DB insertion (direct DB query)
    print(f"\n4️⃣  Verifying database records")
    try:
        # Import DB modules (requiring setup)
        sys.path.insert(0, '.')
        from modules.shared.database import engine as school_engine
        from modules.shared.models import User
        from sqlalchemy import text, select
        
        with school_engine.connect() as conn:
            # Check user exists with portal_type='school'
            result = conn.execute(
                text("SELECT id, username, portal_type FROM users WHERE username = :u"),
                {"u": username}
            ).fetchone()
            if not result:
                print("   ❌ User not found in school DB")
                return False
            user_id = result[0]
            portal_type = result[2]
            print(f"   User ID: {user_id}, Portal: {portal_type}")
            if portal_type != 'school':
                print(f"   ❌ Wrong portal_type: expected 'school', got '{portal_type}'")
                return False
            print("   ✅ User correctly stored with portal_type='school'")
            
            # Check student profile exists
            student_result = conn.execute(
                text("SELECT id, student_id FROM school_students WHERE user_id = :uid"),
                {"uid": user_id}
            ).fetchone()
            if not student_result:
                print("   ❌ Student profile not found in school DB")
                return False
            print(f"   Student profile ID: {student_result[0]}, Student ID: {student_result[1]}")
            print("   ✅ Student profile correctly created")
            
        return True
    except Exception as e:
        print(f"   ❌ DB verification error: {e}")
        return False

def test_college_flow():
    print("\n" + "="*60)
    print("🎓 COLLEGE PORTAL E2E TEST")
    print("="*60)
    
    # 1. Signup a college student
    username = f"college_student_{rand_str()}"
    password = "TestPass123!"
    roll = f"R{rand_str(5)}"
    
    print(f"\n1️⃣  Signing up college student: {username}")
    signup_data = {
        "email": f"{username}@test.com",
        "username": username,
        "password": password,
        "full_name": "Test College Student",
        "roll_number": roll,
        "date_of_birth": "2002-01-01",
        "phone": "1234567890",
        "address": "456 College Ave",
        "cgpa": 8.5,
        "total_credits_completed": 60,
        "program_id": 1,  # Assume exists
        "semester_id": 1  # Assume exists
    }
    
    resp = requests.post(f"{BASE_URL}/auth/signup/college_student", json=signup_data)
    if resp.status_code not in [200, 201]:
        print(f"   ❌ Signup failed: {resp.status_code} - {resp.text}")
        return False
    print("   ✅ Signup successful")
    
    # 2. Login
    print(f"\n2️⃣  Logging in as {username}")
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": username,
        "password": password
    })
    if login_resp.status_code != 200:
        print(f"   ❌ Login failed: {login_resp.status_code} - {login_resp.text}")
        return False
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ Login successful, token obtained")
    
    # 3. Access college student dashboard
    print(f"\n3️⃣  Accessing /api/v1/college/students/dashboard")
    dash_resp = requests.get(f"{BASE_URL}/college/students/dashboard", headers=headers)
    if dash_resp.status_code != 200:
        print(f"   ❌ Dashboard access failed: {dash_resp.status_code} - {dash_resp.text}")
        return False
    print("   ✅ College dashboard accessible")
    print(f"   Data: {dash_resp.json()}")
    
    # 4. Verify DB insertion in college DB
    print(f"\n4️⃣  Verifying database records (college DB)")
    try:
        sys.path.insert(0, '.')
        from modules.college.database import CollegeAsyncSessionLocal
        from backup.models.college.student import CollegeStudent
        from sqlalchemy import select
        
        # Use async session in sync context
        import asyncio
        async def check():
            async with CollegeAsyncSessionLocal() as db:
                result = await db.execute(
                    select(CollegeStudent).where(CollegeStudent.user.has(username=username))
                )
                student = result.scalars().first()
                return student
        
        student = asyncio.run(check())
        if not student:
            print("   ❌ College student record not found in college DB")
            return False
        print(f"   College Student ID: {student.id}, Roll: {student.roll_number}")
        print("   ✅ College student profile correctly created")
        return True
    except Exception as e:
        print(f"   ❌ DB verification error: {e}")
        import traceback; traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("🚀 END-TO-END WALKTHROUGH AUTOMATION")
    print("="*60)
    
    school_ok = test_school_flow()
    college_ok = test_college_flow()
    
    print("\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    print(f"School Portal: {'✅ PASS' if school_ok else '❌ FAIL'}")
    print(f"College Portal: {'✅ PASS' if college_ok else '❌ FAIL'}")
    
    if school_ok and college_ok:
        print("\n✅ All E2E checks passed!")
        return 0
    else:
        print("\n❌ Some checks failed — review output above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
