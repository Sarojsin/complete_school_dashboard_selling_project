import requests

BASE_URL = "http://localhost:8001"

def test_add_student():
    # 1. Create authority and login
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    auth_username = f"auth_{suffix}"
    auth_data = {
        "email": f"{auth_username}@example.com",
        "username": auth_username,
        "password": "password123",
        "full_name": "Authority Test",
        "phone": "1234567890",
        "position": "Admin",
        "department": "Administration",
        "secret_key": "admin-secret-2024"
    }
    
    print(f"Creating authority: {auth_username}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/authority", json=auth_data)
    if resp.status_code != 200:
        print(f"Failed to create authority: {resp.text}")
        return
    
    # Login
    login_data = {
        "username": auth_username,
        "password": "password123"
    }
    resp = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["access_token"]
    cookies = {"access_token": f"Bearer {token}"}
    
    # 2. Submit student form
    student_data = {
        "first_name": "John",
        "last_name": "Doe",
        "dob": "2010-01-01",
        "gender": "male",
        "address": "123 Test St",
        "email": f"john.doe.{suffix}@student.com",
        "phone": "1234567890",
        "emergency_contact": "Jane Doe",
        "emergency_phone": "0987654321",
        "grade": "10",
        "section": "A",
        "roll_number": "101",
        "admission_date": "2024-01-01",
        "student_id": f"STU{suffix}",
        "parent_name": "Jane Doe",
        "parent_relation": "mother",
        "parent_phone": "0987654321"
    }
    
    print(f"Creating student via form...")
    resp = requests.post(
        f"{BASE_URL}/authority/students/add",
        data=student_data,
        cookies=cookies,
        allow_redirects=False  # Don't follow redirect so we can see it
    )
    
    print(f"Status: {resp.status_code}")
    if resp.status_code == 303:
        print(f"Redirect to: {resp.headers.get('location')}")
        # Extract credentials from URL
        import urllib.parse
        location = resp.headers.get('location', '')
        if '?success=' in location:
            success_msg = urllib.parse.unquote(location.split('?success=')[1])
            print(f"SUCCESS! {success_msg}")
            
            # Try to login with generated credentials
            # Extract username and password from message
            if "Username:" in success_msg and "Password:" in success_msg:
                username_part = success_msg.split("Username:")[1].split(",")[0].strip()
                password_part = success_msg.split("Password:")[1].split("(")[0].strip()
                
                print(f"\nTrying to login as student...")
                print(f"Username: {username_part}")
                print(f"Password: {password_part}")
                
                login_resp = requests.post(
                    f"{BASE_URL}/api/auth/login",
                    data={"username": username_part, "password": password_part}
                )
                
                if login_resp.status_code == 200:
                    print("✓ Student can login successfully!")
                else:
                    print(f"✗ Student login failed: {login_resp.text}")
    else:
        print(f"Response: {resp.text[:500]}")

if __name__ == "__main__":
    test_add_student()
