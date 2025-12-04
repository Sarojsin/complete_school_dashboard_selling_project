import requests
import random
import string

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_signup_and_login():
    # 1. Create Student
    username = f"user_{generate_random_string()}"
    email = f"{username}@example.com"
    password = "password123"
    student_id = f"STU_{generate_random_string(5)}"
    
    print(f"Creating Student: {username}, {student_id}")
    
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
        print(f"Student Signup Failed: {response.text}")
        return
    print("Student Signup Success")

    # 2. Create Parent linked to Student
    parent_username = f"parent_{generate_random_string()}"
    parent_email = f"{parent_username}@example.com"
    
    print(f"Creating Parent: {parent_username} linked to {student_id}")
    
    parent_signup_data = {
        "email": parent_email,
        "username": parent_username,
        "password": password,
        "full_name": "Test Parent",
        "student_id": student_id, # Linking to the student created above
        "phone": "0987654321",
        "address": "123 Test St",
        "occupation": "Tester"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=parent_signup_data)
    print(f"Parent Signup Status: {response.status_code}")
    print(f"Parent Signup Response: {response.text}")
    
    if response.status_code == 200:
        print("Parent Signup SUCCESS!")
        
        # 3. Login Parent
        print("Attempting Parent Login...")
        login_data = {
            "username": parent_username,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        print(f"Parent Login Status: {response.status_code}")
        if response.status_code == 200:
            print("Parent Login SUCCESS!")
        else:
            print(f"Parent Login FAILED: {response.text}")

if __name__ == "__main__":
    test_signup_and_login()
