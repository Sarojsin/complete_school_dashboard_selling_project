import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def check_user():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT id, username, role, is_active FROM users WHERE username = 'saroj'"))
        user = result.fetchone()
        if user:
            print(f"User found: ID={user[0]}, Username={user[1]}, Role={user[2]}, IsActive={user[3]}")
        else:
            print("User 'saroj' not found.")


if __name__ == "__main__":
    asyncio.run(check_user())
