import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def clean_school_db():
    print("Cleaning school_sell_db...")
    url = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://").replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_async_engine(url)
    
    # Tables to drop
    tables = [
        "college_enrollments",
        "college_courses",
        "college_programs",
        "college_semesters",
        "college_departments",
        "college_faculty",
        "college_students"
    ]
    
    async with engine.begin() as conn:
        for table in tables:
            print(f"Dropping {table}...")
            await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
            
    await engine.dispose()
    print("Done cleaning school_sell_db.")

async def init_college_db():
    print("Ensuring college_sell_db exists...")
    # Connect to the default postgres database to create college_sell_db
    default_url = "postgresql+asyncpg://user:tara@localhost:5432/postgres"
    engine = create_async_engine(default_url, isolation_level="AUTOCOMMIT")
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'college_sell_db'"))
        exists = result.scalar()
        if not exists:
            print("Creating database college_sell_db...")
            await conn.execute(text("CREATE DATABASE college_sell_db"))
        else:
            print("college_sell_db already exists.")
            
    await engine.dispose()

async def main():
    try:
        await clean_school_db()
    except Exception as e:
        print(f"Error cleaning school_sell_db: {e}")
        
    try:
        await init_college_db()
    except Exception as e:
        print(f"Error ensuring college_sell_db: {e}")

if __name__ == "__main__":
    asyncio.run(main())
