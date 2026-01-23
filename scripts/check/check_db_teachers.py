
import asyncio
from app.core.database import async_engine
from sqlalchemy import text

async def check_teachers():
    async with async_engine.connect() as conn:
        print("--- Teachers Table ---")
        try:
            res = await conn.execute(text("SELECT id, user_id, employee_id, full_name, status FROM teachers"))
            rows = res.fetchall()
            if not rows:
                print("No teachers found.")
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error reading teachers: {e}")
            
        print("\n--- Users Table (Teachers) ---")
        try:
            res = await conn.execute(text("SELECT id, email, role FROM users"))
            for row in res.fetchall():
                if str(row.role).lower() == 'teacher':
                    print(row)
        except Exception as e:
            print(f"Error reading users: {e}")

if __name__ == "__main__":
    asyncio.run(check_teachers())
