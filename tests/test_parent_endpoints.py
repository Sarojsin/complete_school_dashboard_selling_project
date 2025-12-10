import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING PARENT ENDPOINTS")
print("=" * 60)

# Test 1: Parent Signup
print("\n1. Testing Parent Signup...")
print("-" * 60)
signup_data = {
    "email": "testparent@school.com",
    "username": "testparent",
    "password": "Password123",
    "full_name": "Test Parent",
    "phone": "1234567890",
    "address": "123 Test Street",
    "occupation": "Engineer",
    "student_id": 1
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/signup/parent",
        json=signup_data,
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Parent signup successful!")
    else:
        print(f"❌ Parent signup failed: {response.json().get('detail', 'Unknown error')}")
except Exception as e:
    print(f"❌ Error during signup: {str(e)}")

# Test 2: Parent Login
print("\n2. Testing Parent Login...")
print("-" * 60)
login_data = {
    "username": "testparent",
    "password": "Password123"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        access_token = result.get("access_token")
        user_data = result.get("user")
        print("✅ Parent login successful!")
        print(f"User: {user_data.get('full_name')} ({user_data.get('role')})")
        print(f"Token: {access_token[:50]}...")
        
        # Save token for next tests
        headers = {"Cookie": f"access_token=Bearer {access_token}"}
        
        # Test 3: Access Parent Dashboard
        print("\n3. Testing Parent Dashboard Access...")
        print("-" * 60)
        try:
            dash_response = requests.get(
                f"{BASE_URL}/parent/dashboard",
                headers=headers,
                timeout=10
            )
            print(f"Status Code: {dash_response.status_code}")
            if dash_response.status_code == 200:
                print("✅ Parent dashboard accessible!")
            else:
                print(f"❌ Dashboard access failed: {dash_response.status_code}")
        except Exception as e:
            print(f"❌ Error accessing dashboard: {str(e)}")
            
        # Test 4: Check Parent Chat Endpoint
        print("\n4. Testing Parent Chat Page...")
        print("-" * 60)
        try:
            chat_response = requests.get(
                f"{BASE_URL}/parent/chat",
                headers=headers,
                timeout=10
            )
            print(f"Status Code: {chat_response.status_code}")
            if chat_response.status_code == 200:
                print("✅ Parent chat page accessible!")
            else:
                print(f"❌ Chat access failed: {chat_response.status_code}")
        except Exception as e:
            print(f"❌ Error accessing chat: {str(e)}")
            
        # Test 5: Check Parent Notices Endpoint
        print("\n5. Testing Parent Notices Page...")
        print("-" * 60)
        try:
            notices_response = requests.get(
                f"{BASE_URL}/parent/notices",
                headers=headers,
                timeout=10
            )
            print(f"Status Code: {notices_response.status_code}")
            if notices_response.status_code == 200:
                print("✅ Parent notices page accessible!")
            else:
                print(f"❌ Notices access failed: {notices_response.status_code}")
        except Exception as e:
            print(f"❌ Error accessing notices: {str(e)}")
            
    else:
        print(f"❌ Parent login failed: {response.json().get('detail', 'Unknown error')}")
except Exception as e:
    print(f"❌ Error during login: {str(e)}")

print("\n" + "=" * 60)
print("PARENT ENDPOINT TESTING COMPLETE")
print("=" * 60)
