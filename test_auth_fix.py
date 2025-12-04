import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User
from database.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE_URL = "http://localhost:8000"

def test_parent_auth():
    print("Testing Parent Authorization...")
    
    # Get the parent user credentials
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "parent_demo_6y025g").first()
        if not user:
            print("Parent user not found!")
            return
        
        # We don't know the password for this user, so let's create a new one or use the one we know
        # Let's use the 'parent_test' user if it exists, or create it
        
        # Actually, let's just create a new parent user to be sure
        username = "auth_test_parent"
        password = "password123"
        email = "auth_test_parent@example.com"
        
        # Check if exists
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            # We can't easily create via DB because of password hashing
            # Let's use the signup endpoint
            pass
        else:
            # If exists, we hope the password is correct. If not, we might fail login.
            pass
            
    finally:
        db.close()

    # Signup a new parent to ensure we have valid credentials
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    username = f"parent_auth_{suffix}"
    password = "password123"
    email = f"{username}@example.com"
    
    signup_data = {
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Auth Test Parent",
        "phone": "1234567890",
        "address": "Test Address",
        "occupation": "Tester"
    }
    
    print(f"1. Signing up new parent: {username}")
    response = requests.post(f"{BASE_URL}/api/auth/signup/parent", json=signup_data)
    if response.status_code != 200:
        print(f"Signup failed: {response.text}")
        return
        
    print("   Signup successful")
    
    # Login
    print("2. Logging in...")
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login successful")
    
    # Access protected parent route
    print("3. Accessing protected parent route (get contacts)...")
    response = requests.get(f"{BASE_URL}/api/chat/contacts/parent", headers=headers)
    
    if response.status_code == 200:
        print("   SUCCESS: Authorized!")
        print(f"   Contacts count: {len(response.json())}")
    else:
        print(f"   FAILED: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_parent_auth()
