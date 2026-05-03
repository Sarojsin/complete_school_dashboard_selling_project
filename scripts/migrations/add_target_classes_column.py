
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup.core.database import engine

def add_column():
    try:
        with engine.connect() as connection:
            print("Checking if target_classes column exists...")
            # Check if column exists (PostgreSQL specific check, adapting for general SQL if possible or try/catch)
            try:
                # Try simple select to see if it exists
                connection.execute(text("SELECT target_classes FROM assignments LIMIT 1"))
                print("Column 'target_classes' already exists.")
            except Exception:
                # Rollback the failed transaction from the select above
                connection.rollback()
                print("Column 'target_classes' not found. Adding it...")
                # Add the column
                connection.execute(text("ALTER TABLE assignments ADD COLUMN target_classes VARCHAR(255)"))
                connection.commit()
                print("Column 'target_classes' added successfully.")
                
    except Exception as e:
        print(f"Error modifying database: {e}")

if __name__ == "__main__":
    add_column()
