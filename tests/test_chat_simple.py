# -*- coding: utf-8 -*-
import requests
import random
import string
import time

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

print("="*60)
print("PARENT-TEACHER CHAT TEST")
print("="*60)

# 1. Create Teacher
teacher_username = f"teacher_demo_{generate_random_string(6)}"
teacher_data = {
    "email": f"{teacher_username}@example.com",
    "username": teacher_username,
    "password": "password123",
    "full_name": "Demo Teacher",
    "employee_id": f"EMP_{generate_random_string(5)}",
    "department": "Mathematics",
    "phone": "1234567890",
    "address": "123 Teacher St",
    "subjects": ["Mathematics"],
    "qualification": "PhD"
}

print("\n1. Creating Teacher...")
response = requests.post(f"{BASE_URL}/api/auth/signup/teacher", json=teacher_data)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
teacher_user_id = response.json()["user"]["id"]
print(f"OK - Teacher ID: {teacher_user_id}")

# 2. Create Student
student_username = f"student_demo_{generate_random_string(6)}"
student_data = {
    "email": f"{student_username}@example.com",
    "username": student_username,
    "password": "password123",
    "full_name": "Demo Student",
    "student_id": f"STU_{generate_random_string(6)}",
    "grade_level": "10",
    "section": "A",
    "date_of_birth": "2008-01-01",
    "phone": "9876543210",
    "address": "456 Student Ave"
}

print("\n2. Creating Student...")
response = requests.post(f"{BASE_URL}/api/auth/signup/student", json=student_data)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
student_user_id = response.json()["user"]["id"]
print(f"OK - Student ID: {student_user_id}")

# 3. Create Parent
parent_username = f"parent_demo_{generate_random_string(6)}"
parent_data = {
    "email": f"{parent_username}@example.com",
    "username": parent_username,
    "password": "password123",
    "full_name": "Demo Parent",
    "phone": "5555555555",
    "address": "789 Parent Blvd",
    "student_id": student_data["student_id"]
}

print("\n3. Creating Parent...")
response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=parent_data)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
parent_user_id = response.json()["user"]["id"]
print(f"OK - Parent ID: {parent_user_id}")

# 4. Login as Parent
print("\n4. Parent Login...")
response = requests.post(f"{BASE_URL}/api/auth/login", data={"username": parent_username, "password": "password123"})
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
parent_cookies = response.cookies
print("OK")

# 5. Login as Teacher
print("\n5. Teacher Login...")
response = requests.post(f"{BASE_URL}/api/auth/login", data={"username": teacher_username, "password": "password123"})
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
teacher_cookies = response.cookies
print("OK")

# 6. Parent sends message to Teacher
print("\n6. Parent --> Teacher Message...")
msg_data = {"content": "Hello Teacher! Test message from parent."}
response = requests.post(f"{BASE_URL}/api/chat/messages/{teacher_user_id}", json=msg_data, cookies=parent_cookies)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
print("OK - Message sent")
time.sleep(1)

# 7. Teacher sends message to Parent
print("\n7. Teacher --> Parent Message...")
msg_data = {"content": "Hello Parent! Thank you for your message."}
response = requests.post(f"{BASE_URL}/api/chat/messages/{parent_user_id}", json=msg_data, cookies=teacher_cookies)
if response.status_code != 200:
    print(f"Failed: {response.text}")
    exit(1)
print("OK - Message sent")
time.sleep(1)

# 8. Verify messages
print("\n8. Verifying Message Exchange...")
response = requests.get(f"{BASE_URL}/api/chat/messages/{teacher_user_id}", cookies=parent_cookies)
if response.status_code == 200:
    messages = response.json()["messages"]
    print(f"Parent sees {len(messages)} messages:")
    for msg in messages[-2:]:
        sender = "Parent" if msg["sender_id"] == parent_user_id else "Teacher"
        print(f"  [{sender}]: {msg['content']}")

response = requests.get(f"{BASE_URL}/api/chat/messages/{parent_user_id}", cookies=teacher_cookies)
if response.status_code == 200:
    messages = response.json()["messages"]
    print(f"Teacher sees {len(messages)} messages:")
    for msg in messages[-2:]:
        sender = "Parent" if msg["sender_id"] == parent_user_id else "Teacher"
        print(f"  [{sender}]: {msg['content']}")

print("\n" + "="*60)
print("TEST COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nDemo Accounts:")
print(f"  Teacher: {teacher_username} / password123")
print(f"  Parent:  {parent_username} / password123")
print(f"  Student: {student_username} / password123")
