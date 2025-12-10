import requests
import random
import string

BASE_URL = "http://localhost:8000"

def test_parent_auth_api():
    print("Testing Parent Authorization via API...")
    
    # 1. Signup a student first
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    student_username = f"student_auth_{suffix}"
    password = "password123"
    student_email = f"{student_username}@example.com"
    
    student_data = {
        "email": student_email,
        "username": student_username,
        "password": password,
        "full_name": "Auth Test Student",
        "student_id": f"STU_{suffix}",
        "date_of_birth": "2010-01-01",
        "phone": "1234567890",
        "address": "Test Address",
        "parent_name": "Test Parent",
        "parent_phone": "0987654321"
    }
    
    print(f"1. Signing up new student: {student_username}")
    response = requests.post(f"{BASE_URL}/api/auth/signup/student", json=student_data)
    if response.status_code != 200:
        print(f"Student Signup failed: {response.text}")
        return
    
    # Get student ID from response
    # Response structure: {"user": {"id": 1, ...}, "student": {"id": 1, "student_id": "...", ...}}
    # Or maybe just the user/student object. Let's check.
    # Based on previous tests, it returns the created user/profile.
    # Let's assume response.json()["student"]["id"] is the profile ID, or we need the user ID?
    # Parent links to student via student_id (string) or ID (int)?
    # ParentCreate schema has student_id: str. This usually refers to the student_id string (e.g. STU_...).
    
    student_id_str = student_data["student_id"]
    print(f"   Student created with ID: {student_id_str}")

    # 2. Signup a parent
    parent_username = f"parent_auth_{suffix}"
    parent_email = f"{parent_username}@example.com"
    
    parent_data = {
        "email": parent_email,
        "username": parent_username,
        "password": password,
        "full_name": "Auth Test Parent",
        "phone": "1234567890",
        "address": "Test Address",
        "occupation": "Tester",
        "student_id": student_id_str  # Link to the student we just created
    }
    
    print(f"2. Signing up new parent: {parent_username}")
    response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=parent_data)
    if response.status_code != 200:
        print(f"Parent Signup failed: {response.text}")
        return
        
    print("   Parent Signup successful")
    
    # 3. Login
    print("3. Logging in as parent...")
    login_data = {
        "username": parent_username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login successful")
    
    # 4. Access protected parent route
    print("4. Accessing protected parent route (get contacts)...")
    response = requests.get(f"{BASE_URL}/api/chat/contacts/parent", headers=headers)
    
    if response.status_code == 200:
        print("   SUCCESS: Authorized!")
        print(f"   Contacts count: {len(response.json())}")
    else:
        print(f"   FAILED: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_parent_auth_api()
