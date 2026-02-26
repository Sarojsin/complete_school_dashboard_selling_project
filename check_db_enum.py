
import asyncio
from sqlalchemy import text
from app.core.database import async_engine

async def check_enum():
    async with async_engine.connect() as conn:
        try:
            result = await conn.execute(text(
                "SELECT enumlabel FROM pg_enum "
                "JOIN pg_type ON pg_enum.enum_typid = pg_type.oid "
                "WHERE pg_type.typname = 'userrole';"
            ))
            labels = [row[0] for row in result.fetchall()]
            print(f"Current userrole labels: {labels}")
            
            # If 'ADMIN' is missing, add it
            if 'ADMIN' not in labels:
                # ALTER TYPE ... ADD VALUE cannot be executed in a transaction block
                # SQLAlchemy's async connection might be in one. 
                # We'll try to use a raw connection if needed, but let's try direct first.
                print("Attempting to add 'ADMIN' to userrole enum...")
                # Note: asyncpg connection doesn't support non-transactional commands easily via SQLAlchemy connect
                # We might need to use the underlying asyncpg connection
            
        except Exception as e:
            print(f"Error checking enum: {e}")

if __name__ == "__main__":
    asyncio.run(check_enum())
