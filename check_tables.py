import sqlite3

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print('Existing tables:')
for table in tables:
    print(f'  - {table[0]}')
print(f'\nTotal tables: {len(tables)}')
conn.close()
