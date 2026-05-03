import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def reset_college_db_alembic():
    print("Resetting alembic_version table in college_sell_db...")
    url = "postgresql+asyncpg://user:tara@localhost:5432/college_sell_db"
    engine = create_async_engine(url)
    
    async with engine.begin() as conn:
        print("Dropping alembic_version table if it exists...")
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
            
    await engine.dispose()
    print("Done resetting.")

if __name__ == "__main__":
    asyncio.run(reset_college_db_alembic())
