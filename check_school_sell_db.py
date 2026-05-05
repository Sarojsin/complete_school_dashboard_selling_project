import sqlite3
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
rows = cursor.fetchall()
print("ALL TABLES IN school_sell.db:")
for r in rows:
    print(r[0])
conn.close()
