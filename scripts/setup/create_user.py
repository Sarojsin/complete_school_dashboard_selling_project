import requests

url = "http://localhost:8000/api/auth/signup/student"
data = {
    "username": "teststudent2",
    "email": "test2@student.com",
    "password": "password123",
    "full_name": "Test Student 2",
    "student_id": "STU002",
    "date_of_birth": "2000-01-01",
    "phone": "1234567890",
    "address": "123 Test St",
    "parent_name": "Parent Test",
    "parent_phone": "0987654321",
    "grade_level": "10",
    "section": "A"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
