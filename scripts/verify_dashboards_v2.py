import asyncio
import httpx
import sys

# BASE_URL is not used directly for the list below to avoid prefix confusion
BASE_URL = "http://localhost:8000"

async def check_endpoint(client, path, role_name):
    full_url = f"{BASE_URL}{path}"
    print(f"Checking {role_name} dashboard: {full_url}...", end=" ")
    try:
        response = await client.get(path)
        # 200: Success
        # 401: Unauthorized (expected without token)
        # 403: Forbidden (expected without token)
        if response.status_code in [200, 401, 403]:
            print(f"PASSED ({response.status_code})")
        else:
            print(f"FAILED ({response.status_code})")
            if response.status_code == 422:
                print(f"  Validation Error (422): {response.json()}")
            elif response.status_code == 404:
                print(f"  Not Found (404) - Check route registration.")
            elif response.status_code == 500:
                print(f"  Internal Server Error (500) - Check server logs.")
    except Exception as e:
        print(f"CONNECTION ERROR: {str(e)}")

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Based on app/main.py and individual module routers
        endpoints = [
            ("/api/v1/school/student", "Student"),
            ("/api/v1/school/teacher", "Teacher"),
            ("/api/v1/school/parent", "Parent"),
            ("/api/v1/school/authority", "Authority"),
            ("/api/v1/school/dashboard", "HOD"),
            ("/admin/dashboard", "Super Admin"),
        ]
        
        print(f"Starting dashboard API audit on {BASE_URL}...")
        for path, role in endpoints:
            await check_endpoint(client, path, role)

if __name__ == "__main__":
    asyncio.run(main())
