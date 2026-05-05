import sqlite3
import re
from collections import defaultdict

# Load raw SQL from script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# Split into statements by semicolon followed by newline
raw_statements = [s.strip() for s in re.split(r';\s*\n', raw_sql) if s.strip() and not s.strip().startswith('--')]
print(f"Split into {len(raw_statements)} raw statements")

# -------------------------------------------------------------
# Phase 1: Categorize statements
# -------------------------------------------------------------
create_table_stmts = {}  # table_name -> original CREATE TABLE statement (without semicolon)
alter_constraints = defaultdict(list)  # table_name -> list of "CONSTRAINT ..." strings
other_statements = []  # CREATE INDEX, etc.

for stmt in raw_statements:
    stmt_upper = stmt.upper()
    if stmt_upper.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in stmt_upper:
        # Parse: ALTER TABLE table_name ADD CONSTRAINT constraint_name definition
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', stmt, re.IGNORECASE)
        if m:
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            alter_constraints[tbl].append(f"  CONSTRAINT {cname} {cdef}")
    elif stmt_upper.startswith('CREATE TABLE'):
        # Extract table name
        m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            create_table_stmts[tbl] = stmt
        else:
            other_statements.append(stmt)
    elif stmt_upper.startswith('CREATE INDEX') or stmt_upper.startswith('CREATE UNIQUE INDEX'):
        other_statements.append(stmt)
    else:
        # Other DDL (e.g., comments, maybe CREATE SEQUENCE etc.), just keep
        other_statements.append(stmt)

print(f"CREATE TABLE: {len(create_table_stmts)}")
print(f"ALTER constraints: {sum(len(v) for v in alter_constraints.values())}")
print(f"Other statements: {len(other_statements)}")

# -------------------------------------------------------------
# Phase 2: Conversion function
# -------------------------------------------------------------
def convert_types(text):
    # Data types
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

# -------------------------------------------------------------
# Phase 3: Build final CREATE TABLE statements
# -------------------------------------------------------------
final_statements = []

for tbl, create_stmt in create_table_stmts.items():
    # Convert types in the whole statement
    converted = convert_types(create_stmt)
    
    # Extract the header and body
    # Find the body inside parentheses
    # Simple: Find the first '(' and its matching ')'
    start = converted.index('(')
    # Find matching closing paren (skip string literals)
    # Basic: since there are no nested parentheses on top level? Actually column definitions can have CHECK with parentheses. Use simple count.
    depth = 0
    end = start
    for idx in range(start, len(converted)):
        c = converted[idx]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                end = idx
                break
    header = converted[:start].strip()
    body = converted[start+1:end].strip()  # content inside parentheses
    
    # Add merged ALTER constraints as extra lines in body
    if tbl in alter_constraints:
        for constraint in alter_constraints[tbl]:
            body += ',\n' + constraint
    
    # Rebuild statement
    new_stmt = f"{header} (\n{body}\n);"
    final_statements.append(new_stmt)

# Add other statements (indexes) converted
for stmt in other_statements:
    converted = convert_types(stmt)
    # Ensure ends with semicolon
    if not converted.strip().endswith(';'):
        converted += ';'
    final_statements.append(converted)

print(f"Final statements: {len(final_statements)}")

# -------------------------------------------------------------
# Phase 4: Save and Execute
# -------------------------------------------------------------
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(final_statements))

import os
if os.path.exists('school_sell.db'):
    os.remove('school_sell.db')
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []
for idx, stmt in enumerate(final_statements, 1):
    try:
        cursor.execute(stmt)
        created += 1
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
    print("All tables created successfully!")
conn.close()
