
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine

def list_users_raw():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT id, email, role FROM users"))
            print("--- Users in Database ---")
            for row in result:
                # Row structure depends on sqlalchemy version, usually tuple-like or object
                print(f"ID: {row[0]}, Email: {row[1]}, Role: {row[2]}")
                
    except Exception as e:
        print(f"Error querying users: {e}")

if __name__ == "__main__":
    list_users_raw()
