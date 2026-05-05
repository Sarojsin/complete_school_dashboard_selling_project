import sqlite3
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f'Created {len(tables)} tables:')
for t in tables:
    print(f'  {t[0]}')
conn.close()
