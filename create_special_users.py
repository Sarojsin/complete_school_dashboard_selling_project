import asyncio
from sqlalchemy import text
from app.api.endpoints.auth import UserRepository
from app.core.database import AsyncSessionLocal
from app.models.models import UserRole

async def create_special_users():
    async with AsyncSessionLocal() as session:
        # 1. Create Library Manager
        print("--- Processing Library Manager ---")
        existing_lib = await UserRepository.get_by_username(session, "library_admin")
        if existing_lib:
            print(f"User 'library_admin' already exists.")
        else:
            print("Creating 'library_admin'...")
            try:
                await UserRepository.create(
                    db=session,
                    email="library@school.com",
                    username="library_admin",
                    password="123",
                    full_name="Library Manager",
                    role=UserRole.LIBRARY_MANAGER
                )
                print("Created 'library_admin' successfully.")
            except Exception as e:
                print(f"Failed to create library_admin: {e}")

        # 2. Create Account Section
        print("\n--- Processing Account Section ---")
        existing_acc = await UserRepository.get_by_username(session, "account_admin")
        if existing_acc:
            print(f"User 'account_admin' already exists.")
        else:
            print("Creating 'account_admin'...")
            try:
                await UserRepository.create(
                    db=session,
                    email="account@school.com",
                    username="account_admin",
                    password="123",
                    full_name="Account Manager",
                    role=UserRole.ACCOUNT_SECTION
                )
                print("Created 'account_admin' successfully.")
            except Exception as e:
                print(f"Failed to create account_admin: {e}")

if __name__ == "__main__":
    asyncio.run(create_special_users())
