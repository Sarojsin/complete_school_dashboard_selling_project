# -*- coding: utf-8 -*-
import requests
import random
import string
from sqlalchemy import create_engine, text
from database.database import engine

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

BASE_URL = "http://localhost:8000"

print("="*60)
print("Testing Name Field Storage in Profile Tables")
print("="*60)

# Create a new student
student_username = f"test_student_{generate_random_string(6)}"
student_name = "Test Student Name"
student_data = {
    "email": f"{student_username}@example.com",
    "username": student_username,
    "password": "password123",
    "full_name": student_name,
    "student_id": f"STU_{generate_random_string(6)}",
    "grade_level": "10",
    "section": "A",
    "date_of_birth": "2008-01-01",
    "phone": "1234567890",
    "address": "Test Address"
}

print("\n1. Creating new student...")
response = requests.post(f"{BASE_URL}/api/auth/signup/student", json=student_data)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)

student_user_id = response.json()["user"]["id"]
print(f"OK - Student created with user_id: {student_user_id}")

# Check database directly
print("\n2. Checking database for name storage...")
with engine.connect() as conn:
    # Check students table
    result = conn.execute(text("SELECT full_name FROM students WHERE user_id = :user_id"), {"user_id": student_user_id})
    row = result.fetchone()
    if row and row[0]:
        print(f"OK - Student name in database: '{row[0]}'")
        if row[0] == student_name:
            print("OK - Name matches!")
        else:
            print(f"ERROR - Name mismatch! Expected '{student_name}', got '{row[0]}'")
    else:
        print("ERROR - No name found in students table!")

# Create a new teacher
teacher_username = f"test_teacher_{generate_random_string(6)}"
teacher_name = "Test Teacher Name"
teacher_data = {
    "email": f"{teacher_username}@example.com",
    "username": teacher_username,
    "password": "password123",
    "full_name": teacher_name,
    "employee_id": f"EMP_{generate_random_string(6)}",
    "department": "Test Dept",
    "phone": "9876543210"
}

print("\n3. Creating new teacher...")
response = requests.post(f"{BASE_URL}/api/auth/signup/teacher", json=teacher_data)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)

teacher_user_id = response.json()["user"]["id"]
print(f"OK - Teacher created with user_id: {teacher_user_id}")

print("\n4. Checking database for teacher name...")
with engine.connect() as conn:
    result = conn.execute(text("SELECT full_name FROM teachers WHERE user_id = :user_id"), {"user_id": teacher_user_id})
    row = result.fetchone()
    if row and row[0]:
        print(f"OK - Teacher name in database: '{row[0]}'")
        if row[0] == teacher_name:
            print("OK - Name matches!")
        else:
            print(f"ERROR - Name mismatch!")
    else:
        print("ERROR - No name found in teachers table!")

print("\n" + "="*60)
print("TEST COMPLETED!")
print("="*60)
