import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# For existing users, default to 'school' portal.
# New registrations will include portal_type.
cursor.execute("UPDATE users SET portal_type = 'school' WHERE portal_type IS NULL")

conn.commit()
conn.close()
print("Backfill complete - all existing users set to school portal")
