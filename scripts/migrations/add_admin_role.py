"""
Migration script to add ADMIN role to the database enum
"""
import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from sqlalchemy import text
from backup.core.database import engine


def add_admin_role():
    """Add ADMIN to userrole enum if it doesn't exist"""
    with engine.connect() as conn:
        # Check if ADMIN already exists
        result = conn.execute(text("""
            SELECT 1 FROM pg_enum 
            WHERE enumlabel = 'ADMIN' 
            AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')
        """))
        
        if result.fetchone():
            print("ADMIN role already exists in database")
            return
            
        # Add ADMIN to enum
        conn.execute(text("""
            ALTER TYPE userrole ADD VALUE 'ADMIN'
        """))
        conn.commit()
        print("Successfully added ADMIN role to database")


if __name__ == "__main__":
    add_admin_role()
