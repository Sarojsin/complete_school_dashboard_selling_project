import urllib.request
import json
import urllib.error

url = "http://localhost:8000/api/auth/signup/parent"

def test_signup(payload, test_name):
    print(f"\n--- Test: {test_name} ---")
    headers = {
        "Content-Type": "application/json"
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.getcode()}")
            print(f"Response Body: {response.read().decode('utf-8')}")
            print("SUCCESS: Signup successful!")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
        print(f"Response Body: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")

# Test 1: Correct role
payload_correct = {
    "full_name": "API Test Parent Correct",
    "email": "api_test_parent_correct@school.com",
    "username": "api_test_parent_correct",
    "password": "Parent123",
    "role": "parent",
    "phone": "5555555555",
    "address": "123 API Test Lane",
    "occupation": "API Tester",
    "student_id": "TEST_SIGNUP_1"
}

# Test 2: Missing role
payload_no_role = {
    "full_name": "API Test Parent No Role",
    "email": "api_test_parent_norole@school.com",
    "username": "api_test_parent_norole",
    "password": "Parent123",
    # "role": "parent",  <-- Missing
    "phone": "5555555555",
    "address": "123 API Test Lane",
    "occupation": "API Tester",
    "student_id": "TEST_SIGNUP_1"
}

test_signup(payload_correct, "Correct Role")
test_signup(payload_no_role, "Missing Role")
