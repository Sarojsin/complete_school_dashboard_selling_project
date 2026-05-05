import re
from collections import defaultdict, deque

with open('script.txt', 'r') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

statements = [s.strip() for s in re.split(r';\s*\n', raw_sql) if s.strip()]

create_table = {}
alters = defaultdict(list)

for stmt in statements:
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if not stmt_nc:
        continue
    upper = stmt_nc.upper()
    if upper.startswith('CREATE TABLE'):
        m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt_nc, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            create_table[tbl] = stmt_nc

# Show CREATE for school_classes
print("school_classes statement excerpt:")
stmt = create_table['school_classes']
# Find all FKs
fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
print(f"  FK references: {fks}")

# Check teachers
print("\nteachers statement excerpt:")
stmt2 = create_table['teachers']
fks2 = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt2, re.IGNORECASE)
print(f"  FK references: {fks2}")

print("\nAll tables and their FK refs:")
for tbl, stmt in create_table.items():
    refs = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
    if refs:
        print(f"  {tbl}: {refs}")
