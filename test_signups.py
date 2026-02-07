import httpx
import asyncio

async def test_hod_signup():
    async with httpx.AsyncClient() as client:
        payload = {
            "email": "hod_test@school.com",
            "username": "hod_test",
            "password": "123",
            "full_name": "HOD Test User",
            "employee_id": "HOD001",
            "department": "Computer Science",
            "qualification": "PhD",
            "specialization": "AI",
            "phone": "1234567890"
        }
        response = await client.post("http://localhost:8000/api/auth/signup/hod", json=payload)
        print(f"HOD Signup Status: {response.status_code}")
        print(f"Response: {response.json()}")

async def test_exam_signup():
    async with httpx.AsyncClient() as client:
        payload = {
            "email": "exam_test@school.com",
            "username": "exam_test",
            "password": "123",
            "full_name": "Exam Test User",
            "position": "Exam Controller",
            "department": "Exam Section",
            "phone": "9876543210",
            "secret_key": "saroj_special_key" # Replace with actual setting
        }
        response = await client.post("http://localhost:8000/api/auth/signup/exam-section", json=payload)
        print(f"Exam Signup Status: {response.status_code}")
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    # Ensure server is running before executing
    asyncio.run(test_hod_signup())
    asyncio.run(test_exam_signup())
