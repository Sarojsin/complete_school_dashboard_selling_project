import requests
import random
import string

BASE_URL = "http://localhost:8001"

def verify_search():
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    # 1. Create a student to search for
    student_username = f"search_target_{suffix}"
    student_name = f"Search Target {suffix}"
    student_data = {
        "email": f"{student_username}@example.com",
        "username": student_username,
        "password": "password123",
        "full_name": student_name,
        "student_id": f"STU_{suffix}",
        "date_of_birth": "2010-01-01",
        "phone": "1234567890",
        "address": "Test Address",
        "parent_name": "Test Parent",
        "parent_phone": "0987654321",
        "grade_level": "10",
        "section": "A"
    }
    print(f"Creating student: {student_name}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/student", json=student_data)
    if resp.status_code != 200:
        print(f"Failed to create student: {resp.text}")
        return
    
    # 2. Create an authority user
    auth_username = f"authority_{suffix}"
    auth_data = {
        "email": f"{auth_username}@example.com",
        "username": auth_username,
        "password": "password123",
        "full_name": "Authority User",
        "phone": "1234567890",
        "position": "Admin",
        "department": "Administration",
        "secret_key": "admin-secret-2024"  # This matches AUTHORITY_SECRET_KEY in config.py
    }
    print(f"Creating authority: {auth_username}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/authority", json=auth_data)
    if resp.status_code != 200:
        print(f"Failed to create authority: {resp.text}")
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
    # The app uses cookies for HTML pages authentication usually, specifically "access_token" cookie
    cookies = {"access_token": f"Bearer {token}"} 
    
    # 4. Search for the student
    print(f"Searching for: {student_name}")
    resp = requests.get(f"{BASE_URL}/authority/students", params={"search": student_name}, cookies=cookies)
    
    if resp.status_code == 200:
        if student_name in resp.text:
            print("SUCCESS: Student found in search results!")
        else:
            print("FAILURE: Student NOT found in search results.")
            # print(resp.text)
    else:
        print(f"Request failed: {resp.status_code}")

if __name__ == "__main__":
    verify_search()
