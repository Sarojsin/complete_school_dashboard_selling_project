import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def check_roles():
    async with AsyncSessionLocal() as session:
        # Check for Library Manager
        print("--- Checking for Library Managers ---")
        result = await session.execute(text("SELECT id, username, email, role FROM users WHERE role = 'library_manager'"))
        users = result.fetchall()
        if users:
            for user in users:
                print(f"Library Manager found: ID={user[0]}, Username={user[1]}, Email={user[2]}")
        else:
            print("No Library Manager users found.")

        # Check for Account Section
        print("\n--- Checking for Account Section users ---")
        result = await session.execute(text("SELECT id, username, email, role FROM users WHERE role = 'account_section'"))
        users = result.fetchall()
        if users:
            for user in users:
                print(f"Account Section user found: ID={user[0]}, Username={user[1]}, Email={user[2]}")
        else:
            print("No Account Section users found.")

if __name__ == "__main__":
    asyncio.run(check_roles())
