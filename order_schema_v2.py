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
            create_table[m.group(1)] = stmt_nc
    elif upper.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in upper:
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', stmt_nc, re.IGNORECASE)
        if m:
            alters[m.group(1)].append(f"CONSTRAINT {m.group(2)} {m.group(3).rstrip(', ')}")

# Build graph: edge A -> B means A depends on B (B must come before A)
graph = defaultdict(list)
in_degree = {tbl: 0 for tbl in create_table}

for tbl, stmt in create_table.items():
    # Extract FOREIGN KEY references from CREATE TABLE
    fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
    # Also extract from ALTER TABLE constraints for this table
    for alter_stmt in alters.get(tbl, []):
        alter_refs = re.findall(r'REFERENCES\s+(\w+)', alter_stmt, re.IGNORECASE)
        fks.extend(alter_refs)
    for ref in fks:
        if ref in create_table and ref != tbl:  # Skip self-referential FKs
            graph[ref].append(tbl)
            in_degree[tbl] = in_degree.get(tbl, 0) + 1

# Ensure all nodes in in_degree
for tbl in create_table:
    if tbl not in in_degree:
        in_degree[tbl] = 0

# Topological sort (Kahn)
queue = deque([t for t, d in in_degree.items() if d == 0])
sorted_tables = []
while queue:
    node = queue.popleft()
    sorted_tables.append(node)
    for neighbor in graph.get(node, []):
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

# Check for cycles
if len(sorted_tables) < len(create_table):
    cycles = set(create_table.keys()) - set(sorted_tables)
    print(f"WARNING: Cycle detected involving {len(cycles)} tables: {cycles}")
    # Break cycles by arbitrarily adding remaining
    for t in create_table:
        if t not in sorted_tables:
            sorted_tables.append(t)

print(f"Sorted {len(sorted_tables)} tables")
print("\nOrder:")
for i, t in enumerate(sorted_tables, 1):
    deps = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', create_table[t], re.IGNORECASE)
    ok = all(d in sorted_tables[:i] for d in deps if d in create_table)
    status = "OK" if ok else "WRONG ORDER"
    print(f"  {i:3}. {t:40} [{status}]")

# Build final SQL
final_sql = []
for tbl in sorted_tables:
    stmt = create_table[tbl]
    # Merge ALTER constraints
    constraints = alters.get(tbl, [])
    if constraints:
        pos = stmt.rfind(')')
        if pos != -1:
            body = stmt[:pos].rstrip()
            # Remove any trailing comma from body
            if body.endswith(','):
                body = body[:-1].rstrip()
            # Build constraints block: each constraint separated by comma
            constraint_block = ',\n  '.join(constraints)
            stmt = body + ',\n  ' + constraint_block + '\n)'
    final_sql.append(stmt + ';')

# Append CREATE INDEX statements
for stmt in statements:
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if stmt_nc.upper().startswith(('CREATE INDEX', 'CREATE UNIQUE INDEX')):
        # Remove partial indexes (WHERE) - not supported in PG? They are fine in PG actually keep them
        # But remove stray GIN references that are already removed? Keep as-is for PostgreSQL
        final_sql.append(stmt_nc + ';')

with open('school_schema_ordered.sql', 'w') as f:
    f.write('\n\n'.join(final_sql))

print(f"\nTotal statements: {len(final_sql)}")
print("Saved school_schema_ordered.sql")
