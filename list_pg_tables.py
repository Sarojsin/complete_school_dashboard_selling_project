import subprocess

conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'

# Get all tables
result = subprocess.run(
    ['psql', conn_str, '-t', '-c',
     "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"],
    capture_output=True, text=True
)
tables = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]

print(f"Total tables: {len(tables)}\n")
for t in tables:
    print(f"  {t}")

# Expected non-school tables: users, teachers, groups, notices, periods, tests, chat_messages, exam_notices, exam_results
non_school = {'users','teachers','groups','notices','periods','tests','chat_messages','exam_notices','exam_results'}
school_star = [t for t in tables if t.startswith('school_')]
print(f"\nschool_* tables: {len(school_star)}")
print(f"Non-school expected: {len(non_school)} found: {len([t for t in tables if t in non_school])}")
print(f"Total: {len(tables)}")
