import subprocess, time, requests, json, os

# Start uvicorn server
proc = subprocess.Popen(
    ["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc"
)

# Wait for startup
time.sleep(8)

# Capture initial logs
import select
if proc.stdout:
    proc.stdout.flush()
    time.sleep(1)

# Now make a test request
import httpx
import random, string

def rand_suffix():
    return ''.join(random.choices(string.digits, k=4))

suffix = rand_suffix()
student_data = {
    "username": f"teststudent_{suffix}",
    "email": f"teststudent_{suffix}@example.com",
    "password": "TestPass123!",
    "full_name": "Test Student",
    "student_id": f"TS2024{suffix}",
    "portal_type": "college"
}

try:
    resp = httpx.post("http://127.0.0.1:8000/api/v1/auth/signup/college/student", json=student_data, timeout=10.0)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
except Exception as e:
    print(f"Request error: {e}")

# Stop server
proc.terminate()
proc.wait(timeout=5)
