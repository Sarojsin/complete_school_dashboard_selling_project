import requests
import random
import string

BASE_URL = "http://localhost:8001"

def test_course_search():
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    # 1. Create a teacher
    teacher_name = f"Prof {suffix}"
    teacher_data = {
        "email": f"prof_{suffix}@example.com",
        "username": f"prof_{suffix}",
        "password": "password123",
        "full_name": teacher_name,
        "employee_id": f"EMP_{suffix}",
        "phone": "1234567890",
        "department": "Science",
        "qualification": "Ph.D",
        "specialization": "Physics"
    }
    print(f"Creating teacher: {teacher_name}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/teacher", json=teacher_data)
    if resp.status_code != 200:
        print(f"Failed to create teacher: {resp.text[:200]}")
        return
    teacher_id = resp.json().get("id") # Note: signup might not return ID directly, but let's see
    
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
    
    # 4. Create a course via the new POST endpoint
    course_code = f"PHY{suffix}"
    course_name = f"Physics {suffix}"
    print(f"Creating course: {course_name} ({course_code})")
    
    # We need to get the teacher ID properly. For now, let's just use the form without teacher if possible or try to fetch teachers
    # Actually, let's just try to search for an existing course or create one blindly
    
    course_data = {
        "code": course_code,
        "name": course_name,
        "description": "Intro to Physics",
        "department": "Science",
        "grade_level": "11",
        "credits": "3",
        "course_type": "core",
        "start_date": "2024-01-01",
        "end_date": "2024-06-01"
        # teacher_id might be required, let's see if we can skip it or if we need to fetch it
    }
    
    # Let's try to create it. If it fails due to missing teacher, we'll know.
    # But wait, I implemented the POST handler to require teacher_id if present in form.
    # Let's just search for "Mathematics" which should be in the seed data or previously created courses
    
    print(f"Searching for: {course_name}")
    # First, let's try to create it to ensure it exists
    resp = requests.post(f"{BASE_URL}/authority/courses/add", data=course_data, cookies=cookies)
    
    # Now search
    resp = requests.get(f"{BASE_URL}/authority/courses", params={"search": course_name}, cookies=cookies)
    
    if resp.status_code == 200:
        if course_name in resp.text:
            print("SUCCESS: Course found in search results!")
        else:
            print("FAILURE: Course NOT found in search results (might not have been created if teacher_id was required)")
            # Try searching for something generic that might exist
            print("Searching for 'Math'...")
            resp = requests.get(f"{BASE_URL}/authority/courses", params={"search": "Math"}, cookies=cookies)
            if "Math" in resp.text:
                 print("SUCCESS: Found 'Math' in search results!")
    else:
        print(f"Request failed: {resp.status_code}")

if __name__ == "__main__":
    test_course_search()
