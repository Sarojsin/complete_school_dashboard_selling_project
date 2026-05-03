import asyncio
from sqlalchemy import text
from backup.core.database import AsyncSessionLocal

async def add_enum_values():
    # Enums to add
    new_roles = ["HOD", "EXAM_SECTION", "LIBRARY_MANAGER", "ACCOUNT_SECTION"]
    
    async with AsyncSessionLocal() as session:
        print("Starting Enum Update...")
        for role in new_roles:
            try:
                # We must run this as a transaction that commits immediately or autocommits
                # But ALTER TYPE cannot run inside a transaction block in some scenarios.
                # However, with asyncpg/sqlalchemy, session.execute() + commit() usually works unless it's strictly disallowed 
                # (Postgres < 12 didn't allow inside transaction, newer might).
                # The generic way is to try.
                print(f"Adding value: {role}")
                await session.execute(text(f"ALTER TYPE userrole ADD VALUE IF NOT EXISTS '{role}'"))
                await session.commit()
                print(f"Added {role}")
            except Exception as e:
                print(f"Could not add {role}: {e}")
                # We continue to next one
        
        print("Enum update process finished.")

if __name__ == "__main__":
    asyncio.run(add_enum_values())
