import requests
import random
import string

BASE_URL = "http://localhost:8001"

def test_fee_structure():
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    
    # 1. Create an authority user
    auth_username = f"auth_fee_{suffix}"
    auth_data = {
        "email": f"{auth_username}@example.com",
        "username": auth_username,
        "password": "password123",
        "full_name": "Fee Admin",
        "phone": "1234567890",
        "position": "Admin",
        "department": "Finance",
        "secret_key": "admin-secret-2024"
    }
    print(f"Creating authority: {auth_username}")
    resp = requests.post(f"{BASE_URL}/api/auth/signup/authority", json=auth_data)
    if resp.status_code != 200:
        print(f"Failed to create authority: {resp.text[:200]}")
        return

    # 2. Login as authority
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
    
    # 3. Access the Fee Structure page (GET)
    print("Accessing Fee Structure page...")
    resp = requests.get(f"{BASE_URL}/authority/fee-structure", cookies=cookies)
    if resp.status_code == 200:
        print("SUCCESS: Fee Structure page loaded.")
    else:
        print(f"FAILURE: Failed to load Fee Structure page. Status: {resp.status_code}")
        return

    # 4. Create a new Fee Structure (POST)
    print("Creating new Fee Structure...")
    fee_data = {
        "grade_level": "10",
        "academic_year": "2024-2025",
        "tuition_fee": "5000",
        "registration_fee": "500",
        "library_fee": "200",
        "sports_fee": "300",
        "lab_fee": "400",
        "activity_fee": "100",
        "other_charges": "50",
        "due_date": "2024-12-31",
        "description": "Standard fee structure for Grade 10"
    }
    
    resp = requests.post(f"{BASE_URL}/authority/fee-structure", data=fee_data, cookies=cookies, allow_redirects=False)
    
    if resp.status_code == 303:
        print("SUCCESS: Fee Structure created (redirected).")
    else:
        print(f"FAILURE: Failed to create Fee Structure. Status: {resp.status_code}, Response: {resp.text[:200]}")
        return

    # 5. Verify it appears in the list
    print("Verifying new structure in list...")
    resp = requests.get(f"{BASE_URL}/authority/fee-structure", cookies=cookies)
    if "Standard fee structure for Grade 10" in resp.text:
        print("SUCCESS: New Fee Structure found in the list!")
    else:
        print("FAILURE: New Fee Structure NOT found in the list.")

if __name__ == "__main__":
    test_fee_structure()
