import asyncio
import logging
from backup.core.database import AsyncSessionLocal
from sqlalchemy import text

async def test_db():
    logging.basicConfig(level=logging.INFO)
    try:
        async with AsyncSessionLocal() as session:
            # Check connection
            print("Checking connection...")
            res = await session.execute(text("SELECT 1"))
            print(f"Connection OK: {res.scalar()}")
            
            # Check users table
            print("Checking users table...")
            res = await session.execute(text("SELECT COUNT(*) FROM users"))
            print(f"User count: {res.scalar()}")
            
            # List some users
            res = await session.execute(text("SELECT id, username, email, role FROM users LIMIT 5"))
            users = res.fetchall()
            for user in users:
                print(f"User: ID={user[0]}, Name={user[1]}, Email={user[2]}, Role={user[3]}")
                
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db())
