import sqlite3
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%college%' ORDER BY name")
rows = cursor.fetchall()
print("COLLEGE-RELATED TABLES IN school_sell.db:")
for r in rows:
    print(r[0])
if not rows:
    print("(none)")
cursor.execute("SELECT version_num FROM alembic_version")
ver = cursor.fetchone()
print(f"\nAlembic version: {ver[0] if ver else 'not found'}")
conn.close()
