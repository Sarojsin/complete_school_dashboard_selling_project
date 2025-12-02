# API Testing Guide

Complete guide for testing all API endpoints using cURL, Postman, or Python.

## Authentication

All protected endpoints require a JWT token in the Authorization header.

### Login

```bash
# Get access token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student&password=student123"

# Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "student@school.com",
    "username": "student",
    "full_name": "Jane Student",
    "role": "student"
  }
}
```

### Using Token

```bash
TOKEN="your-jwt-token-here"

curl http://localhost:8000/api/students/me \
  -H "Authorization: Bearer $TOKEN"
```

## Student Endpoints

### Get Student Profile

```bash
curl http://localhost:8000/api/students/me \
  -H "Authorization: Bearer $TOKEN"
```

### Get Student Dashboard

```bash
curl http://localhost:8000/api/students/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

### Get Enrolled Courses

```bash
curl http://localhost:8000/api/students/courses \
  -H "Authorization: Bearer $TOKEN"
```

### Get Course Details

```bash
curl http://localhost:8000/api/students/courses/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Get Assignments

```bash
curl http://localhost:8000/api/students/assignments \
  -H "Authorization: Bearer $TOKEN"
```

### Get Grades

```bash
curl http://localhost:8000/api/students/grades \
  -H "Authorization: Bearer $TOKEN"
```

### Get Attendance

```bash
curl http://localhost:8000/api/students/attendance \
  -H "Authorization: Bearer $TOKEN"
```

### Get Fees

```bash
curl http://localhost:8000/api/students/fees \
  -H "Authorization: Bearer $TOKEN"
```

## Test Management

### Get Available Tests (Student)

```bash
curl http://localhost:8000/api/tests/student/available \
  -H "Authorization: Bearer $TOKEN"
```

### Get Test Details (Student)

```bash
curl http://localhost:8000/api/tests/student/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Start Test

```bash
curl -X POST http://localhost:8000/api/tests/1/start \
  -H "Authorization: Bearer $TOKEN"

# Response includes test data and remaining time
```

### Submit Test

```bash
curl -X POST http://localhost:8000/api/tests/1/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "1": "Option A",
      "2": "True",
      "3": "Your answer here"
    }
  }'
```

### Get Test Result

```bash
curl http://localhost:8000/api/tests/student/1/result \
  -H "Authorization: Bearer $TOKEN"
```

### Get All Results

```bash
curl http://localhost:8000/api/tests/student/my-results \
  -H "Authorization: Bearer $TOKEN"
```

## Teacher Endpoints

### Create Test

```bash
curl -X POST http://localhost:8000/api/tests \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mid-term Exam",
    "description": "Mathematics mid-term examination",
    "course_id": 1,
    "duration": 60,
    "start_time": "2024-12-01T10:00:00",
    "end_time": "2024-12-01T12:00:00",
    "instructions": "Answer all questions. No calculators allowed.",
    "questions": [
      {
        "question_text": "What is 2 + 2?",
        "question_type": "mcq",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "points": 5,
        "order": 1
      },
      {
        "question_text": "Is Python a programming language?",
        "question_type": "true_false",
        "correct_answer": "True",
        "points": 5,
        "order": 2
      }
    ]
  }'
```

### Get Teacher's Tests

```bash
curl http://localhost:8000/api/tests/teacher/my-tests \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

### Update Test

```bash
curl -X PUT http://localhost:8000/api/tests/1 \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "is_active": false
  }'
```

### Delete Test

```bash
curl -X DELETE http://localhost:8000/api/tests/1 \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

### Get Test Results

```bash
curl http://localhost:8000/api/tests/1/results \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

## Chat Endpoints

### WebSocket Connection

```javascript
// JavaScript example
const token = localStorage.getItem('access_token');
const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);

ws.onopen = () => {
    console.log('Connected to chat');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Send message
ws.send(JSON.stringify({
    type: 'message',
    receiver_id: 2,
    content: 'Hello!'
}));

// Send typing indicator
ws.send(JSON.stringify({
    type: 'typing',
    receiver_id: 2
}));

// Mark messages as read
ws.send(JSON.stringify({
    type: 'mark_read',
    message_ids: [1, 2, 3]
}));
```

### Python WebSocket Client

```python
import asyncio
import websockets
import json

async def chat_client(token):
    uri = f"ws://localhost:8000/ws/chat?token={token}"
    
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            'type': 'message',
            'receiver_id': 2,
            'content': 'Hello from Python!'
        }))
        
        # Receive messages
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

# Run
token = "your-jwt-token"
asyncio.run(chat_client(token))
```

## File Upload Endpoints

### Upload Assignment

```bash
curl -X POST http://localhost:8000/api/assignments/1/submit \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@assignment.pdf" \
  -F "submission_text=Here is my assignment"
```

### Upload Notes

```bash
curl -X POST http://localhost:8000/api/notes/upload \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -F "file=@notes.pdf" \
  -F "title=Chapter 1 Notes" \
  -F "description=Introduction to Algebra" \
  -F "course_id=1"
```

### Upload Video

```bash
curl -X POST http://localhost:8000/api/videos/upload \
  -H "Authorization: Bearer $TEACHER_TOKEN" \
  -F "file=@lecture.mp4" \
  -F "title=Lecture 1" \
  -F "description=Introduction" \
  -F "course_id=1"
```

## Python Testing Examples

