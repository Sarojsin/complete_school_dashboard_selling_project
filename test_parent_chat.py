import requests

BASE_URL = "http://localhost:8000"

# Use parent credentials from earlier test
parent_username = "parent_f2fbid8z"  # From successful test
password = "password123"

print("Testing Parent Chat Access...")
print("1. Logging in as parent")

login_data = {
    "username": parent_username,
    "password": password
}

response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
if response.status_code != 200:
    print(f"   ❌ Login failed: {response.status_code}")
    exit(1)

print("   ✓ Login successful")
cookies = response.cookies

print("2. Accessing parent chat page")
response = requests.get(f"{BASE_URL}/parent/chat", cookies=cookies)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("   ✓ Parent chat page accessible!")
else:
    print(f"   ❌ Failed: {response.text[:500]}")
