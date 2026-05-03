import os
import sys

# Add the project root to sys.path to import local modules
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backup.core.database import engine
from sqlalchemy import text


def run_migration():
    print(f"Using engine: {engine.url}")
    with engine.connect() as connection:
        try:
            print("Adding profile_picture column to users table...")
            connection.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255);"))
            connection.commit()
            print("Successfully added profile_picture column.")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                print("Column profile_picture already exists.")
            else:
                print(f"Error: {e}")


if __name__ == "__main__":
    run_migration()