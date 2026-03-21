import requests

BASE_URL = "http://localhost:8000"


def test_refresh_flow():
    print("Step 1: Logging in...")
    login_data = {"username": "student", "password": "student123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)

    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    access_cookie = response.cookies.get("access_token")
    refresh_cookie = response.cookies.get("refresh_token")
    cookies = response.cookies

    if not access_cookie or not refresh_cookie:
        print("Login did not return expected auth cookies.")
        return

    print("Logged in. Auth cookies received.")

    print("\nStep 2: Accessing protected resource...")
    resp = requests.get(f"{BASE_URL}/student/dashboard", cookies=cookies)
    if resp.status_code == 200:
        print("Access granted to dashboard.")
    else:
        print(f"Access denied: {resp.status_code}")

    print("\nStep 3: Refreshing token...")
    refresh_resp = requests.post(f"{BASE_URL}/api/auth/refresh", cookies=cookies)
    if refresh_resp.status_code == 200:
        new_access_cookie = refresh_resp.cookies.get("access_token")
        new_refresh_cookie = refresh_resp.cookies.get("refresh_token")
        if new_access_cookie and new_refresh_cookie:
            print("Token refreshed. New auth cookies received.")
        else:
            print("Refresh succeeded but did not include rotated auth cookies.")
    else:
        print(f"Refresh failed: {refresh_resp.status_code} - {refresh_resp.text}")


if __name__ == "__main__":
    test_refresh_flow()
