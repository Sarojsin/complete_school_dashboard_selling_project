import requests
import random
import string

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_parent_access():
    # 1. Create Student
    username = f"stud_{generate_random_string(6)}"
    email = f"{username}@example.com"
    password = "password123"
    student_id = f"STU_{generate_random_string(5)}"
    
    print(f"1. Creating Student: {student_id}")
    
    signup_data = {
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Test Student",
        "student_id": student_id,
        "date_of_birth": "2005-01-01",
        "phone": "1234567890",
        "address": "123 Test St",
        "parent_name": "Parent Test",
        "parent_phone": "0987654321",
        "grade_level": "10",
        "section": "A"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/student", json=signup_data)
    if response.status_code != 200:
        print(f"   ❌ Student Signup Failed: {response.text}")
        return
    print("   ✓ Student created")

    # 2. Create Parent
    parent_username = f"parent_{generate_random_string(6)}"
    parent_email = f"{parent_username}@example.com"
    
    print(f"2. Creating Parent: {parent_username}")
    
    parent_signup_data = {
        "email": parent_email,
        "username": parent_username,
        "password": password,
        "full_name": "Test Parent",
        "student_id": student_id,
        "phone": "0987654321",
        "address": "123 Test St",
        "occupation": "Tester"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=parent_signup_data)
    if response.status_code != 200:
        print(f"   ❌ Parent Signup Failed: {response.text}")
        return
    print("   ✓ Parent created")

    # 3. Login as Parent
    print(f"3. Logging in as Parent")
    login_data = {
        "username": parent_username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"   ❌ Login Failed: {response.text}")
        return
    
    print("   ✓ Login successful")
    login_response = response.json()
    print(f"   User role: {login_response['user']['role']}")
    
    # 4. Try to access parent dashboard
    print(f"4. Accessing Parent Dashboard")
    cookies = response.cookies
    
    response = requests.get(f"{BASE_URL}/parent/dashboard", cookies=cookies)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Parent dashboard accessible!")
    else:
        print(f"   ❌ Dashboard access failed: {response.text[:200]}")

if __name__ == "__main__":
    test_parent_access()
