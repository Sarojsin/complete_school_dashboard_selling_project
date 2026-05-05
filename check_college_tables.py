import sqlite3

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'college_%' ORDER BY name")
rows = cursor.fetchall()
print('College tables count:', len(rows))
for row in rows:
    print(row[0])
conn.close()
