import sqlite3
conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
rows = cursor.fetchall()
print("SCHOOL DB TABLES:")
for r in rows:
    print(r[0])
conn.close()
