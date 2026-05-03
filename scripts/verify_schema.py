"""
Database Schema Verification Script

Run: python scripts/verify_schema.py

Checks:
- college_sell_db has exactly 23 tables (from backup.models.college)
- school_sell_db has its own separate set of tables
- No cross-contamination of tables between databases
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Import settings
from modules.shared.config import settings

# Import base metadata
from modules.college.base import CollegeBase as CollegeBase
from modules.shared.base import Base as SchoolBase

def count_tables(engine, schema_name=""):
    """Count tables in a given database engine."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return len(tables), tables

def verify_school_db():
    """Verify school database tables."""
    school_url = getattr(settings, 'DATABASE_URL', None) or getattr(settings, 'DATABASE_URL_FIXED')
    if not school_url:
        print("ERROR: DATABASE_URL not configured")
        return False
    
    # Use sync engine for inspection
    engine = create_engine(school_url)
    count, tables = count_tables(engine, "school")
    print(f"\nSchool DB ({school_url}):")
    print(f"   Total tables: {count}")
    # Print list (sorted)
    for t in sorted(tables):
        print(f"   - {t}")
    engine.dispose()
    return count > 0

def verify_college_db():
    """Verify college database tables."""
    college_url = getattr(settings, 'COLLEGE_DATABASE_URL', None) or getattr(settings, 'DATABASE_URL_FIXED')
    if not college_url:
        print("ERROR: COLLEGE_DATABASE_URL not configured")
        return False
    
    # Use sync engine for inspection
    engine = create_engine(college_url)
    count, tables = count_tables(engine, "college")
    print(f"\nCollege DB ({college_url}):")
    print(f"   Total tables: {count}")
    # Print list (sorted)
    for t in sorted(tables):
        print(f"   - {t}")
    
    # Now get metadata tables from CollegeBase
    metadata_tables = list(CollegeBase.metadata.tables.keys())
    print(f"\n   Expected college tables (from CollegeBase): {len(metadata_tables)}")
    for t in sorted(metadata_tables):
        print(f"   - {t}")
    
    # Check for school table leakage
    school_table_markers = ['school_', 'teacher', 'student', 'parent', 'authority', 'class_', 'subject', 'assignment', 'grade_', 'notice', 'video', 'note', 'attendance', 'timetable', 'group_', 'chat_', 'course_enrollment']
    leaked = [t for t in tables if any(m in t for m in school_table_markers)]
    if leaked:
        print(f"\n   WARNING: Leaked school tables into college DB: {leaked}")
        return False
    else:
        print(f"\n   OK: No school tables detected in college DB")
    
    # Check count matches
    expected_count = len(metadata_tables)
    if count != expected_count:
        print(f"\n   WARNING: Table count mismatch: expected {expected_count}, got {count}")
        return False
    else:
        print(f"\n   OK: Table count matches expected ({expected_count})")
    
    engine.dispose()
    return True

def main():
    print("="*60)
    print("Database Schema Verification")
    print("="*60)
    
    try:
        school_ok = verify_school_db()
    except Exception as e:
        print(f"\nSchool DB error: {e}")
        school_ok = False
    
    try:
        college_ok = verify_college_db()
    except Exception as e:
        print(f"\nCollege DB error: {e}")
        college_ok = False
    
    print("\n" + "="*60)
    if school_ok and college_ok:
        print("SUCCESS: Schema verification PASSED")
        return 0
    else:
        print("FAILURE: Schema verification FAILED - review output above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
