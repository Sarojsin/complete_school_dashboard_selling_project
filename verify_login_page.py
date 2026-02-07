import httpx
import asyncio

async def verify_login_page():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/login", timeout=10.0)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("✅ Login page reachable")
                if "EduManage" in response.text and "Welcome Back" in response.text:
                    print("✅ Login page content verified")
                else:
                    print("❌ Login page content mismatch")
                    print(response.text[:500])
            else:
                print(f"❌ Failed to reach login page. Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    asyncio.run(verify_login_page())
