import asyncio
from sqlalchemy import text
from backup.core.database import AsyncSessionLocal

async def check_enum():
    async with AsyncSessionLocal() as session:
        try:
            print("Checking userrole enum values...")
            # PostgreSQL specific query to list enum values
            result = await session.execute(text("SELECT unnest(enum_range(NULL::userrole))"))
            enums = result.fetchall()
            print(f"Current Enum Values: {[e[0] for e in enums]}")
            
            print("\nChecking raw role value for saroj...")
            res = await session.execute(text("SELECT role FROM users WHERE username = 'saroj'"))
            role = res.scalar()
            print(f"Saroj raw role in DB: {role} (Type: {type(role)})")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_enum())
