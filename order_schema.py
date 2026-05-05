import re
from collections import defaultdict, deque

# Load script.txt
with open('script.txt', 'r') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# Split into statements properly - split on semicolon
raw_statements = [s.strip() for s in re.split(r';\s*\n', raw_sql) if s.strip()]

# Categorize
create_table = {}
alters = defaultdict(list)
indexes = []
others = []

for stmt in raw_statements:
    # Remove inline comments
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if not stmt_nc:
        continue
    upper = stmt_nc.upper()
    if upper.startswith('CREATE TABLE'):
        m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt_nc, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            create_table[tbl] = stmt_nc
    elif upper.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in upper:
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', stmt_nc, re.IGNORECASE)
        if m:
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            alters[tbl].append(f"CONSTRAINT {cname} {cdef}")
    elif upper.startswith(('CREATE INDEX', 'CREATE UNIQUE INDEX')):
        indexes.append(stmt_nc)
    else:
        others.append(stmt_nc)

print(f"CREATE TABLE: {len(create_table)}")
print(f"ALTER constraints: {sum(len(v) for v in alters.values())}")
print(f"Indexes: {len(indexes)}")

# Build dependency graph from foreign keys in CREATE TABLE statements
def extract_fks(stmt):
    # Find all table references in FOREIGN KEY clauses
    fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
    return fks

# Topological sort
in_degree = {tbl: 0 for tbl in create_table}
for tbl, stmt in create_table.items():
    deps = extract_fks(stmt)
    for dep in deps:
        if dep in in_degree:
            in_degree[dep] += 1  # increment dependency count (actually out-degree tracking? Let's do proper in-degree)
        # else: dep might not be in our set, ignore

# Actually compute in-degree properly
graph = defaultdict(list)
for tbl, stmt in create_table.items():
    deps = extract_fks(stmt)
    for dep in deps:
        if dep in create_table:
            graph[dep].append(tbl)  # dep -> tbl edge
            in_degree[tbl] = in_degree.get(tbl, 0) + 1

# Ensure all tables have in_degree entry
for tbl in create_table:
    if tbl not in in_degree:
        in_degree[tbl] = 0

# Kahn's algorithm
queue = deque([tbl for tbl, deg in in_degree.items() if deg == 0])
sorted_tables = []
while queue:
    tbl = queue.popleft()
    sorted_tables.append(tbl)
    for neighbor in graph.get(tbl, []):
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

if len(sorted_tables) < len(create_table):
    # Cycle detected - add remaining
    missing = set(create_table.keys()) - set(sorted_tables)
    sorted_tables.extend(sorted(missing))
    print(f"\nWARNING: Cycle detected, added {len(missing)} tables arbitrarily")

print(f"\nDependency order ({len(sorted_tables)} tables):")
for t in sorted_tables:
    deps = extract_fks(create_table[t])
    if any(d not in sorted_tables[:sorted_tables.index(t)] for d in deps if d in create_table):
        print(f"  WARNING: {t} may have forward ref: {deps}")
    else:
        print(f"  {t}")

# Save ordered schema
ordered_sql = []
for tbl in sorted_tables:
    stmt = create_table[tbl]
    # Merge ALTER constraints inline BEFORE the closing )
    # Find the closing parenthesis
    constraints = alters.get(tbl, [])
    if constraints:
        # Insert constraints before closing ')'
        pos = stmt.rfind(')')
        if pos != -1:
            body = stmt[:pos].rstrip()
            if body.endswith(','):
                body = body[:-1]
            constraint_block = '\n  ' + ',\n  '.join(constraints)
            # Add comma before first constraint if body doesn't end with comma
            if not body.endswith(','):
                body += ','
            stmt = body + constraint_block + '\n)'
    ordered_sql.append(stmt + ';')

# Add indexes after all tables
ordered_sql.extend(indexes)
ordered_sql.extend(others)

with open('school_schema_ordered.sql', 'w') as f:
    f.write('\n\n'.join(ordered_sql))

print(f"\nTotal statements: {len(ordered_sql)}")
print("Saved to school_schema_ordered.sql")
