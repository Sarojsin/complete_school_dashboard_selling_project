import asyncio
import httpx
import sys
import json
from typing import Dict, List, Any

BASE_URL = "http://localhost:8000"

# Credentials
CREDENTIALS = {
    "student": {"username": "student", "password": "student123"},
    "teacher": {"username": "teacher", "password": "teacher123"},
    "admin": {"username": "admin", "password": "admin123"}
}

# Endpoints to test
# Format: (method, path, role_required, data)
ENDPOINTS = [
    ("GET", "/", None, None),
    ("GET", "/health", None, None),
    
    # Auth
    ("POST", "/api/auth/login", None, {"username": "student", "password": "student123"}),
    
    # Student
    ("GET", "/api/students/dashboard", "student", None),
    ("GET", "/api/students/courses", "student", None),
    ("GET", "/api/students/assignments", "student", None),
    ("GET", "/api/students/grades", "student", None),
    ("GET", "/api/students/attendance", "student", None),
    ("GET", "/api/students/fees", "student", None),
    ("GET", "/api/students/notices", "student", None),
    ("GET", "/api/students/timetable", "student", None),
    ("GET", "/api/students/notes", "student", None),
    ("GET", "/api/students/videos", "student", None),
    
    # Teacher
    ("GET", "/api/teachers/dashboard", "teacher", None),
    ("GET", "/api/teachers/students", "teacher", None),
    ("GET", "/api/teachers/courses", "teacher", None),
    ("GET", "/api/teachers/assignments", "teacher", None),
    ("GET", "/api/teachers/attendance", "teacher", None),
    ("GET", "/api/teachers/grades", "teacher", None),
    ("GET", "/api/teachers/tests", "teacher", None),
    ("GET", "/api/teachers/timetable", "teacher", None),
    
    # Authority
    ("GET", "/api/authority/dashboard", "admin", None),
    ("GET", "/api/authority/students", "admin", None),
    ("GET", "/api/authority/teachers", "admin", None),
    ("GET", "/api/authority/courses", "admin", None),
    ("GET", "/api/authority/fees", "admin", None),
    ("GET", "/api/authority/notices", "admin", None),
    ("GET", "/api/authority/analytics", "admin", None),
    ("GET", "/api/authority/reports", "admin", None),
]

async def get_token(client: httpx.AsyncClient, role: str) -> str:
    creds = CREDENTIALS.get(role)
    if not creds:
        return None
    
    try:
        response = await client.post(f"{BASE_URL}/api/auth/login", data=creds)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Failed to login as {role}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error logging in as {role}: {e}")
        return None

async def verify_endpoints():
    print(f"Verifying endpoints on {BASE_URL}...\n")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Check if server is up
        try:
            await client.get(f"{BASE_URL}/health")
        except httpx.ConnectError:
            print("Error: Could not connect to server. Please make sure it is running.")
            print("Run: uvicorn app.main:app --reload")
            return

        # Get tokens
        tokens = {}
        for role in ["student", "teacher", "admin"]:
            token = await get_token(client, role)
            if token:
                tokens[role] = token
                print(f"✓ Authenticated as {role}")
            else:
                print(f"✗ Failed to authenticate as {role}")

        print("\nTesting Endpoints:")
        print("-" * 60)
        print(f"{'Method':<8} {'Role':<10} {'Status':<8} {'Path'}")
        print("-" * 60)

        results = {"passed": 0, "failed": 0}

        for method, path, role, data in ENDPOINTS:
            headers = {}
            if role:
                if role not in tokens:
                    print(f"{method:<8} {role:<10} SKIPPED  {path} (No token)")
                    results["failed"] += 1
                    continue
                headers["Authorization"] = f"Bearer {tokens[role]}"
                # print(f"DEBUG: Headers: {headers}")
            
            try:
                if method == "GET":
                    response = await client.get(f"{BASE_URL}{path}", headers=headers)
                elif method == "POST":
                    response = await client.post(f"{BASE_URL}{path}", headers=headers, json=data if role else None, data=data if not role else None)
                elif method == "PUT":
                    response = await client.put(f"{BASE_URL}{path}", headers=headers, json=data)
                elif method == "DELETE":
                    response = await client.delete(f"{BASE_URL}{path}", headers=headers)
                
                status = response.status_code
                status_str = str(status)
                
                if 200 <= status < 400:
                    print(f"{method:<8} {role or 'None':<10} {status_str:<8} {path}")
                    results["passed"] += 1
                else:
                    print(f"{method:<8} {role or 'None':<10} {status_str:<8} {path}")
                    # print(f"  Error: {response.text[:100]}...")
                    results["failed"] += 1
                    
            except Exception as e:
                print(f"{method:<8} {role or 'None':<10} ERROR    {path}")
                print(f"  Exception: {e}")
                results["failed"] += 1

        print("-" * 60)
        print(f"Total: {results['passed'] + results['failed']}, Passed: {results['passed']}, Failed: {results['failed']}")

if __name__ == "__main__":
    asyncio.run(verify_endpoints())