### Using Requests Library

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    data={"username": "student", "password": "student123"}
)
token = response.json()["access_token"]

# Headers for authenticated requests
headers = {"Authorization": f"Bearer {token}"}

# Get dashboard
dashboard = requests.get(
    f"{BASE_URL}/api/students/dashboard",
    headers=headers
)
print(dashboard.json())

# Get available tests
tests = requests.get(
    f"{BASE_URL}/api/tests/student/available",
    headers=headers
)
print(tests.json())

# Submit test
submission = requests.post(
    f"{BASE_URL}/api/tests/1/submit",
    headers=headers,
    json={
        "answers": {
            "1": "Option A",
            "2": "True"
        }
    }
)
print(submission.json())
```

### Complete Test Flow

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Login as student
login = requests.post(f"{BASE_URL}/api/auth/login", data={
    "username": "student",
    "password": "student123"
})
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Get available tests
tests = requests.get(f"{BASE_URL}/api/tests/student/available", headers=headers)
test_id = tests.json()[0]["id"]

# 3. Start test
start = requests.post(f"{BASE_URL}/api/tests/{test_id}/start", headers=headers)
print(f"Test started. Time remaining: {start.json()['time_remaining']} seconds")

# 4. Simulate taking test
time.sleep(2)  # Think for 2 seconds

# 5. Submit answers
answers = {}
for question in start.json()["test"]["questions"]:
    if question["question_type"] == "mcq":
        answers[str(question["id"])] = question["options"][0]
    elif question["question_type"] == "true_false":
        answers[str(question["id"])] = "True"

submission = requests.post(
    f"{BASE_URL}/api/tests/{test_id}/submit",
    headers=headers,
    json={"answers": answers}
)
print(f"Test submitted. Score: {submission.json()['score']}")

# 6. Get result
result = requests.get(
    f"{BASE_URL}/api/tests/student/{test_id}/result",
    headers=headers
)
print(f"Final result: {result.json()}")
```

## Postman Collection

### Environment Variables

```json
{
  "base_url": "http://localhost:8000",
  "token": "",
  "student_token": "",
  "teacher_token": "",
  "admin_token": ""
}
```

### Pre-request Script for Authentication

```javascript
// Add to Collection Pre-request Script
if (!pm.environment.get("token")) {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/auth/login",
        method: 'POST',
        header: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
            mode: 'urlencoded',
            urlencoded: [
                {key: 'username', value: 'student'},
                {key: 'password', value: 'student123'}
            ]
        }
    }, function (err, res) {
        pm.environment.set("token", res.json().access_token);
    });
}
```

## Integration Tests

### pytest Example

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/auth/login", data={
        "username": "student",
        "password": "student123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_dashboard():
    # Login first
    login = client.post("/api/auth/login", data={
        "username": "student",
        "password": "student123"
    })
    token = login.json()["access_token"]
    
    # Get dashboard
    response = client.get(
        "/api/students/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "student" in response.json()

def test_complete_test_flow():
    # Login
    login = client.post("/api/auth/login", data={
        "username": "student",
        "password": "student123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get available tests
    tests = client.get("/api/tests/student/available", headers=headers)
    assert tests.status_code == 200
    
    # Start test
    test_id = 1
    start = client.post(f"/api/tests/{test_id}/start", headers=headers)
    assert start.status_code == 200
    
    # Submit test
    submission = client.post(
        f"/api/tests/{test_id}/submit",
        headers=headers,
        json={"answers": {"1": "Option A"}}
    )
    assert submission.status_code == 200
```

## Load Testing

### Using Apache Bench

```bash
# Test login endpoint
ab -n 1000 -c 10 -p login.json -T application/x-www-form-urlencoded \
   http://localhost:8000/api/auth/login

# Test authenticated endpoint
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" \
   http://localhost:8000/api/students/dashboard
```

### Using Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class StudentUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/login", data={
            "username": "student",
            "password": "student123"
        })
        self.token = response.json()["access_token"]
    
    @task(3)
    def get_dashboard(self):
        self.client.get(
            "/api/students/dashboard",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(2)
    def get_courses(self):
        self.client.get(
            "/api/students/courses",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def get_tests(self):
        self.client.get(
            "/api/tests/student/available",
            headers={"Authorization": f"Bearer {self.token}"}
        )

# Run: locust -f locustfile.py
```

## Common Response Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

## Error Handling

```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Detail: {e.response.json()}")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.Timeout:
    print("Request timeout")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## Tips

1. **Use environment variables** for tokens and base URLs
2. **Implement retry logic** for failed requests
3. **Add timeouts** to all requests
4. **Log all API calls** for debugging
5. **Test edge cases** (empty data, invalid inputs)
6. **Check response times** for performance
7. **Validate response schemas** against documentation
8. **Test with different user roles** (student, teacher, admin)

## Automation

```bash
#!/bin/bash
# test-api.sh - Automated API testing script

BASE_URL="http://localhost:8000"

# Login and get token
TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -d "username=student&password=student123" | jq -r '.access_token')

echo "Token obtained: ${TOKEN:0:20}..."

# Test endpoints
echo "Testing dashboard..."
curl -s "$BASE_URL/api/students/dashboard" \
  -H "Authorization: Bearer $TOKEN" | jq '.student.user.full_name'

echo "Testing courses..."
curl -s "$BASE_URL/api/students/courses" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'

echo "All tests passed!"
```