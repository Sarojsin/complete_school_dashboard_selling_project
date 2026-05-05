import sqlite3

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
rows = cursor.fetchall()
for row in rows:
    print(row[0])
conn.close()
