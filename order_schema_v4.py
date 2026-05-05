#!/usr/bin/env python3
import re
from collections import defaultdict, deque

with open('script.txt', 'r') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# Split into raw statements first at semicolons
raw_statements = []
buffer = []
for line in raw_sql.split('\n'):
    if ';' in line:
        buffer.append(line)
        full_stmt = ' '.join(buffer).strip()
        if full_stmt:
            raw_statements.append(full_stmt)
        buffer = []
    else:
        buffer.append(line)
if buffer:
    raw_statements.append(' '.join(buffer).strip())

create_table = {}
# First pass: identify CREATE TABLE statements (might be single or multi-line in raw_statements)
for stmt in raw_statements:
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if not stmt_nc:
        continue
    m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt_nc, re.IGNORECASE)
    if m:
        create_table[m.group(1)] = stmt_nc
print(f"Found {len(create_table)} CREATE TABLE statements")
print(f"Found {len(create_table)} CREATE TABLE statements")

# Pass 2: collect ALTER TABLE constraints (maybe spanning multiple lines in raw_statements)
for i, stmt in enumerate(raw_statements):
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if not stmt_nc:
        continue
    if stmt_nc.upper().startswith('ALTER TABLE'):
        # Get table name
        m = re.search(r'ALTER\s+TABLE\s+(\w+)', stmt_nc, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            # This is the start of an ALTER block. Collect this and subsequent statements that begin with ADD CONSTRAINT
            alter_block = stmt_nc
            j = i + 1
            while j < len(raw_statements):
                next_stmt = raw_statements[j].strip()
                next_nc = re.sub(r'--.*', '', next_stmt).strip()
                if next_nc.upper().startswith('ADD CONSTRAINT'):
                    alter_block += ' ' + next_nc
                    j += 1
                else:
                    break
            # Extract all table references from the full block
            refs = extract_fks_from_alter(alter_block)
            alter_deps[tbl].extend(refs)
    elif stmt_nc.upper().startswith(('CREATE INDEX', 'CREATE UNIQUE INDEX')):
        indexes.append(stmt_nc)

# Build graph
graph = defaultdict(list)
in_degree = {tbl: 0 for tbl in create_table}

for tbl, stmt in create_table.items():
    # Inline FKs in CREATE TABLE
    fks = re.findall(r'FOREIGN\s+KEY\s*\([^)]*\)\s+REFERENCES\s+(\w+)', stmt, re.IGNORECASE)
    for ref in fks:
        if ref in create_table and ref != tbl and ref not in graph[tbl]:
            graph[ref].append(tbl)
            in_degree[tbl] = in_degree.get(tbl, 0) + 1
    # ALTER FKs
    for ref in alter_deps.get(tbl, []):
        if ref in create_table and ref != tbl and ref not in graph[tbl]:
            graph[ref].append(tbl)
            in_degree[tbl] = in_degree.get(tbl, 0) + 1

for tbl in create_table:
    in_degree.setdefault(tbl, 0)

# Toposort
queue = deque([t for t, d in in_degree.items() if d == 0])
sorted_tables = []
while queue:
    node = queue.popleft()
    sorted_tables.append(node)
    for neighbor in graph.get(node, []):
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

if len(sorted_tables) < len(create_table):
    cycles = set(create_table.keys()) - set(sorted_tables)
    print(f"WARNING: Cycle in {len(cycles)} tables: {cycles}")
    for t in create_table:
        if t not in sorted_tables:
            sorted_tables.append(t)

# Build final SQL
final_sql = []
# Pre-pass: collect complete ALTER statements for each table
alter_statements = {}
i = 0
while i < len(raw_statements):
    stmt = raw_statements[i]
    stmt_nc = re.sub(r'--.*', '', stmt).strip()
    if not stmt_nc:
        i += 1
        continue
    if stmt_nc.upper().startswith('ALTER TABLE'):
        m = re.search(r'ALTER\s+TABLE\s+(\w+)', stmt_nc, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            block = stmt_nc
            j = i + 1
            while j < len(raw_statements):
                next_nc = re.sub(r'--.*', '', raw_statements[j]).strip()
                if next_nc.upper().startswith('ADD CONSTRAINT'):
                    block += ' ' + next_nc
                    j += 1
                else:
                    break
            alter_statements[tbl] = block
            i = j
            continue
    i += 1
            i = j
            continue
    i += 1

for tbl in sorted_tables:
    stmt = create_table[tbl]
    if tbl in alter_statements:
        # Insert the ALTER's constraints into the CREATE before closing )
        pos = stmt.rfind(')')
        if pos != -1:
            body = stmt[:pos].rstrip()
            # Extract constraint parts from the ALTER block
            alter_sql = alter_statements[tbl]
            # Split by ADD CONSTRAINT and rebuild
            parts = re.split(r'ADD\s+CONSTRAINT\s+', alter_sql, flags=re.IGNORECASE)
            clauses = []
            for part in parts[1:]:
                part = part.strip().rstrip(';').rstrip(',')
                words = part.split(None, 1)
                if len(words) == 2:
                    clauses.append(f"CONSTRAINT {words[0]} {words[1]}")
            if clauses:
                if body.endswith(','):
                    body = body[:-1].rstrip()
                block = ',\n  '.join(clauses)
                stmt = body + ',\n  ' + block + '\n)'
    final_sql.append(stmt + ';')

final_sql.extend(indexes)

with open('school_schema_ordered.sql', 'w') as f:
    f.write('\n\n'.join(final_sql))

print(f"Generated {len(final_sql)} statements (including {len(sorted_tables)} tables)")
