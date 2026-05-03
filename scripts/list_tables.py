"""
List all tables in school_sell_db and college_sell_db

Usage: python scripts/list_tables.py
"""

import sys
import os
from sqlalchemy import create_engine, inspect

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.shared.config import settings

def list_tables(url, db_name):
    """List all tables in a database."""
    try:
        engine = create_engine(url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n{db_name} ({url}):")
        print(f"  Total tables: {len(tables)}")
        for table in sorted(tables):
            print(f"    - {table}")
        engine.dispose()
        return tables
    except Exception as e:
        print(f"\n{db_name}: ERROR - {e}")
        return []

def main():
    print("="*60)
    print("Database Tables Listing")
    print("="*60)
    
    school_url = getattr(settings, 'DATABASE_URL', None) or getattr(settings, 'DATABASE_URL_FIXED', '')
    college_url = getattr(settings, 'COLLEGE_DATABASE_URL', None) or getattr(settings, 'DATABASE_URL_FIXED', '')
    
    if not school_url:
        print("ERROR: DATABASE_URL not configured")
        sys.exit(1)
    
    school_tables = list_tables(school_url, "school_sell_db")
    college_tables = list_tables(college_url, "college_sell_db")
    
    # Check for any overlap
    overlap = set(school_tables) & set(college_tables)
    if overlap:
        print(f"\nWARNING: Tables appear in BOTH databases: {overlap}")
    else:
        print("\nGood: No tables are shared between the two databases.")
    
    print("\n" + "="*60)
    print("Done.")

if __name__ == "__main__":
    main()
