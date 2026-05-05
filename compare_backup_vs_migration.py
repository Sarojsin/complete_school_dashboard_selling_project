import importlib
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load backup models module
backup_pkg = importlib.import_module('backup.models.college')

# Get all classes with __tablename__
backup_tables = {}
for name in dir(backup_pkg):
    obj = getattr(backup_pkg, name)
    if hasattr(obj, '__tablename__') and hasattr(obj, '__table__'):
        backup_tables[obj.__tablename__] = name

# Expected from migrations (both college migrations)
migration_tables = [
    # 1f0fc964eedc
    "college_departments","college_faculty","college_programs","college_semesters",
    "college_courses","college_students","college_enrollments",
    "hostels","rooms","hostel_allocations","hostel_complaints",
    "labs","lab_equipment","lab_schedules",
    "placement_companies","placement_jobs","placement_applications",
    "research_projects","research_publications","research_patents",
    # 20260505_add_exam_account_tables
    "college_exam_results","college_exam_notices","college_faculty_payments",
]

print("Tables in backup models but NOT in college migrations:")
missing_from_migration = set(backup_tables.keys()) - set(migration_tables)
for t in sorted(missing_from_migration):
    print(f"  - {t} (model: {backup_tables[t]})")

print("\nTables in migrations but NOT in backup models:")
extra_in_migration = set(migration_tables) - set(backup_tables.keys())
for t in sorted(extra_in_migration):
    print(f"  - {t}")

print("\nTables that have name mismatches (same table, different name):")
# This is approximate - we check if similar names exist
mapping = {
    "college_labs": "labs",
    "companies": "placement_companies",
    "jobs": "placement_jobs",
    "applications": "placement_applications",
    "publications": "research_publications",
    "patents": "research_patents",
}
for backup_name, mig_name in mapping.items():
    if backup_name in backup_tables and mig_name in migration_tables:
        print(f"  backup: {backup_name}  <-->  migration: {mig_name}")
