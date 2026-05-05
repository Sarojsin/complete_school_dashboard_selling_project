#!/usr/bin/env python3
import re
from collections import defaultdict, deque

with open('script.txt', 'r') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# Split into statements at semicolon
statements = [s.strip() for s in re.split(r';\s*\n', raw_sql) if s.strip()]

create_table = {}
# alter_deps[tbl] = list of other tables this table depends on via ALTER FKs
alter_deps = defaultdict(list)
indexes = []
others = []

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
        # Get target table
        m = re.search(r'ALTER\s+TABLE\s+(\w+)', stmt_nc, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            # Find all REFERENCES in this ALTER statement
            refs = re.findall(r'REFERENCES\s+(\w+)', stmt_nc, re.IGNORECASE)
            # Keep only those that are tables in our schema and not self-ref
            for r in refs:
                if r in create_table and r != tbl:
                    alter_deps[tbl].append(r)
    elif upper.startswith(('CREATE INDEX', 'CREATE UNIQUE INDEX')):
        indexes.append(stmt_nc)
    else:
        others.append(stmt_nc)

print(f"CREATE TABLE: {len(create_table)}")
print(f"ALTER dependencies collected for {len(alter_deps)} tables")

# Build dependency graph (edges: dependency -> dependent)
graph = defaultdict(list)
in_degree = {tbl: 0 for tbl in create_table}

for tbl, stmt in create_table.items():
    # Inline FKs from CREATE TABLE
    fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
    for ref in fks:
        if ref in create_table and ref != tbl:
            graph[ref].append(tbl)
            in_degree[tbl] = in_degree.get(tbl, 0) + 1
    # ALTER FKs
    for ref in alter_deps.get(tbl, []):
        if ref in create_table and ref != tbl:
            graph[ref].append(tbl)
            in_degree[tbl] = in_degree.get(tbl, 0) + 1

# Ensure all have in_degree
for tbl in create_table:
    in_degree.setdefault(tbl, 0)

# Topological sort
queue = deque([t for t, d in in_degree.items() if d == 0])
sorted_tables = []
while queue:
    node = queue.popleft()
    sorted_tables.append(node)
    for neighbor in graph.get(node, []):
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

# Handle cycles
if len(sorted_tables) < len(create_table):
    cycles = set(create_table.keys()) - set(sorted_tables)
    print(f"WARNING: Cycle involving {len(cycles)} tables: {cycles}")
    for t in create_table:
        if t not in sorted_tables:
            sorted_tables.append(t)

print(f"Sorted {len(sorted_tables)} tables")
print("\nOrder:")
for i, t in enumerate(sorted_tables, 1):
    deps = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', create_table[t], re.IGNORECASE)
    deps += alter_deps.get(t, [])
    ok = all(d in sorted_tables[:i] for d in deps if d in create_table)
    status = "OK" if ok else "FAIL"
    print(f"  {i:3}. {t:40} [{status}]")

# Build final SQL
final_sql = []
for tbl in sorted_tables:
    stmt = create_table[tbl]
    constraints = alter_deps.get(tbl, [])
    if constraints:
        # Get original ALTER constraint definitions for this table (full text)
        # Instead of just refs, we need actual constraint clauses.
        # Collect by scanning statements again for ALTER TABLE tbl
        constraint_clauses = []
        for s in statements:
            s_nc = re.sub(r'--.*', '', s).strip()
            if s_nc.upper().startswith('ALTER TABLE') and f'ALTER TABLE {tbl}' in s_nc:
                # Extract the part after ADD CONSTRAINT(s)
                parts = re.split(r'ADD\s+CONSTRAINT\s+', s_nc)
                for part in parts[1:]:  # skip before first ADD
                    part = part.strip().rstrip(';').rstrip(',')
                    words = part.split(None, 1)
                    if len(words) == 2:
                        constraint_clauses.append(f"CONSTRAINT {words[0]} {words[1]}")
        if constraint_clauses:
            pos = stmt.rfind(')')
            if pos != -1:
                body = stmt[:pos].rstrip()
                if body.endswith(','):
                    body = body[:-1].rstrip()
                block = ',\n  '.join(constraint_clauses)
                stmt = body + ',\n  ' + block + '\n)'
    final_sql.append(stmt + ';')

# Append other statements (CREATE INDEX, etc.) but NOT ALTER TABLEs since they were merged
final_sql.extend(indexes)
# Also include any remaining 'others' statements that are not ALTER TABLE
for stmt in others:
    # Only include if not an ALTER TABLE (should have been caught and merged)
    if not stmt.upper().startswith('ALTER TABLE'):
        final_sql.append(stmt + ';')

with open('school_schema_ordered.sql', 'w') as f:
    f.write('\n\n'.join(final_sql))

print(f"\nTotal statements: {len(final_sql)}")
print("Saved to school_schema_ordered.sql")
