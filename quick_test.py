import httpx
import json
import random
import string

def random_suffix():
    return ''.join(random.choices(string.digits, k=4))

BASE_URL = "http://127.0.0.1:8000"
suffix = random_suffix()
student_data = {
    "username": f"test_student_{suffix}",
    "email": f"test.student_{suffix}@example.com",
    "password": "TestPass123!",
    "full_name": "Test Student",
    "student_id": f"TS2024{suffix}",
    "portal_type": "college"
}

response = httpx.post(f"{BASE_URL}/api/v1/auth/signup/college/student", json=student_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Also test teacher
teacher_data = {
    "username": f"test_teacher_{suffix}",
    "email": f"test.teacher_{suffix}@example.com",
    "password": "TestPass123!",
    "full_name": "Test Teacher",
    "employee_id": f"TT2024{suffix}",
    "portal_type": "college"
}
resp2 = httpx.post(f"{BASE_URL}/api/v1/auth/signup/college/teacher", json=teacher_data)
print(f"\nTeacher Status: {resp2.status_code}")
print(f"Teacher Response: {resp2.text}")
