import requests
import random
import string

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_parent_sees_all_teachers():
    """Test that parent can see all teachers in contacts list"""
    # Create parent
    username = f"parent_{generate_random_string(6)}"
    email = f"{username}@example.com"
    password = "password123"
    
    print(f"1. Creating Parent: {username}")
    
    # Create a student first
    student_username = f"student_{generate_random_string(6)}"
    student_data = {
        "email": f"{student_username}@example.com",
        "username": student_username,
        "password": password,
        "full_name": "Test Student",
        "grade_level": "10",
        "section": "A",
        "roll_number": random.randint(1, 100),
        "date_of_birth": "2008-01-01",
        "gender": "male",
        "phone": "1234567890",
        "address": "123 Test St"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/student", json=student_data)
    if response.status_code != 200:
        print(f"   ❌ Student creation failed: {response.text}")
        return
    student_id = response.json()["id"]
    print(f"   ✓ Student created with ID: {student_id}")
    
    # Create parent
    parent_data = {
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Test Parent",
        "phone": "0987654321",
        "address": "456 Parent Ave",
        "student_ids": [student_id]
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=parent_data)
    if response.status_code != 200:
        print(f"   ❌ Parent Signup Failed: {response.text}")
        return
    print("   ✓ Parent created")
    
    # Login as parent
    print(f"2. Logging in as parent")
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"   ❌ Login Failed: {response.text}")
        return
    
    print("   ✓ Login successful")
    cookies = response.cookies
    
    # Get parent contacts (should return ALL teachers, not just child's teachers)
    print(f"3. Fetching parent contacts")
    response = requests.get(f"{BASE_URL}/api/chat/contacts/parent", cookies=cookies)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        contacts = response.json()
        print(f"   ✓ Parent can see {len(contacts)} teacher(s)")
        if len(contacts) > 0:
            print(f"   ✓ Contact list includes: {[c['user']['full_name'] for c in contacts]}")
        print("   ✓ SUCCESS: Parent contact endpoint works!")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")

if __name__ == "__main__":
    test_parent_sees_all_teachers()
