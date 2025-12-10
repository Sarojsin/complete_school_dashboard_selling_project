import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy import text
from database.database import engine

def check_enum():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'userrole'
            ORDER BY e.enumsortorder;
        """))
        
        print("Database userrole enum values:")
        for row in result:
            print(f"  - {row[0]}")

if __name__ == "__main__":
    check_enum()
