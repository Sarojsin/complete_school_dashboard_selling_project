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
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            print(f"\n--- ALTER for {tbl} ---")
            print(f"  cname: {cname}")
            print(f"  cdef: {cdef}")
            alters[tbl].append(cdef)

print("\n\n== Summary of ALTER FKs ==")
for tbl, defs in alters.items():
    all_refs = []
    for d in defs:
        refs = re.findall(r'REFERENCES\s+(\w+)', d, re.IGNORECASE)
        all_refs.extend(refs)
    if all_refs:
        print(f"{tbl}: {all_refs}")
