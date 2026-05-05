import sqlite3
import re
from collections import defaultdict, OrderedDict

# -------------------------------------------------------------
# Load source
# -------------------------------------------------------------
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)
lines = raw_sql.split('\n')
print(f"Total lines: {len(lines)}")

# -------------------------------------------------------------
# Pass 1: Collect ALTER TABLE constraints, mark lines to skip
# -------------------------------------------------------------
alter_constraints = defaultdict(list)  # table -> list of "CONSTRAINT name definition"
skip_lines = set()  # line indices to exclude
current_alter_table = None

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Skip comment-only lines generally, but still process if they contain keywords? ignore
    if stripped.startswith('--') or not stripped:
        continue
    
    # Detect start of ALTER TABLE
    if stripped.upper().startswith('ALTER TABLE'):
        # extract table name
        m = re.search(r'ALTER\s+TABLE\s+(\w+)', stripped, re.IGNORECASE)
        if m:
            current_alter_table = m.group(1)
        else:
            current_alter_table = None
        skip_lines.add(i)
        # Check if same line also has ADD CONSTRAINT
        after = stripped[m.end():].strip()
        if after.upper().startswith('ADD CONSTRAINT'):
            after2 = after[len('ADD CONSTRAINT'):].strip()
            parts = after2.split(None, 1)
            if len(parts) == 2:
                cname, cdef = parts[0], parts[1].rstrip(',; ')
                alter_constraints[current_alter_table].append(f"  CONSTRAINT {cname} {cdef}")
            if ';' in stripped:
                current_alter_table = None
        continue
    
    # If we are inside an ALTER block (current_alter_table set)
    if current_alter_table:
        skip_lines.add(i)
        if stripped.upper().startswith('ADD CONSTRAINT'):
            after = stripped[len('ADD CONSTRAINT'):].strip()
            parts = after.split(None, 1)
            if len(parts) == 2:
                cname, cdef = parts[0], parts[1].rstrip(',; ')
                alter_constraints[current_alter_table].append(f"  CONSTRAINT {cname} {cdef}")
            # If line ends with semicolon, block ends
            if ';' in stripped:
                current_alter_table = None
        else:
            # Could be a line with just a comma or something; ignore
            if ';' in stripped:
                current_alter_table = None
        continue

print(f"Collected constraints for {len(alter_constraints)} tables, skipping {len(skip_lines)} lines")

# -------------------------------------------------------------
# Pass 2: Assemble statements (buffer until semicolon)
# -------------------------------------------------------------
raw_statements = []
buffer = []
for i, line in enumerate(lines):
    if i in skip_lines:
        continue
    # Remove inline comments
    line_nc = re.sub(r'--.*', '', line)
    buffer.append(line_nc)
    if ';' in line_nc:
        stmt = ' '.join(buffer).strip()
        if stmt:
            raw_statements.append(stmt)
        buffer = []
if buffer:
    stmt = ' '.join(buffer).strip()
    if stmt:
        raw_statements.append(stmt)

print(f"Raw statements (after removing ALTER): {len(raw_statements)}")

# -------------------------------------------------------------
# Pass 3: Categorize statements
# -------------------------------------------------------------
create_table_stmts = OrderedDict()
other_statements = []

for stmt in raw_statements:
    stmt_upper = stmt.upper()
    if stmt_upper.startswith('CREATE TABLE'):
        m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            create_table_stmts[tbl] = stmt
    elif stmt_upper.startswith('CREATE INDEX') or stmt_upper.startswith('CREATE UNIQUE INDEX'):
        other_statements.append(stmt)
    # Others like COMMENT? ignore

print(f"CREATE TABLE found: {len(create_table_stmts)}")
print(f"Other statements: {len(other_statements)}")

