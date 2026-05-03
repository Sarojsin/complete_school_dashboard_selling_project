import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_portal_type ON users(portal_type)')
conn.commit()
conn.close()
print("Index created")
