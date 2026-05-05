import sqlite3
conn = sqlite3.connect('school_sell.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]
print(f'Total: {len(tables)} tables')
print('All tables:')
for t in tables:
    print(f'  {t}')
conn.close()
