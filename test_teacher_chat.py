import requests
import random
import string

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_teacher_chat():
    # 1. Create Teacher
    username = f"teach_{generate_random_string(6)}"
    email = f"{username}@example.com"
    password = "password123"
    
    print(f"1. Creating Teacher: {username}")
    
    signup_data = {
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Test Teacher",
        "employee_id": f"EMP_{generate_random_string(5)}",
        "department": "Science",
        "phone": "1234567890",
        "address": "123 Test St",
        "subjects": ["Physics", "Chemistry"],
        "qualification": "PhD"
    }
    
    # Assuming there's a teacher signup endpoint or we need to use admin
    # Let's try the signup endpoint if it exists, otherwise we might need to login as existing teacher
    # Checking auth routes... /api/auth/signup/teacher exists
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/teacher", json=signup_data)
    if response.status_code != 200:
        print(f"   ❌ Teacher Signup Failed: {response.text}")
        return
    print("   ✓ Teacher created")

    # 2. Login as Teacher
    print(f"2. Logging in as Teacher")
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
    
    # 3. Access Teacher Chat
    print(f"3. Accessing Teacher Chat")
    response = requests.get(f"{BASE_URL}/teacher/chat", cookies=cookies)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Teacher chat accessible!")
        if "WebSocket connected" in response.text: # Check for JS content
            print("   ✓ WebSocket JS present")
    else:
        print(f"   ❌ Chat access failed: {response.text[:200]}")

if __name__ == "__main__":
    test_teacher_chat()
