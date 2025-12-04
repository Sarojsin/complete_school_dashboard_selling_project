import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy import text
from database.database import engine

def add_parent_to_enum():
    with engine.connect() as conn:
        # Check if PARENT already exists
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'userrole' AND e.enumlabel = 'PARENT';
        """))
        
        if result.fetchone():
            print("PARENT already exists in userrole enum")
        else:
            print("Adding PARENT to userrole enum...")
            conn.execute(text("ALTER TYPE userrole ADD VALUE 'PARENT'"))
            conn.commit()
            print("✓ PARENT added successfully")
        
        # Verify
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'userrole'
            ORDER BY e.enumsortorder;
        """))
        
        print("\nCurrent userrole enum values:")
        for row in result:
            print(f"  - {row[0]}")

if __name__ == "__main__":
    add_parent_to_enum()
