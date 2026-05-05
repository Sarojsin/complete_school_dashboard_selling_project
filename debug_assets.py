import re
from collections import defaultdict

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
            create_table[m.group(1)] = stmt_nc
    elif upper.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in upper:
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', stmt_nc, re.IGNORECASE)
        if m:
            alters[m.group(1)].append(m.group(3).rstrip(', '))

asset_tables = ['school_asset_categories', 'school_assets', 'school_asset_assignments', 'school_asset_maintenance_logs']
for tbl in asset_tables:
    print(f"\n{tbl}:")
    if tbl in create_table:
        fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', create_table[tbl], re.IGNORECASE)
        print(f"  CREATE refs: {fks}")
    for alt in alters.get(tbl, []):
        refs = re.findall(r'REFERENCES\s+(\w+)', alt, re.IGNORECASE)
        print(f"  ALTER refs: {refs}  (in: {alt[:80]})")

# Also check school_students and school_classes
print("\n\nschool_students ALTER refs:")
for alt in alters.get('school_students', []):
    refs = re.findall(r'REFERENCES\s+(\w+)', alt, re.IGNORECASE)
    print(f"  {refs}: {alt[:100]}")
print("\nschool_classes ALTER refs:")
for alt in alters.get('school_classes', []):
    refs = re.findall(r'REFERENCES\s+(\w+)', alt, re.IGNORECASE)
    print(f"  {refs}: {alt[:100]}")