# -------------------------------------------------------------
# Conversion helpers
# -------------------------------------------------------------
def convert_sql(text):
    text = re.sub(r'\bBIGSERIAL\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSERIAL\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBIGINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bVARCHAR\([^)]*\)\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bCHAR\([^)]*\)\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDECIMAL\([^)]*\)\b', 'REAL', text, flags=re.IGNORECASE)
    text = re.sub(r'\bNUMERIC\([^)]*\)\b', 'REAL', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTIMESTAMP\b', 'DATETIME', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJSONB?\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bINET\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTSVECTOR\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBYTEA\b', 'BLOB', text, flags=re.IGNORECASE)
    text = re.sub(r'\bUUID\b', 'TEXT', text, flags=re.IGNORECASE)
    # Defaults
    text = text.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    text = text.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    text = re.sub(r'\bDEFAULT\s+TRUE\b', 'DEFAULT 1', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDEFAULT\s+FALSE\b', 'DEFAULT 0', text, flags=re.IGNORECASE)
    text = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", text)
    # Handle PostgreSQL cast operators :: (e.g., borrowed_at::date)
    text = re.sub(r'(\w+)::date', r'DATE(\1)', text, flags=re.IGNORECASE)
    text = re.sub(r'::\w+', '', text)  # remove any remaining casts
    # Remove PG specifics
    text = re.sub(r'CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+\w+;?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+USING\s+GIN\s*\([^)]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'GENERATED\s+ALWAYS\s+AS\s*\([^)]*\)\s+STORED', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COLLATE\s+[^\s,]+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COMMENT\s*=\s*\'[^\']*\'', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ENGINE\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'UNSIGNED', '', text, flags=re.IGNORECASE)
    # Remove partial indexes
    text = re.sub(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+[^(]*\([^)]*\)\s+WHERE\s+[^;]+;?', '', text, flags=re.IGNORECASE)
    return text

def find_matching_paren(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1

# -------------------------------------------------------------
# Pass 4: Build final statements with constraints merged
# -------------------------------------------------------------
final_statements = []

def merge_constraints(create_sql, constraints):
    create_sql = create_sql.strip()
    if create_sql.endswith(';'):
        create_sql = create_sql[:-1].strip()
    # Find outer parentheses
    try:
        start = create_sql.index('(')
        close = find_matching_paren(create_sql, start)
        if close == -1:
            # malformed
            return create_sql + ';'
    except ValueError:
        return create_sql + ';'
    header = create_sql[:start].strip()
    body = create_sql[start+1:close].strip()
    # Append constraints
    if constraints:
        for constraint in constraints:
            body = body.rstrip()
            if not body.endswith(','):
                body += ','
            body += f'\n{constraint},'
        body = re.sub(r',\s*$', '', body)  # strip trailing comma
    new_sql = f"{header} (\n{body}\n);"
    return new_sql

for tbl, raw_create in create_table_stmts.items():
    conv = convert_sql(raw_create)
    # Convert constraints as well
    raw_constraints = alter_constraints.get(tbl, [])
    converted_constraints = [convert_sql(c) for c in raw_constraints]
    final_stmt = merge_constraints(conv, converted_constraints)
    final_statements.append(final_stmt)

# Add other statements
for stmt in other_statements:
    conv = convert_sql(stmt)
    if not conv.endswith(';'):
        conv += ';'
    final_statements.append(conv)

print(f"Final statement count: {len(final_statements)}")

# -------------------------------------------------------------
# Write to file for review
# -------------------------------------------------------------
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(final_statements))

# -------------------------------------------------------------
# Execute
# -------------------------------------------------------------
import os
if os.path.exists('school_sell.db'):
    os.remove('school_sell.db')
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

errors = []
for idx, stmt in enumerate(final_statements, 1):
    try:
        cursor.execute(stmt)
    except (sqlite3.OperationalError, sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
        errors.append((idx, stmt[:200], str(e)))

conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\nCreated {len(tables)} tables")
for t in tables:
    print(f"  {t[0]}")

if errors:
    print(f"\nFirst 20 errors:")
    for idx, s, err in errors[:20]:
        print(f"  [{idx}] {err}")
        print(f"       {s[:150]}")
else:
    print("\nSUCCESS: All tables created without errors!")

conn.close()
