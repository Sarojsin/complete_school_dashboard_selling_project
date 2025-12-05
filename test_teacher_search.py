import requests
import random
import string

BASE_URL = "http://localhost:8001"

def test_teacher_search():
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    # 1. Create a teacher to search for
    teacher_name = f"Test Teacher {suffix}"
    teacher_data = {
        "email": f"teacher_{suffix}@example.com",
        "username": f"teacher_{suffix}",
        "password": "password123",
        "full_name": teacher_name,
        "employee_id": f"EMP_{suffix}",
        "phone": "1234567890",
        "department": "Mathematics",
        "qualification": "M.Sc",
        "specialization": "Algebra"
    }
    print(f"Creating teacher: {teacher_name}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/teacher", json=teacher_data)
    if resp.status_code != 200:
        print(f"Failed to create teacher: {resp.text[:200]}")
        return
    
    # 2. Create an authority user
    auth_username = f"auth_{suffix}"
    auth_data = {
        "email": f"{auth_username}@example.com",
        "username": auth_username,
        "password": "password123",
        "full_name": "Authority User",
        "phone": "1234567890",
        "position": "Admin",
        "department": "Administration",
        "secret_key": "admin-secret-2024"
    }
    print(f"Creating authority: {auth_username}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/authority", json=auth_data)
    if resp.status_code != 200:
        print(f"Failed to create authority: {resp.text[:200]}")
        return

    # 3. Login as authority
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
    
    # 4. Search for the teacher
    print(f"Searching for: {teacher_name}")
    resp = requests.get(f"{BASE_URL}/authority/teachers", params={"search": teacher_name}, cookies=cookies)
    
    if resp.status_code == 200:
        if teacher_name in resp.text:
            print("SUCCESS: Teacher found in search results!")
        else:
            print("FAILURE: Teacher NOT found in search results.")
    else:
        print(f"Request failed: {resp.status_code}")

if __name__ == "__main__":
    test_teacher_search()
