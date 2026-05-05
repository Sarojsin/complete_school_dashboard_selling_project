"""
Summary of College Database Schema
Based on alembic_college migrations
"""

# Tables from 1f0fc964eedc_initial_college_base_schema.py (base college tables)
base_tables = [
    "college_departments",
    "college_faculty", 
    "college_programs",
    "college_semesters",
    "college_courses",
    "college_students",
    "college_enrollments",
    "hostels",
    "rooms",
    "hostel_allocations",
    "hostel_complaints",
    "labs",
    "lab_equipment",
    "lab_schedules",
    "placement_companies",
    "placement_jobs",
    "placement_applications",
    "research_projects",
    "research_publications",
    "research_patents",
]

# Tables from 20260505_add_exam_account_tables.py (new module tables)
new_module_tables = [
    "college_exam_results",
    "college_exam_notices",
    "college_faculty_payments",
]

# Also there might be additional fee tables from backup models
fee_tables = [
    "college_fee_structures",
    "college_fee_records",
]

all_expected_tables = base_tables + new_module_tables + fee_tables

print(f"Base college tables: {len(base_tables)}")
for t in base_tables:
    print(f"  - {t}")

print(f"\nNew module tables: {len(new_module_tables)}")
for t in new_module_tables:
    print(f"  - {t}")

print(f"\nFee tables (from backup models, not in college migrations): {len(fee_tables)}")
for t in fee_tables:
    print(f"  - {t}")

print(f"\nTotal expected college tables: {len(all_expected_tables)}")

# Check school_sell.db for any college tables
import sqlite3
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
existing_tables = [r[0] for r in cursor.fetchall()]
existing_college = [t for t in existing_tables if t.startswith('college_')]
print(f"\nExisting college_* tables in school_sell.db: {len(existing_college)}")
for t in existing_college:
    print(f"  - {t}")

missing = [t for t in all_expected_tables if t not in existing_tables]
print(f"\nMissing college tables: {len(missing)}")
for t in missing:
    print(f"  - {t}")

conn.close()
