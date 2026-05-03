"""
Data Inventory Script

Run: python scripts/data_inventory.py
Counts all records in all tables before migration.
Save output → compare after migration to verify zero data loss.

Usage:
    python scripts/data_inventory.py > reports/pre_migration_count.txt
    python scripts/data_inventory.py > reports/post_migration_count.txt
"""

from sqlalchemy import text
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup.core.database import SessionLocal

db = SessionLocal()

# List of tables to check - expand based on your actual database schema
TABLES = [
    # Core users
    "users",
    
    # School-related
    "teachers",
    "students",
    "parents",
    "authorities",
    
    # Academic
    "exams",
    "tests",
    "courses",
    "departments",
    "classes",
    "sections",
    
    # Fees & Accounts
    "fees",
    "accounts",
    "fee_structures",
    "fee_payments",
    
    # Library
    "library_books",
    "book_issues",
    
    # Attendance
    "attendance_records",
    "attendance_sessions",
    
    # College-specific
    "college_students",
    "faculty",
    "departments",
    "programs",
    "semesters",
    "enrollments",
    
    # Hostel
    "hostels",
    "hostel_rooms",
    "hostel_allocations",
    
    # Labs
    "labs",
    "lab_equipment",
    
    # Placement
    "placement_drives",
    "placement_applications",
    
    # Chat & Groups
    "chat_rooms",
    "chat_messages",
    "chat_participants",
    "groups",
    "group_posts",
    
    # Notices & Notifications
    "notices",
    "notifications",
    
    # Admin
    "system_settings",
    "features",
    "audit_logs",
    "system_backups",
]

print("=" * 50)
print("📊 DATA INVENTORY — Pre-Migration")
print("=" * 50)
print()

total = 0
for table in TABLES:
    try:
        # Use text() for raw SQL to avoid ORM issues
        result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        print(f"  {table:<35} {count:>8} rows")
        total += count
    except Exception as e:
        print(f"  {table:<35} {'ERROR':>8} ({str(e)[:50]})")

print()
print("-" * 50)
print(f"  {'TOTAL':<35} {total:>8} rows")
print("=" * 50)

db.close()

print()
print("💾 Save this output to compare after migration:")
print("   python scripts/data_inventory.py > reports/pre_migration_count.txt")
