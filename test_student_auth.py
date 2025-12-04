import urllib.request
import json
import random
import string
import urllib.error

BASE_URL = "http://localhost:8000/api/auth"

def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_student_auth():
    username = f"student_{get_random_string()}"
    email = f"{username}@example.com"
    password = "TestPassword123"
    student_id = f"ST_{get_random_string(5).upper()}"
    
    print(f"Testing with Username: {username}, Student ID: {student_id}")

    # 1. Signup
    signup_payload = {
        "username": username,
        "email": email,
        "password": password,
        "full_name": "Test Student",
        "role": "student",
        "student_id": student_id,
        "grade_level": "10",
        "section": "A",
        "phone": "1234567890",
        "address": "123 Test St"
    }
    
    print("\n1. Testing Signup...")
    try:
        data = json.dumps(signup_payload).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/signup/student", data=data, headers={"Content-Type": "application/json"}, method='POST')
        
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.getcode()}")
            print("Signup Successful:", response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Signup Failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
        return
    except Exception as e:
        print(f"Signup Exception: {e}")
        return

    # 2. Login
    print("\n2. Testing Login...")
    login_payload = {
        "username": username,
        "password": password
    }
    
    try:
        data = json.dumps(login_payload).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/login-json", data=data, headers={"Content-Type": "application/json"}, method='POST')
        
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.getcode()}")
            resp_body = response.read().decode('utf-8')
            data = json.loads(resp_body)
            if "access_token" in data:
                print("Login Successful! Access Token received.")
            else:
                print("Login Successful but no token?", data)
    except urllib.error.HTTPError as e:
        print(f"Login Failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Login Exception: {e}")

if __name__ == "__main__":
    test_student_auth()
