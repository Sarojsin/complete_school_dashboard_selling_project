"""
Test college signup using FastAPI TestClient to get full error tracebacks
"""
import asyncio
from fastapi.testclient import TestClient
from app.main import app

# Generate unique credentials
import random, string
suffix = ''.join(random.choices(string.digits, k=4))
STUDENT_USERNAME = f"student_{suffix}"
STUDENT_EMAIL = f"student_{suffix}@test.com"
STUDENT_ID = f"CS2024{suffix}"
TEACHER_USERNAME = f"teacher_{suffix}"
TEACHER_EMAIL = f"teacher_{suffix}@test.com"
TEACHER_EMPLOYEE_ID = f"CT2024{suffix}"

client = TestClient(app)

print("=" * 60)
print("College Signup Test (using TestClient)")
print("=" * 60)

# Test student signup
print("\n--- College Student Signup ---")
student_data = {
    "username": STUDENT_USERNAME,
    "email": STUDENT_EMAIL,
    "password": "SecurePass123!",
    "full_name": "College Student Test",
    "student_id": STUDENT_ID,
    "portal_type": "college"
}
response = client.post("/api/v1/auth/signup/college/student", json=student_data)
print(f"Status: {response.status_code}")
if response.status_code == 201:
    print("SUCCESS: Student signup")
    print(f"Response: {response.json()}")
else:
    print("FAILED: Student signup")
    print(f"Response: {response.text}")
    # Try to get detail if JSON

# Test teacher signup
print("\n--- College Teacher Signup ---")
teacher_data = {
    "username": TEACHER_USERNAME,
    "email": TEACHER_EMAIL,
    "password": "SecurePass123!",
    "full_name": "College Teacher Test",
    "employee_id": TEACHER_EMPLOYEE_ID,
    "portal_type": "college"
}
response2 = client.post("/api/v1/auth/signup/college/teacher", json=teacher_data)
print(f"Status: {response2.status_code}")
if response2.status_code == 201:
    print("SUCCESS: Teacher signup")
    print(f"Response: {response2.json()}")
else:
    print("FAILED: Teacher signup")
    print(f"Response: {response2.text}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Student signup: {'PASS' if response.status_code == 201 else 'FAIL'}")
print(f"Teacher signup: {'PASS' if response2.status_code == 201 else 'FAIL'}")
