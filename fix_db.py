
import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.core.database import async_engine

async def fix_database():
    print("Fixing Database Enum Mismatch...")
    
    # We need to add 'ADMIN' to the userrole enum and update existing rows.
    # Note: ALTER TYPE ... ADD VALUE cannot be executed in a transaction block.
    # We will try to execute it and ignore 'already exists' errors.
    
    async with async_engine.connect() as conn:
        try:
            # 1. Try to add the value. We use a trick to try and bypass transaction issues if possible,
            # but usually it requires a non-transactional connection.
            # In many setups, simply calling it works if not explicitly in a 'begin' block.
            await conn.execute(text("COMMIT")) # Try to break any existing transaction
            try:
                await conn.execute(text("ALTER TYPE userrole ADD VALUE 'ADMIN'"))
                print("Added 'ADMIN' to userrole enum.")
            except Exception as e:
                # If it already exists, this will fail. We ignore that specific case.
                if "already exists" in str(e):
                    print("'ADMIN' value already exists in userrole enum.")
                else:
                    print(f"Note on ADD VALUE: {e}")
            
            # 2. Update existing lowercase values to uppercase
            print("Updating existing users to standardized uppercase roles...")
            await conn.execute(text("UPDATE users SET role = 'ADMIN' WHERE role::text = 'admin'"))
            await conn.commit()
            print("Database update complete.")
            
        except Exception as e:
            print(f"Error during fix: {e}")
            print("\nIf 'ALTER TYPE' failed due to transaction, please run this manually in your PG console:")
            print("ALTER TYPE userrole ADD VALUE 'ADMIN';")

if __name__ == "__main__":
    asyncio.run(fix_database())
