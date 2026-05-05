import sqlite3
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()

# Check for both naming conventions
migration_names = [
    "placement_companies", "placement_jobs", "placement_applications",
    "research_publications", "research_patents",
    "labs"
]
backup_names = [
    "companies", "jobs", "applications",
    "publications", "patents",
    "college_labs"
]

print("Checking for placement/research/lab tables in school_sell.db:\n")
all_found = []
for t in migration_names + backup_names:
    cursor.execute(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{t}'")
    exists = cursor.fetchone() is not None
    if exists:
        print(f"  FOUND: {t}")
        all_found.append(t)

if not all_found:
    print("  (none of these tables exist)")

conn.close()
