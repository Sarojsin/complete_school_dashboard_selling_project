import requests
import time

BASE_URL = "http://localhost:8000"

def test_refresh_flow():
    print("Step 1: Logging in...")
    login_data = {"username": "student", "password": "student123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    cookies = response.cookies
    
    print(f"✅ Logged in. Access Token: {access_token[:10]}... Refresh Token: {refresh_token[:10]}...")
    
    print("\nStep 2: Accessing protected resource...")
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"{BASE_URL}/student/dashboard", cookies=cookies)
    if resp.status_code == 200:
        print("✅ Access granted to dashboard.")
    else:
        print(f"❌ Access denied: {resp.status_code}")

    print("\nStep 3: Refreshing token...")
    # Simulate refresh call
    refresh_resp = requests.post(f"{BASE_URL}/api/auth/refresh", cookies=cookies)
    if refresh_resp.status_code == 200:
        new_data = refresh_resp.json()
        print(f"✅ Token refreshed. New Access Token: {new_data['access_token'][:10]}...")
    else:
        print(f"❌ Refresh failed: {refresh_resp.status_code} - {refresh_resp.text}")

if __name__ == "__main__":
    test_refresh_flow()
